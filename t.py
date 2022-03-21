import socket
import pandas as pd
import numpy as np
import time
import tensorflow as tf

DEFAULT_SCALE = np.sqrt(2)
DEFAULT_MODE = 'fan_in'


def ortho_init(scale=DEFAULT_SCALE, mode=None):
    def _ortho_init(shape, dtype, partition_info=None):
        # lasagne ortho init for tf
        shape = tuple(shape)
        if len(shape) == 2: # fc: in, out
            flat_shape = shape
        elif (len(shape) == 3) or (len(shape) == 4): # 1d/2dcnn: (in_h), in_w, in_c, out
            flat_shape = (np.prod(shape[:-1]), shape[-1])
        a = np.random.standard_normal(flat_shape)
        u, _, v = np.linalg.svd(a, full_matrices=False)
        q = u if u.shape == flat_shape else v # pick the one with the correct shape
        q = q.reshape(shape)
        return (scale * q).astype(np.float32)
    return _ortho_init

DEFAULT_METHOD = ortho_init

def fc(x, scope, n_out, act=tf.nn.relu, init_scale=DEFAULT_SCALE,
       init_mode=DEFAULT_MODE, init_method=DEFAULT_METHOD):
    with tf.variable_scope(scope):
        n_in = x.shape[1].value
        w = tf.get_variable("w", [n_in, n_out],
                            initializer=init_method(init_scale, init_mode))
        b = tf.get_variable("b", [n_out], initializer=tf.constant_initializer(0.0))
        z = tf.matmul(x, w) + b
        return act(z)

def batch_to_seq(x):
    n_step = x.shape[0].value
    if len(x.shape) == 1:
        x = tf.expand_dims(x, -1)
    return tf.split(axis=0, num_or_size_splits=n_step, value=x)

def seq_to_batch(x):
    return tf.concat(axis=0, values=x)

def lstm(xs, dones, s, scope, init_scale=DEFAULT_SCALE, init_mode=DEFAULT_MODE,
         init_method=DEFAULT_METHOD):
    
    xs = batch_to_seq(xs)
    # need dones to reset states
    dones = batch_to_seq(dones)
    n_in = xs[0].shape[1].value

    ############//整數除
    n_out = s.shape[0] // 2
    with tf.variable_scope(scope):
        wx = tf.get_variable("wx", [n_in, n_out*4],
                             initializer=init_method(init_scale, init_mode))
        wh = tf.get_variable("wh", [n_out, n_out*4],
                             initializer=init_method(init_scale, init_mode))
        b = tf.get_variable("b", [n_out*4], initializer=tf.constant_initializer(0.0))
    s = tf.expand_dims(s, 0)
    c, h = tf.split(axis=1, num_or_size_splits=2, value=s)
    for ind, (x, done) in enumerate(zip(xs, dones)):
        c = c * (1-done)
        h = h * (1-done)
        z = tf.matmul(x, wx) + tf.matmul(h, wh) + b
        i, f, o, u = tf.split(axis=1, num_or_size_splits=4, value=z)
        i = tf.nn.sigmoid(i)
        f = tf.nn.sigmoid(f)
        o = tf.nn.sigmoid(o)
        u = tf.tanh(u)
        c = f*c + i*u
        h = o*tf.tanh(c)
        xs[ind] = h
    s = tf.concat(axis=1, values=[c, h])
    return seq_to_batch(xs), tf.squeeze(s)
class TransBuffer:
    def reset(self):
        self.buffer = []

    @property
    def size(self):
        return len(self.buffer)

    def add_transition(self, ob, a, r, *_args, **_kwargs):
        raise NotImplementedError()

    def sample_transition(self, *_args, **_kwargs):
        raise NotImplementedError()
class OnPolicyBuffer(TransBuffer):
    def __init__(self, gamma):
        self.gamma = gamma
        self.reset()

    def reset(self, done=False):
        # the done before each step is required
        self.obs = []
        self.acts = []
        self.rs = []
        self.vs = []
        self.dones = [done]

    def add_transition(self, ob, a, r, v, done):
        self.obs.append(ob)
        self.acts.append(a)
        self.rs.append(r)
        self.vs.append(v)
        self.dones.append(done)
        
    def _add_R_Adv(self, R):
        Rs = []
        Advs = []
        # use post-step dones here
        for r, v, done in zip(self.rs[::-1], self.vs[::-1], self.dones[:0:-1]):
           
            R = r + self.gamma * R * (1.-done)
            
            Adv = R - v
            Rs.append(R)
            Advs.append(Adv)
        Rs.reverse()
        Advs.reverse()
        self.Rs = Rs
        self.Advs = Advs

    def sample_transition(self, R, discrete=True):
        self._add_R_Adv(R)
        obs = np.array(self.obs, dtype=np.float32)
        if discrete:
            acts = np.array(self.acts, dtype=np.int32)
        else:
            acts = np.array(self.acts, dtype=np.float32)

        
        Rs = np.array(self.Rs, dtype=np.float32)
        Advs = np.array(self.Advs, dtype=np.float32)
        # use pre-step dones here
        dones = np.array(self.dones[:-1], dtype=np.bool)
        self.reset(self.dones[-1])
        return obs, acts, dones, Rs, Advs


class FPlstm:
    def __init__(self, n_s, n_a, n_w,n_f, n_step, n_name, n_fc_wave=128, n_fc_wait=32, n_fc_fp=32, n_lstm=64):
        self.name = n_name
        self.n_a = n_a
        self.n_s = n_s
        self.n_w = n_w
        self.n_step = n_step
        self.n_lstm = n_lstm
        self.n_fc_wave = n_fc_wave
        self.n_fc_wait = n_fc_wait
        self.n_fc_fp = n_fc_fp
        self.ob_fw = tf.placeholder(tf.float32, [1, n_s + n_w + n_f])
        self.done_fw = tf.placeholder(tf.float32, [1])
        self.ob_bw = tf.placeholder(tf.float32, [n_step, n_s + n_w + n_f])
        self.done_bw = tf.placeholder(tf.float32, [n_step])
        self.states = tf.placeholder(tf.float32, [2, n_lstm * 2])
        self.sess = tf.Session()
        with tf.variable_scope(self.name):
            self.pi_fw, pi_state = self._build_net('forward', 'pi')
            ########################critic########################
            self.v_fw, v_state = self._build_net('forward', 'v')
            #增加單位向量1在哪個位子
            pi_state = tf.expand_dims(pi_state, 0)
            v_state = tf.expand_dims(v_state, 0)
            self.new_states = tf.concat([pi_state, v_state], 0)
        with tf.variable_scope(self.name, reuse=True):
            self.pi, _ = self._build_net('backward', 'pi')
            self.v, _ = self._build_net('backward', 'v')
        self._init_train()
        self.sess.run(tf.global_variables_initializer())
        self.saver = tf.train.Saver(max_to_keep=5)
        self._reset()

    def load(self, model_dir):
        self.saver.restore(self.sess, model_dir)

    def save(self, model_dir, global_step):
        self.saver.save(self.sess, model_dir + "checkpoint", global_step=global_step)

    def prepare_loss(self, v_coef, max_grad_norm, alpha, epsilon):
        self.A = tf.placeholder(tf.int32, [self.n_step])
        self.ADV = tf.placeholder(tf.float32, [self.n_step])
        self.R = tf.placeholder(tf.float32, [self.n_step])
        self.entropy_coef = tf.placeholder(tf.float32, [])
        A_sparse = tf.one_hot(self.A, self.n_a)
        log_pi = tf.log(tf.clip_by_value(self.pi, 1e-10, 1.0))
        entropy = -tf.reduce_sum(self.pi * log_pi, axis=1)
        entropy_loss = -tf.reduce_mean(entropy) * self.entropy_coef
        policy_loss = -tf.reduce_mean(tf.reduce_sum(log_pi * A_sparse, axis=1) * self.ADV)
        value_loss = tf.reduce_mean(tf.square(self.R - self.v)) * 0.5 * v_coef
        self.loss = policy_loss + value_loss + entropy_loss
        #print("entroy")
        #print(entropy_loss)
        #print("policy_loss")
        #print(policy_loss)
        #print("value loss")
        #print(value_loss)
        #print("######################")
        #print("loss: ")
        #print(self.loss)
        wts = tf.trainable_variables(scope=self.name)
        
        grads = tf.gradients(self.loss, wts)
        if max_grad_norm > 0:
            grads, self.grad_norm = tf.clip_by_global_norm(grads, max_grad_norm)
        self.lr = tf.placeholder(tf.float32, [])
        self.optimizer = tf.train.RMSPropOptimizer(learning_rate=self.lr, decay=alpha,
                                                   epsilon=epsilon)
        #print(list(zip(grads, wts)))
        self._train = self.optimizer.apply_gradients(list(zip(grads, wts)))
       
    def _init_train(self):
        # init loss
        v_coef = 0.5
        max_grad_norm = 40
        alpha = 0.99
        epsilon = 1e-5
        self.prepare_loss(v_coef, max_grad_norm, alpha, epsilon)

        # init replay buffer
        gamma = 0.99
        self.trans_buffer = OnPolicyBuffer(gamma)
    def add_transition(self, ob, action, reward, value, done):
        # Hard code the reward norm for negative reward only
        #if (self.reward_norm):
            #reward /= self.reward_norm
        #if self.reward_clip:
            ###########限定 reward 在 reaward 與 -reward_chip
            #reward = np.clip(reward, -self.reward_clip, self.reward_clip)
        self.trans_buffer.add_transition(ob, action, reward, value, done)
    def _reset(self):
        # forget the cumulative states every cum_step
        self.states_fw = np.zeros((2, self.n_lstm * 2), dtype=np.float32)
        self.states_bw = np.zeros((2, self.n_lstm * 2), dtype=np.float32)

    def _build_out_net(self, h, out_type):
        if out_type == 'pi':
            pi = fc(h, out_type, 2, act=tf.nn.softmax)

            #移除大小為1
            return tf.squeeze(pi)
        else:
            v = fc(h, out_type, 1, act=lambda x: x)
            return tf.squeeze(v)

    def _build_net(self, in_type, out_type):
        if in_type == 'forward':
            ob = self.ob_fw
            done = self.done_fw
        else:
            ob = self.ob_bw
            done = self.done_bw
        if out_type == 'pi':
            states = self.states[0]
        else:
            states = self.states[1]

        h0 = fc(ob[:, :self.n_s], out_type + '_fcw', self.n_fc_wave)
        
        ##################policy fc
        h1 = fc(ob[:, (self.n_s + self.n_w):], out_type + '_fcf', self.n_fc_fp)

        ##################MA2C沒wait state##########
        if self.n_w == 0:
            h = tf.concat([h0, h1], 1)
        else:

            h2 = fc(ob[:, self.n_s: (self.n_s + self.n_w)], out_type + '_fct', self.n_fc_wait)
            h = tf.concat([h0, h1, h2], 1)

        h, new_states = lstm(h, done, states, out_type + '_lstm')
        out_val = self._build_out_net(h, out_type)


        return out_val, new_states

    def _get_forward_outs(self, out_type):
        outs = []
        if 'p' in out_type:
            outs.append(self.pi_fw)
        if 'v' in out_type:
            outs.append(self.v_fw)
        return outs
    def _return_forward_outs(self, out_values):
        if len(out_values) == 1:
            return out_values[0]
        return out_values
    
    def forward(self, ob, done, out_type='pv'):
        outs = self._get_forward_outs(out_type)
        # update state only when p is called
        if 'p' in out_type:
            outs.append(self.new_states)

        #print("out: ")
        #print(outs)
        out_values = self.sess.run(outs, {self.ob_fw:np.array([ob]),
                                     self.done_fw:np.array([done]),
                                     self.states:self.states_fw})
        #print(out_values)
        if 'p' in out_type:
            self.states_fw = out_values[-1]
            out_values = out_values[:-1]
        return self._return_forward_outs(out_values)


    def backward(self, R, summary_writer=None, global_step=None):
        if summary_writer is None:
            ops = self._train
        else:
            ops = [self.summary, self._train]
        obs, acts, dones, Rs, Advs = self.trans_buffer.sample_transition(R)
        #print(Advs)
        outs = self.sess.run(ops,
                        {self.ob_bw: obs,
                         self.done_bw: dones,
                         self.states: self.states_bw,
                         self.A: acts,
                         self.ADV: Advs,
                         self.R: Rs,
                         self.lr: 5e-4,
                         self.entropy_coef:  0.01})
        
        self.states_bw = np.copy(self.states_fw)
        


def update_action(policy, phase, name, simTime):
    if(policy == 0):
        return
    if((name == "ms") ):
        if(phase == 1):
            for i in range(5):	
                if(i == 0):
                    s.sendall(MSp1Y)
                if(i == 2):
                    s.sendall(MSp1R)
                if(i == 5):
                    s.sendall(MSp2)

        if(phase == 2):
            for i in range(5):	
                if(i == 0):
                    s.sendall(MSp2Y)
                if(i == 2):
                    s.sendall(MSp2R)
                if(i == 5):
                    s.sendall(MSp1)
def init_policy(n_s, n_a, n_w, n_f, agent_name):
    n_fw = 128
    n_ft = 32
    n_lstm = 64
    n_fp = 64
    n_step = 40

    policy = FPlstm(n_s, n_a, n_w, n_f, n_step, n_name=agent_name, n_fc_wave=n_fw,
                    n_fc_wait=n_ft, n_fc_fp=n_fp, n_lstm=n_lstm)

    return policy

'''
ms_policy = init_policy(n_s = 10, n_a = 2, n_w = 0, n_f = 5, agent_name = "ms")
ob = [0.  , 0.  , 0.  , 0.  , 0.  , 0.  , 0.  , 0.  , 0.  , 0. , 0.5 , 0.25, 0.25, 0.25, 0.25]
done = True
n_step = 40
for j in range(5):
    for i in range(40):
        fw = ms_policy.forward(ob, done, 'pv')
        policy = (fw[0])
        value = (fw[1])
        print(policy)
        print(value)
        action = 1
        reward = 0.001 * j
        ob = [1. , 3.  , 0.  , 0.  , 0.  , 0.  , 0.  , 0.  , 0.  , 0. , 0.5 , 0.25, 0.25, 0.25, 0.25]
        ms_policy.add_transition(ob, action, reward, value, done)
    R = ms_policy.forward(ob, False, 'v')

    ob = [1. , 3.  , 0.  , 0.  , 0.  , 0.  , 0.  , 0.  , 0.  , 0. , 0.5 , 0.25, 0.25, 0.25, 0.25]

    ms_policy.backward(R)
'''