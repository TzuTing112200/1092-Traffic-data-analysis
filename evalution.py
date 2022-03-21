import socket
import pandas as pd
import numpy as np
import time
import datetime
from t import *

def df_empty(columns, dtypes, index=None):
    df = pd.DataFrame(index=index)
    for c,d in zip(columns, dtypes):
        df[c] = pd.Series(dtype=d)
    return df

ms_policy = init_policy(n_s = 13, n_a = 2, n_w = 0, n_f = 2, agent_name = "ms")
mn_policy = init_policy(n_s = 19, n_a = 2, n_w = 0, n_f = 3, agent_name = "mn")
pg_policy = init_policy(n_s = 20, n_a = 2, n_w = 0, n_f = 3, agent_name = "pg")
hn_policy = init_policy(n_s = 22, n_a = 2, n_w = 0, n_f = 3, agent_name = "hn")
dz_policy = init_policy(n_s = 22, n_a = 2, n_w = 0, n_f = 2, agent_name = "dz")

ms_policy.load("E:\\tlc-sim\\model\\model2\\ms_checkpoint-200")
mn_policy.load("E:\\tlc-sim\\model\\model2\\mn_checkpoint-200")
pg_policy.load("E:\\tlc-sim\\model\\model2\\pg_checkpoint-200")
hn_policy.load("E:\\tlc-sim\\model\\model2\\hn_checkpoint-200")
dz_policy.load("E:\\tlc-sim\\model\\model2\\dz_checkpoint-200")

MSp2_1G = b'minShengP2_1Green\n' # phase1 green
MSp1_2Y = b'minShengP1_2Yellow\n'
MSp1_2R = b'minShengP1_2AllRed\n'

MSp1_2G = b'minShengP1_2Green\n' # phase2 green
MSp2_1Y = b'minShengP2_1Yellow\n'
MSp2_1R = b'minShengP2_1AllRed\n'

MAp2_1G = b'minAnP2_1Green\n' # phase1 green
MAp1_2Y = b'minAnP1_2Yellow\n'
MAp1_2R = b'minAnP1_2AllRed\n'

MAp1_2G = b'minAnP1_2Green\n' # phase2 green
MAp2_1Y = b'minAnP2_1Yellow\n'
MAp2_1R = b'minAnP2_1AllRed\n'

PAp2_1G = b'pingAnP2_1Green\n' # phase1 green
PAp1_2Y = b'pingAnP1_2Yellow\n'
PAp1_2R = b'pingAnP1_2AllRed\n'

PAp1_2G = b'pingAnP1_2Green\n' # phase2 green
PAp2_1Y = b'pingAnP2_1Yellow\n'
PAp2_1R = b'pingAnP2_1AllRed\n'

HNp3_1G = b'hengNanP3_1Green\n' # phase1 green
HNp2_1G = b'hengNanP2_1Green\n'

HNp1_2Y = b'hengNanP1_2Yellow\n'
HNp1_2R = b'hengNanP1_2AllRed\n'

HNp1_3Y = b'hengNanP1_3Yellow\n'
HNp1_3R = b'hengNanP1_3AllRed\n'

HNp1_2G = b'hengNanP1_2Green\n' # phase2 green
HNp1_3G = b'hengNanP1_3Green\n'

HNp2_3Y = b'hengNanP2_3Yellow\n'
HNp2_1Y = b'hengNanP2_1Yellow\n'

HNp2_3R = b'hengNanP2_3AllRed\n'
HNp2_1R = b'hengNanP2_1AllRed\n'

HNp2_3G = b'hengNanP2_3Green\n' # phase3 green
HNp1_3G = b'hengNanP1_3Green\n'

HNp3_1Y = b'hengNanP3_1Yellow\n'
HNp3_2Y = b'hengNanP3_2Yellow\n'

HNp3_1R = b'hengNanP3_1AllRed\n'
HNp3_2R = b'hengNanP3_2AllRed\n'

ERp4_1G = b'eastRampP4_1Green\n' # phase1 green
ERp2_1G = b'eastRampP2_1Green\n'
ERp3_1G = b'eastRampP3_1Green\n'

ERp1_2Y = b'eastRampP1_2Yellow\n'
ERp1_3Y = b'eastRampP1_3Yellow\n'
ERp1_4Y = b'eastRampP1_4Yellow\n'

ERp1_2R = b'eastRampP1_2AllRed\n'
ERp1_3R = b'eastRampP1_3AllRed\n'
ERp1_4R = b'eastRampP1_4AllRed\n'

ERp1_2G = b'eastRampP1_2Green\n' # phase2 green
ERp3_2G = b'eastRampP3_2Green\n'
ERp4_2G = b'eastRampP4_2Green\n'

ERp2_3Y = b'eastRampP2_3Yellow\n'
ERp2_1Y = b'eastRampP2_1Yellow\n'
ERp2_4Y = b'eastRampP2_4Yellow\n'

ERp2_3R = b'eastRampP2_3AllRed\n'
ERp2_1R = b'eastRampP2_1AllRed\n'
ERp2_4R = b'eastRampP2_4AllRed\n'

ERp2_3G = b'eastRampP2_3Green\n' # phase3 green
ERp1_3G = b'eastRampP1_3Green\n'
ERp4_3G = b'eastRampP4_3Green\n'

ERp3_4Y = b'eastRampP3_4Yellow\n'
ERp3_1Y = b'eastRampP3_1Yellow\n'
ERp3_2Y = b'eastRampP3_2Yellow\n'

ERp3_4R = b'eastRampP3_4AllRed\n'
ERp3_1R = b'eastRampP3_1AllRed\n'
ERp3_2R = b'eastRampP3_2AllRed\n'

ERp3_4G = b'eastRampP3_4Green\n' # phase4 green
ERp1_4G = b'eastRampP1_4Green\n'
ERp2_4G = b'eastRampP2_4Green\n'

ERp4_1Y = b'eastRampP4_1Yellow\n'
ERp4_2Y = b'eastRampP4_2Yellow\n'
ERp4_3Y = b'eastRampP4_3Yellow\n'

ERp4_1R = b'eastRampP4_1AllRed\n'
ERp4_2R = b'eastRampP4_2AllRed\n'
ERp4_3R = b'eastRampP4_3AllRed\n'

getState = b'getState\n'
repaint = b'repaint\n'
simStep = b'simStep\n'


def update_action(s, policy, phase, stateDF, simTime, step):
    yellowCommand = bytearray()
    allredCommand = bytearray()
    newphaseCommand = bytearray()
    for i in range(5):
        if(policy[i] == 0):
            continue
        else:
            if(i == 0):
                if(phase[0] == 1):
                    yellowCommand += b'minShengP1_2Yellow\n'
                    allredCommand += b'minShengP1_2AllRed\n'
                    newphaseCommand += b'minShengP1_2Green\r\n'
                    phase[0] = 2
                else:
                    yellowCommand += b'minShengP2_1Yellow\n'
                    allredCommand +=  b'minShengP2_1AllRed\n'
                    newphaseCommand += b'minShengP2_1Green\r\n'
                    phase[0] = 1

            if(i == 1):
                if(phase[1] == 1):
                    yellowCommand += b'minAnP1_2Yellow\n'
                    allredCommand += b'minAnP1_2AllRed\n'
                    newphaseCommand += b'minAnP1_2Green\r\n'
                    phase[1] = 2
                else:
                    yellowCommand += b'minAnP2_1Yellow\n'
                    allredCommand += b'minAnP2_1AllRed\n'
                    newphaseCommand += b'minAnP2_1Green\r\n'
                    phase[1] = 1

            if(i == 2):
                if(phase[2] == 1):
                    yellowCommand += b'pingAnP1_2Yellow\n'
                    allredCommand += b'pingAnP1_2AllRed\n'
                    newphaseCommand += b'pingAnP1_2Green\r\n'
                    phase[2] = 2
                else:
                    yellowCommand += b'pingAnP2_1Yellow\n'
                    allredCommand += b'pingAnP2_1AllRed\n'
                    newphaseCommand += b'pingAnP2_1Green\r\n'
                    phase[2] = 1

            if(i == 3):
                if(phase[3] == 1):
                    yellowCommand += b'hengNanP1_2Yellow\n'
                    allredCommand += b'hengNanP1_2AllRed\n'
                    newphaseCommand += b'hengNanP1_2Green\r\n'
                    phase[3] = 2
                elif(phase[3] == 2):
                    yellowCommand += b'hengNanP2_3Yellow\n'
                    allredCommand += b'hengNanP2_3AllRed\n'
                    newphaseCommand += b'hengNanP2_3Green\r\n'
                    phase[3] = 3
                else:
                    yellowCommand += b'hengNanP3_1Yellow\n'
                    allredCommand += b'hengNanP3_1AllRed\n'
                    newphaseCommand += b'hengNanP3_1Green\r\n'
                    phase[3] = 1

            if(i == 4):
                if(phase[4] == 1):
                    yellowCommand += b'eastRampP1_2Yellow\n'
                    allredCommand += b'eastRampP1_2AllRed\n'
                    newphaseCommand += b'eastRampP1_2Green\r\n'
                    phase[4] = 2
                elif(phase[4] == 2):
                    yellowCommand += b'eastRampP2_3Yellow\n'
                    allredCommand += b'eastRampP2_3AllRed\n'
                    newphaseCommand += b'eastRampP2_3Green\r\n'
                    phase[4] = 3
                elif(phase[4] == 3):
                    yellowCommand += b'eastRampP3_4Yellow\n'
                    allredCommand += b'eastRampP3_4AllRed\n'
                    newphaseCommand += b'eastRampP3_4Green\r\n'
                    phase[4] = 4
                else:
                    yellowCommand += b'eastRampP4_1Yellow\n'
                    allredCommand += b'eastRampP4_1AllRed\n'
                    newphaseCommand += b'eastRampP4_1Green\r\n'
                    phase[4] = 1
    #print(yellowCommand)
    #print(allredCommand)
    #print(newphaseCommand)
    for i in range(5):
        simTime += 1
        if(i == 4):
            s.sendall(b'simStep 1\r\n'+getState + repaint)
            step += 1            
            data = s.recv(8192)
            lst = data.decode('ascii')[:-2].split()
            state = [step] + [int(i) for i in lst]
            stateDF.loc[len(stateDF.index)] = state

            s.sendall(newphaseCommand)

        else:
            ###
            if(i == 0):
                s.sendall(yellowCommand)

            if(i == 2):
                s.sendall(allredCommand)
            
            s.sendall(b'simStep 1\r\n' + repaint)
        
        
    return simTime, step




stateAttributes = ['simTime',
        'laneA0Q', 'laneA0T', 'laneA1Q', 'laneA1T', 'laneB0Q', 'laneB0T', 
            'laneB1Q', 'laneB1T', 'laneC0Q', 'laneC0T', 'laneC1Q', 'laneC1T', 
            'laneD0Q', 'laneD0T', 'laneD1Q', 'laneD1T', 'laneD2Q', 'laneD2T', 
            'laneE0Q', 'laneE0T', 'laneE1Q', 'laneE1T', 'laneE2Q', 'laneE2T',
        'laneE3Q', 'laneE3T', 'laneF0Q', 'laneF0T', 'laneF1Q', 'laneF1T', 
            'laneF2Q', 'laneF2T', 'laneU0Q', 'laneU0T', 'laneU1Q', 'laneU1T', 
            'laneU2Q', 'laneU2T', 'laneV0Q', 'laneV0T', 'laneV1Q', 'laneV1T', 
            'laneV2Q', 'laneV2T', 'laneW0Q', 'laneW0T', 'laneW1Q', 'laneW1T', 
            'laneW2Q', 'laneW2T', 'laneX0Q', 'laneX0T', 'laneX1Q', 'laneX1T', 
            'laneX2Q', 'laneX2T', 'laneY0Q', 'laneY0T', 'laneY0F', 'laneY0Fo', 
            'laneY1Q', 'laneY1T', 'laneY2Q', 'laneY2T', 'laneY2F', 'laneY2Fo', 
            'laneI0Q', 'laneI0T', 'laneI1Q', 'laneI1T', 'laneJ0Q', 'laneJ0T', 
            'laneK0Q', 'laneK0T', 'laneL0Q', 'laneL0T', 'laneM0Q', 'laneM0T', 
            'laneN0Q', 'laneN0T', 'laneN1Q', 'laneN1T', 'laneO0Q', 'laneO0T', 
            'laneO0F', 'laneO0Fo', 'laneP0Q', 'laneP0T',
        'laneA0VehOuts', 'laneA0SIVehOuts', 'laneA0SIVehI2OTT', 'laneA0SIVehO2OTT)', 'laneA0TIVehOuts', 'laneA0TIVehI2OTT', 'laneA0TIVehO2OTT', 'laneA0SIVehCycles', 'laneA0TIVehCycles', 'laneA0FirstVehStoppedTime', 'laneA0FirstVehAccCycles',
        'laneA1VehOuts', 'laneA1SIVehOuts', 'laneA1SIVehI2OTT', 'laneA1SIVehO2OTT)', 'laneA1TIVehOuts', 'laneA1TIVehI2OTT', 'laneA1TIVehO2OTT', 'laneA1SIVehCycles', 'laneA1TIVehCycles', 'laneA1FirstVehStoppedTime', 'laneA1FirstVehAccCycles',
        'laneB0VehOuts', 'laneB0SIVehOuts', 'laneB0SIVehI2OTT', 'laneB0SIVehO2OTT)', 'laneB0TIVehOuts', 'laneB0TIVehI2OTT', 'laneB0TIVehO2OTT', 'laneB0SIVehCycles', 'laneB0TIVehCycles', 'laneB0FirstVehStoppedTime', 'laneB0FirstVehAccCycles',
        'laneB1VehOuts', 'laneB1SIVehOuts', 'laneB1SIVehI2OTT', 'laneB1SIVehO2OTT)', 'laneB1TIVehOuts', 'laneB1TIVehI2OTT', 'laneB1TIVehO2OTT', 'laneB1SIVehCycles', 'laneB1TIVehCycles', 'laneB1FirstVehStoppedTime', 'laneB1FirstVehAccCycles',
        'laneC0VehOuts', 'laneC0SIVehOuts', 'laneC0SIVehI2OTT', 'laneC0SIVehO2OTT)', 'laneC0TIVehOuts', 'laneC0TIVehI2OTT', 'laneC0TIVehO2OTT', 'laneC0SIVehCycles', 'laneC0TIVehCycles', 'laneC0FirstVehStoppedTime', 'laneC0FirstVehAccCycles',
        'laneC1VehOuts', 'laneC1SIVehOuts', 'laneC1SIVehI2OTT', 'laneC1SIVehO2OTT)', 'laneC1TIVehOuts', 'laneC1TIVehI2OTT', 'laneC1TIVehO2OTT', 'laneC1SIVehCycles', 'laneC1TIVehCycles', 'laneC1FirstVehStoppedTime', 'laneC1FirstVehAccCycles',
        'laneD0VehOuts', 'laneD0SIVehOuts', 'laneD0SIVehI2OTT', 'laneD0SIVehO2OTT)', 'laneD0TIVehOuts', 'laneD0TIVehI2OTT', 'laneD0TIVehO2OTT', 'laneD0SIVehCycles', 'laneD0TIVehCycles', 'laneD0FirstVehStoppedTime', 'laneD0FirstVehAccCycles',
        'laneD1VehOuts', 'laneD1SIVehOuts', 'laneD1SIVehI2OTT', 'laneD1SIVehO2OTT)', 'laneD1TIVehOuts', 'laneD1TIVehI2OTT', 'laneD1TIVehO2OTT', 'laneD1SIVehCycles', 'laneD1TIVehCycles', 'laneD1FirstVehStoppedTime', 'laneD1FirstVehAccCycles',
        'laneD2VehOuts', 'laneD2SIVehOuts', 'laneD2SIVehI2OTT', 'laneD2SIVehO2OTT)', 'laneD2TIVehOuts', 'laneD2TIVehI2OTT', 'laneD2TIVehO2OTT', 'laneD2SIVehCycles', 'laneD2TIVehCycles', 'laneD2FirstVehStoppedTime', 'laneD2FirstVehAccCycles',
        'laneE0VehOuts', 'laneE0SIVehOuts', 'laneE0SIVehI2OTT', 'laneE0SIVehO2OTT)', 'laneE0TIVehOuts', 'laneE0TIVehI2OTT', 'laneE0TIVehO2OTT', 'laneE0SIVehCycles', 'laneE0TIVehCycles', 'laneE0FirstVehStoppedTime', 'laneE0FirstVehAccCycles',
        'laneE1VehOuts', 'laneE1SIVehOuts', 'laneE1SIVehI2OTT', 'laneE1SIVehO2OTT)', 'laneE1TIVehOuts', 'laneE1TIVehI2OTT', 'laneE1TIVehO2OTT', 'laneE1SIVehCycles', 'laneE1TIVehCycles', 'laneE1FirstVehStoppedTime', 'laneE1FirstVehAccCycles',
        'laneE2VehOuts', 'laneE2SIVehOuts', 'laneE2SIVehI2OTT', 'laneE2SIVehO2OTT)', 'laneE2TIVehOuts', 'laneE2TIVehI2OTT', 'laneE2TIVehO2OTT', 'laneE2SIVehCycles', 'laneE2TIVehCycles', 'laneE2FirstVehStoppedTime', 'laneE2FirstVehAccCycles',
        'laneE3VehOuts', 'laneE3SIVehOuts', 'laneE3SIVehI2OTT', 'laneE3SIVehO2OTT)', 'laneE3TIVehOuts', 'laneE3TIVehI2OTT', 'laneE3TIVehO2OTT', 'laneE3SIVehCycles', 'laneE3TIVehCycles', 'laneE3FirstVehStoppedTime', 'laneE3FirstVehAccCycles',
        'laneU0VehOuts', 'laneU0SIVehOuts', 'laneU0SIVehI2OTT', 'laneU0SIVehO2OTT)', 'laneU0TIVehOuts', 'laneU0TIVehI2OTT', 'laneU0TIVehO2OTT', 'laneU0SIVehCycles', 'laneU0TIVehCycles', 'laneU0FirstVehStoppedTime', 'laneU0FirstVehAccCycles',
        'laneU1VehOuts', 'laneU1SIVehOuts', 'laneU1SIVehI2OTT', 'laneU1SIVehO2OTT)', 'laneU1TIVehOuts', 'laneU1TIVehI2OTT', 'laneU1TIVehO2OTT', 'laneU1SIVehCycles', 'laneU1TIVehCycles', 'laneU1FirstVehStoppedTime', 'laneU1FirstVehAccCycles',
        'laneU2VehOuts', 'laneU2SIVehOuts', 'laneU2SIVehI2OTT', 'laneU2SIVehO2OTT)', 'laneU2TIVehOuts', 'laneU2TIVehI2OTT', 'laneU2TIVehO2OTT', 'laneU2SIVehCycles', 'laneU2TIVehCycles', 'laneU2FirstVehStoppedTime', 'laneU2FirstVehAccCycles',
        'laneV0VehOuts', 'laneV0SIVehOuts', 'laneV0SIVehI2OTT', 'laneV0SIVehO2OTT)', 'laneV0TIVehOuts', 'laneV0TIVehI2OTT', 'laneV0TIVehO2OTT', 'laneV0SIVehCycles', 'laneV0TIVehCycles', 'laneV0FirstVehStoppedTime', 'laneV0FirstVehAccCycles',
        'laneV1VehOuts', 'laneV1SIVehOuts', 'laneV1SIVehI2OTT', 'laneV1SIVehO2OTT)', 'laneV1TIVehOuts', 'laneV1TIVehI2OTT', 'laneV1TIVehO2OTT', 'laneV1SIVehCycles', 'laneV1TIVehCycles', 'laneV1FirstVehStoppedTime', 'laneV1FirstVehAccCycles',
        'laneV2VehOuts', 'laneV2SIVehOuts', 'laneV2SIVehI2OTT', 'laneV2SIVehO2OTT)', 'laneV2TIVehOuts', 'laneV2TIVehI2OTT', 'laneV2TIVehO2OTT', 'laneV2SIVehCycles', 'laneV2TIVehCycles', 'laneV2FirstVehStoppedTime', 'laneV2FirstVehAccCycles',
        'laneW0VehOuts', 'laneW0SIVehOuts', 'laneW0SIVehI2OTT', 'laneW0SIVehO2OTT)', 'laneW0TIVehOuts', 'laneW0TIVehI2OTT', 'laneW0TIVehO2OTT', 'laneW0SIVehCycles', 'laneW0TIVehCycles', 'laneW0FirstVehStoppedTime', 'laneW0FirstVehAccCycles',
        'laneW1VehOuts', 'laneW1SIVehOuts', 'laneW1SIVehI2OTT', 'laneW1SIVehO2OTT)', 'laneW1TIVehOuts', 'laneW1TIVehI2OTT', 'laneW1TIVehO2OTT', 'laneW1SIVehCycles', 'laneW1TIVehCycles', 'laneW1FirstVehStoppedTime', 'laneW1FirstVehAccCycles',
        'laneW2VehOuts', 'laneW2SIVehOuts', 'laneW2SIVehI2OTT', 'laneW2SIVehO2OTT)', 'laneW2TIVehOuts', 'laneW2TIVehI2OTT', 'laneW2TIVehO2OTT', 'laneW2SIVehCycles', 'laneW2TIVehCycles', 'laneW2FirstVehStoppedTime', 'laneW2FirstVehAccCycles',
        'laneX0VehOuts', 'laneX0SIVehOuts', 'laneX0SIVehI2OTT', 'laneX0SIVehO2OTT)', 'laneX0TIVehOuts', 'laneX0TIVehI2OTT', 'laneX0TIVehO2OTT', 'laneX0SIVehCycles', 'laneX0TIVehCycles', 'laneX0FirstVehStoppedTime', 'laneX0FirstVehAccCycles',
        'laneX1VehOuts', 'laneX1SIVehOuts', 'laneX1SIVehI2OTT', 'laneX1SIVehO2OTT)', 'laneX1TIVehOuts', 'laneX1TIVehI2OTT', 'laneX1TIVehO2OTT', 'laneX1SIVehCycles', 'laneX1TIVehCycles', 'laneX1FirstVehStoppedTime', 'laneX1FirstVehAccCycles',
        'laneX2VehOuts', 'laneX2SIVehOuts', 'laneX2SIVehI2OTT', 'laneX2SIVehO2OTT)', 'laneX2TIVehOuts', 'laneX2TIVehI2OTT', 'laneX2TIVehO2OTT', 'laneX2SIVehCycles', 'laneX2TIVehCycles', 'laneX2FirstVehStoppedTime', 'laneX2FirstVehAccCycles',
        'laneY0VehOuts', 'laneY0SIVehOuts', 'laneY0SIVehI2OTT', 'laneY0SIVehO2OTT)', 'laneY0TIVehOuts', 'laneY0TIVehI2OTT', 'laneY0TIVehO2OTT', 'laneY0SIVehCycles', 'laneY0TIVehCycles', 'laneY0FirstVehStoppedTime', 'laneY0FirstVehAccCycles',
        'laneY0ForkVehOuts', 'laneY0SIForkVehOuts', 'laneY0SIForkVehI2OTT', 'laneY0SIForkVehO2OTT)', 'laneY0TIForkVehOuts', 'laneY0TIForkVehI2OTT', 'laneY0TIForkVehO2OTT', 'laneY0SIForkVehCycles', 'laneY0TIForkVehCycles', 'laneY0FirstForkVehStoppedTime', 'laneY0FirstForkVehAccCycles',
        'laneY1VehOuts', 'laneY1SIVehOuts', 'laneY1SIVehI2OTT', 'laneY1SIVehO2OTT)', 'laneY1TIVehOuts', 'laneY1TIVehI2OTT', 'laneY1TIVehO2OTT', 'laneY1SIVehCycles', 'laneY1TIVehCycles', 'laneY1FirstVehStoppedTime', 'laneY1FirstVehAccCycles',
        'laneY2VehOuts', 'laneY2SIVehOuts', 'laneY2SIVehI2OTT', 'laneY2SIVehO2OTT)', 'laneY2TIVehOuts', 'laneY2TIVehI2OTT', 'laneY2TIVehO2OTT', 'laneY2SIVehCycles', 'laneY2TIVehCycles', 'laneY2FirstVehStoppedTime', 'laneY2FirstVehAccCycles',
        'laneY2ForkVehOuts', 'laneY2SIForkVehOuts', 'laneY2SIForkVehI2OTT', 'laneY2SIForkVehO2OTT)', 'laneY2TIForkVehOuts', 'laneY2TIForkVehI2OTT', 'laneY2TIForkVehO2OTT', 'laneY2SIForkVehCycles', 'laneY2TIForkVehCycles', 'laneY2FirstForkVehStoppedTime', 'laneY2FirstForkVehAccCycles',
        'laneI0VehOuts', 'laneI0SIVehOuts', 'laneI0SIVehI2OTT', 'laneI0SIVehO2OTT)', 'laneI0TIVehOuts', 'laneI0TIVehI2OTT', 'laneI0TIVehO2OTT', 'laneI0SIVehCycles', 'laneI0TIVehCycles', 'lanI0FirstVehStoppedTime', 'laneI0FirstVehAccCycles',
        'laneI1VehOuts', 'laneI1SIVehOuts', 'laneI1SIVehI2OTT', 'laneI1SIVehO2OTT)', 'laneI1TIVehOuts', 'laneI1TIVehI2OTT', 'laneI1TIVehO2OTT', 'laneI1SIVehCycles', 'laneI1TIVehCycles', 'lanI1FirstVehStoppedTime', 'laneI1FirstVehAccCycles',
        'laneI1ForkVehOuts', 'laneI1SIForkVehOuts', 'laneI1SIForkVehI2OTT', 'laneI1SIForkVehO2OTT)', 'laneI1TIForkVehOuts', 'laneI1TIForkVehI2OTT', 'laneI1TIForkVehO2OTT', 'laneI1SIForkVehCycles', 'laneI1TIForkVehCycles', 'laneI1FirstForkVehStoppedTime', 'laneI1FirstForkVehAccCycles',
        'laneJ0VehOuts', 'laneJ0SIVehOuts', 'laneJ0SIVehI2OTT', 'laneJ0SIVehO2OTT)', 'laneJ0TIVehOuts', 'laneJ0TIVehI2OTT', 'laneJ0TIVehO2OTT', 'laneJ0SIVehCycles', 'laneJ0TIVehCycles', 'laneJ0FirstVehStoppedTime', 'laneJ0FirstVehAccCycles',
        'laneK0VehOuts', 'laneK0SIVehOuts', 'laneK0SIVehI2OTT', 'laneK0SIVehO2OTT)', 'laneK0TIVehOuts', 'laneK0TIVehI2OTT', 'laneK0TIVehO2OTT', 'laneK0SIVehCycles', 'laneK0TIVehCycles', 'laneK0FirstVehStoppedTime', 'laneK0FirstVehAccCycles',
        'laneL0VehOuts', 'laneL0SIVehOuts', 'laneL0SIVehI2OTT', 'laneL0SIVehO2OTT)', 'laneL0TIVehOuts', 'laneL0TIVehI2OTT', 'laneL0TIVehO2OTT', 'laneL0SIVehCycles', 'laneL0TIVehCycles', 'laneL0FirstVehStoppedTime', 'laneL0FirstVehAccCycles',
        'laneM0VehOuts', 'laneM0SIVehOuts', 'laneM0SIVehI2OTT', 'laneM0SIVehO2OTT)', 'laneM0TIVehOuts', 'laneM0TIVehI2OTT', 'laneM0TIVehO2OTT', 'laneM0SIVehCycles', 'laneM0TIVehCycles', 'laneM0FirstVehStoppedTime', 'laneM0FirstVehAccCycles',
        'laneN0VehOuts', 'laneN0SIVehOuts', 'laneN0SIVehI2OTT', 'laneN0SIVehO2OTT)', 'laneN0TIVehOuts', 'laneN0TIVehI2OTT', 'laneN0TIVehO2OTT', 'laneN0SIVehCycles', 'laneN0TIVehCycles', 'laneN0FirstVehStoppedTime', 'laneN0FirstVehAccCycles',
        'laneN1VehOuts', 'laneN1SIVehOuts', 'laneN1SIVehI2OTT', 'laneN1SIVehO2OTT)', 'laneN1TIVehOuts', 'laneN1TIVehI2OTT', 'laneN1TIVehO2OTT', 'laneN1SIVehCycles', 'laneN1TIVehCycles', 'laneN1FirstVehStoppedTime', 'laneN1FirstVehAccCycles',
        'laneO0VehOuts', 'laneO0SIVehOuts', 'laneO0SIVehI2OTT', 'laneO0SIVehO2OTT)', 'laneO0TIVehOuts', 'laneO0TIVehI2OTT', 'laneO0TIVehO2OTT', 'laneO0SIVehCycles', 'laneO0TIVehCycles', 'laneO0FirstVehStoppedTime', 'laneO0FirstVehAccCycles',
        'laneO0ForkVehOuts', 'laneO0SIForkVehOuts', 'laneO0SIForkVehI2OTT', 'laneO0SIForkVehO2OTT)', 'laneO0TIForkVehOuts', 'laneO0TIForkVehI2OTT', 'laneO0TIForkVehO2OTT', 'laneO0SIForkVehCycles', 'laneO0TIForkVehCycles', 'laneO0FirstForkVehStoppedTime', 'laneO0FirstForkVehAccCycles',
        'laneP0VehOuts', 'laneP0SIVehOuts', 'laneP0SIVehI2OTT', 'laneP0SIVehO2OTT)', 'laneP0TIVehOuts', 'laneP0TIVehI2OTT', 'laneP0TIVehO2OTT', 'laneP0SIVehCycles', 'laneP0TIVehCycles', 'laneP0FirstVehStoppedTime', 'laneP0FirstVehAccCycles']

#stateDF = df_empty(stateAttributes, [int] * len(stateAttributes))

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 9091        # The port used by the server

now = datetime.datetime.now()
current_time = now.strftime("%H:%M:%S")
print("Current Time =", current_time)
total_reward = []
n_p = [1, 1, 1, 1, 1]
step = 0
nofirst = False

cols = ["step", "ms_reward", "mn_reward", "pg_reward", "hn_reward", "dz_reward"]

reward_data = []
phase_data = []
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print('connected')
    
    for i in range(1):
        simTime = 0
        t_r = 0
        n_p = [1, 1, 1, 1, 1]
        step = 0
        nofirst = False
        gamma = 0.9
        stateDF = df_empty(stateAttributes, [int] * len(stateAttributes))
        print("start epoch: " + str(i)) 
        while simTime < 3600:

            ##intetate 2
            if(simTime < 300):
#            simTime += 1
#            if simTime % 5 == 0:
#                s.sendall(b'simStep 1\r\n')
#                data = s.recv(1024)
##                print(data)
#                s.sendall(getState)
#                data = s.recv(8192)
#                lst = data.decode('ascii')[:-2].split()
#                state = [simTime] + [int(i) for i in lst]
#                stateDF.loc[len(stateDF.index)] = state
#            else:
#                s.sendall(b'simStep 1\r\n')
#                data = s.recv(1024)
##                print(data)
            
            

                simTime += 1;
                if(simTime == 300):
                    s.sendall(b'simStep 1\r\n'+getState+ repaint)
                    data = s.recv(8192)
                    lst = data.decode('ascii')[:-2].split()
                    state = [step] + [int(i) for i in lst]
                    stateDF.loc[len(stateDF.index)] = state
                    s.sendall(MSp2_1G+MAp2_1G+PAp2_1G+HNp3_1G+ERp4_1G)
                else:
                    s.sendall(b'simStep 1\r\n')
            
                sec = simTime % 150
                if sec==0:
                    s.sendall(MSp2_1G+MAp2_1G+PAp2_1G+HNp3_1G+ERp4_1G)
                elif sec==84:
                    s.sendall(ERp1_2Y)
                elif sec==87:
                    s.sendall(ERp1_2R)
                elif sec==90:
                    s.sendall(ERp1_2G)
                elif sec==93:
                    s.sendall(MSp1_2Y+MAp1_2Y+PAp1_2Y+HNp1_2Y)
                elif sec==96:
                    s.sendall(MSp1_2R+MAp1_2R+PAp1_2R+HNp1_2R)
                elif sec==99:
                    s.sendall(MSp1_2G+MAp1_2G+PAp1_2G+HNp1_2G+ERp2_3Y)
                elif sec==102:
                    s.sendall(ERp2_3R)
                elif sec==105:
                    s.sendall(ERp2_3G)
                elif sec==117:
                    s.sendall(HNp2_3Y)
                elif sec==120:
                    s.sendall(HNp2_3R)
                elif sec==123:
                    s.sendall(HNp2_3G)
                elif sec==129:
                    s.sendall(ERp3_4Y)
                elif sec==132:
                    s.sendall(ERp3_4R)
                elif sec==135:
                    s.sendall(ERp3_4G)
                elif sec==144:
                    s.sendall(MSp2_1Y+MAp2_1Y+PAp2_1Y+HNp3_1Y+ERp4_1Y)
                elif sec==147:
                    s.sendall(MSp2_1R+MAp2_1R+PAp2_1R+HNp3_1R+ERp4_1R)

            else:

                ###

                ####每5秒 get state
                '''
                s.sendall(b'simStep 1\r\n'+getState)
                
                
                data = s.recv(8192)
                lst = data.decode('ascii')[:-2].split()
                state = [simTime] + [int(i) for i in lst]
                stateDF.loc[len(stateDF.index)] = state
                    
                print(stateDF)
                #print(stateDF.loc[step -1 , 'simTime'])
                '''
                n_s_ms = []
                ##ms
                n_s_ms.append(stateDF.loc[step, 'laneA0Q'])
                n_s_ms.append(stateDF.loc[step, 'laneA0Q'])
                n_s_ms.append(stateDF.loc[step, 'laneI0Q'])
                n_s_ms.append(stateDF.loc[step, 'laneI1Q'])
                n_s_ms.append(stateDF.loc[step, 'laneU0Q'])
                n_s_ms.append(stateDF.loc[step, 'laneU1Q'])
                n_s_ms.append(stateDF.loc[step, 'laneU2Q'])
                ##mn
                n_s_ms.append(stateDF.loc[step, 'laneB0Q'])
                n_s_ms.append(stateDF.loc[step, 'laneB1Q'])
                n_s_ms.append(stateDF.loc[step, 'laneV0Q'])
                n_s_ms.append(stateDF.loc[step, 'laneV1Q'])
                n_s_ms.append(stateDF.loc[step, 'laneV2Q'])
                n_s_ms.append(stateDF.loc[step, 'laneJ0Q'])

                #finger
                n_s_ms.append(n_p[0])
                n_s_ms.append(n_p[1])
                ###################################################################
                n_s_mn = []
                n_s_mn.append(stateDF.loc[step, 'laneB0Q'])
                n_s_mn.append(stateDF.loc[step, 'laneB1Q'])
                n_s_mn.append(stateDF.loc[step, 'laneV0Q'])
                n_s_mn.append(stateDF.loc[step, 'laneV1Q'])
                n_s_mn.append(stateDF.loc[step, 'laneV2Q'])
                n_s_mn.append(stateDF.loc[step, 'laneJ0Q'])

                n_s_mn.append(stateDF.loc[step, 'laneA0Q'])
                n_s_mn.append(stateDF.loc[step, 'laneA0Q'])
                n_s_mn.append(stateDF.loc[step, 'laneI0Q'])
                n_s_mn.append(stateDF.loc[step, 'laneI1Q'])
                n_s_mn.append(stateDF.loc[step, 'laneU0Q'])
                n_s_mn.append(stateDF.loc[step, 'laneU1Q'])
                n_s_mn.append(stateDF.loc[step, 'laneU2Q'])

                n_s_mn.append(stateDF.loc[step, 'laneC0Q'])
                n_s_mn.append(stateDF.loc[step, 'laneC1Q'])
                n_s_mn.append(stateDF.loc[step, 'laneW0Q'])
                n_s_mn.append(stateDF.loc[step, 'laneW1Q'])
                n_s_mn.append(stateDF.loc[step, 'laneW2Q'])
                n_s_mn.append(stateDF.loc[step, 'laneK0Q'])

                n_s_mn.append(n_p[1])
                n_s_mn.append(n_p[2])
                n_s_mn.append(n_p[0])
                ####################################################################

                n_s_pg = []
                n_s_pg.append(stateDF.loc[step, 'laneC0Q'])
                n_s_pg.append(stateDF.loc[step, 'laneC1Q'])
                n_s_pg.append(stateDF.loc[step, 'laneW0Q'])
                n_s_pg.append(stateDF.loc[step, 'laneW1Q'])
                n_s_pg.append(stateDF.loc[step, 'laneW2Q'])
                n_s_pg.append(stateDF.loc[step, 'laneK0Q'])

                n_s_pg.append(stateDF.loc[step, 'laneD0Q'])
                n_s_pg.append(stateDF.loc[step, 'laneD1Q'])
                n_s_pg.append(stateDF.loc[step, 'laneD2Q'])
                n_s_pg.append(stateDF.loc[step, 'laneX0Q'])
                n_s_pg.append(stateDF.loc[step, 'laneX1Q'])
                n_s_pg.append(stateDF.loc[step, 'laneX2Q'])
                n_s_pg.append(stateDF.loc[step, 'laneL0Q'])
                n_s_pg.append(stateDF.loc[step, 'laneO0Q'])

                n_s_pg.append(stateDF.loc[step, 'laneB0Q'])
                n_s_pg.append(stateDF.loc[step, 'laneB1Q'])
                n_s_pg.append(stateDF.loc[step, 'laneV0Q'])
                n_s_pg.append(stateDF.loc[step, 'laneV1Q'])
                n_s_pg.append(stateDF.loc[step, 'laneV2Q'])
                n_s_pg.append(stateDF.loc[step, 'laneJ0Q'])

                n_s_pg.append(n_p[2])
                n_s_pg.append(n_p[3])
                n_s_pg.append(n_p[1])
                    ####################################################################

                n_s_hn = []
                n_s_hn.append(stateDF.loc[step, 'laneD0Q'])
                n_s_hn.append(stateDF.loc[step, 'laneD1Q'])
                n_s_hn.append(stateDF.loc[step, 'laneD2Q'])
                n_s_hn.append(stateDF.loc[step, 'laneX0Q'])
                n_s_hn.append(stateDF.loc[step, 'laneX1Q'])
                n_s_hn.append(stateDF.loc[step, 'laneX2Q'])
                n_s_hn.append(stateDF.loc[step, 'laneL0Q'])
                n_s_hn.append(stateDF.loc[step, 'laneO0Q'])

                n_s_hn.append(stateDF.loc[step, 'laneE0Q'])
                n_s_hn.append(stateDF.loc[step, 'laneE1Q'])
                n_s_hn.append(stateDF.loc[step, 'laneE2Q'])
                n_s_hn.append(stateDF.loc[step, 'laneE3Q'])
                n_s_hn.append(stateDF.loc[step, 'laneP0Q'])
                n_s_hn.append(stateDF.loc[step, 'laneM0Q'])
                n_s_hn.append(stateDF.loc[step, 'laneN0Q'])
                n_s_hn.append(stateDF.loc[step, 'laneN1Q'])
                    
                n_s_hn.append(stateDF.loc[step, 'laneC0Q'])
                n_s_hn.append(stateDF.loc[step, 'laneC1Q'])
                n_s_hn.append(stateDF.loc[step, 'laneW0Q'])
                n_s_hn.append(stateDF.loc[step, 'laneW1Q'])
                n_s_hn.append(stateDF.loc[step, 'laneW2Q'])
                n_s_hn.append(stateDF.loc[step, 'laneK0Q'])

                n_s_hn.append(n_p[3])
                n_s_hn.append(n_p[4])
                n_s_hn.append(n_p[2])
                    #######################################################################

                n_s_dz = []
                n_s_dz.append(stateDF.loc[step, 'laneE0Q'])
                n_s_dz.append(stateDF.loc[step, 'laneE1Q'])
                n_s_dz.append(stateDF.loc[step, 'laneE2Q'])
                n_s_dz.append(stateDF.loc[step, 'laneE3Q'])
                n_s_dz.append(stateDF.loc[step, 'laneP0Q'])
                n_s_dz.append(stateDF.loc[step, 'laneM0Q'])
                n_s_dz.append(stateDF.loc[step, 'laneN0Q'])
                n_s_dz.append(stateDF.loc[step, 'laneN1Q'])

                n_s_dz.append(stateDF.loc[step, 'laneY0Q'])
                n_s_dz.append(stateDF.loc[step, 'laneY1Q'])
                n_s_dz.append(stateDF.loc[step, 'laneY2Q'])
                n_s_dz.append(stateDF.loc[step, 'laneF0Q'])
                n_s_dz.append(stateDF.loc[step, 'laneF1Q'])
                n_s_dz.append(stateDF.loc[step, 'laneF2Q'])
     
                n_s_dz.append(stateDF.loc[step, 'laneD0Q'])
                n_s_dz.append(stateDF.loc[step, 'laneD1Q'])
                n_s_dz.append(stateDF.loc[step, 'laneD2Q'])
                n_s_dz.append(stateDF.loc[step, 'laneX0Q'])
                n_s_dz.append(stateDF.loc[step, 'laneX1Q'])
                n_s_dz.append(stateDF.loc[step, 'laneX2Q'])
                n_s_dz.append(stateDF.loc[step, 'laneL0Q'])
                n_s_dz.append(stateDF.loc[step, 'laneO0Q'])

                n_s_dz.append(n_p[4])
                n_s_dz.append(n_p[3])

                done = False

                

                fw_ms = ms_policy.forward(n_s_ms, done, 'pv')
                #policy = (fw_ms[0])
                #value = (fw_ms[1])
                fw_mn = mn_policy.forward(n_s_mn, done, 'pv')
                fw_pg = pg_policy.forward(n_s_pg, done, 'pv')
                fw_hn = hn_policy.forward(n_s_hn, done, 'pv')
                fw_dz = dz_policy.forward(n_s_dz, done, 'pv')
                policy = []
                policy.append(np.argmin(fw_ms[0]))
                policy.append(np.argmin(fw_mn[0]))
                policy.append(np.argmin(fw_pg[0]))
                policy.append(np.argmin(fw_hn[0]))
                policy.append(np.argmin(fw_dz[0]))
                print(fw_ms[0])
                print(fw_mn[0])
                print(policy)
                print(n_p)
                simTime, step = update_action(s, policy, n_p, stateDF, simTime, step)
                #print(stateDF)
                print(step)
                print(simTime)
                    ##index  max(0 , -X)

                agent_reward = []
                ms_reward = (stateDF.loc[step , 'laneA0VehOuts'] - stateDF.loc[step - 1, 'laneA0VehOuts'] +
                             stateDF.loc[step , 'laneA1VehOuts'] - stateDF.loc[step - 1, 'laneA1VehOuts'] +
                             stateDF.loc[step , 'laneU0VehOuts'] - stateDF.loc[step - 1, 'laneU0VehOuts'] +
                             stateDF.loc[step , 'laneU1VehOuts'] - stateDF.loc[step - 1, 'laneU1VehOuts'] +
                             stateDF.loc[step , 'laneU2VehOuts'] - stateDF.loc[step - 1, 'laneU2VehOuts'] +
                             stateDF.loc[step , 'laneI0VehOuts'] - stateDF.loc[step - 1, 'laneI0VehOuts'] +
                             stateDF.loc[step , 'laneI1VehOuts'] - stateDF.loc[step - 1, 'laneI1VehOuts'] )
                ms_reward = max(ms_reward, 0)

                mn_reward = (stateDF.loc[step , 'laneB0VehOuts'] - stateDF.loc[step - 1, 'laneB0VehOuts'] +
                             stateDF.loc[step , 'laneB1VehOuts'] - stateDF.loc[step - 1, 'laneB1VehOuts'] +
                             stateDF.loc[step , 'laneV0VehOuts'] - stateDF.loc[step - 1, 'laneV0VehOuts'] +
                             stateDF.loc[step , 'laneV1VehOuts'] - stateDF.loc[step - 1, 'laneV1VehOuts'] +
                             stateDF.loc[step , 'laneV2VehOuts'] - stateDF.loc[step - 1, 'laneV2VehOuts'] +
                             stateDF.loc[step , 'laneJ0VehOuts'] - stateDF.loc[step - 1, 'laneJ0VehOuts'] )
                mn_reward = max(mn_reward, 0)

                pg_reward = (stateDF.loc[step , 'laneC0VehOuts'] - stateDF.loc[step - 1, 'laneC0VehOuts'] +
                             stateDF.loc[step , 'laneC1VehOuts'] - stateDF.loc[step - 1, 'laneC1VehOuts'] +
                             stateDF.loc[step , 'laneW0VehOuts'] - stateDF.loc[step - 1, 'laneW0VehOuts'] +
                             stateDF.loc[step , 'laneW1VehOuts'] - stateDF.loc[step - 1, 'laneW1VehOuts'] +
                             stateDF.loc[step , 'laneW2VehOuts'] - stateDF.loc[step - 1, 'laneW2VehOuts'] +
                             stateDF.loc[step , 'laneK0VehOuts'] - stateDF.loc[step - 1, 'laneK0VehOuts'] )
                pg_reward = max(pg_reward, 0)

                hn_reward = (stateDF.loc[step , 'laneD0VehOuts'] - stateDF.loc[step - 1, 'laneD0VehOuts'] +
                             stateDF.loc[step , 'laneD1VehOuts'] - stateDF.loc[step - 1, 'laneD1VehOuts'] +
                             stateDF.loc[step , 'laneD2VehOuts'] - stateDF.loc[step - 1, 'laneD2VehOuts'] +
                             stateDF.loc[step , 'laneX0VehOuts'] - stateDF.loc[step - 1, 'laneX0VehOuts'] +
                             stateDF.loc[step , 'laneX1VehOuts'] - stateDF.loc[step - 1, 'laneX1VehOuts'] +
                             stateDF.loc[step , 'laneX2VehOuts'] - stateDF.loc[step - 1, 'laneX2VehOuts'] +
                             stateDF.loc[step , 'laneL0VehOuts'] - stateDF.loc[step - 1, 'laneL0VehOuts'] +
                             stateDF.loc[step , 'laneO0VehOuts'] - stateDF.loc[step - 1, 'laneO0VehOuts'] )
                hn_reward = max(hn_reward, 0)

                dz_reward = (stateDF.loc[step , 'laneE0VehOuts'] - stateDF.loc[step - 1, 'laneE0VehOuts'] +
                             stateDF.loc[step , 'laneE1VehOuts'] - stateDF.loc[step - 1, 'laneE1VehOuts'] +
                             stateDF.loc[step , 'laneE2VehOuts'] - stateDF.loc[step - 1, 'laneE2VehOuts'] +
                             stateDF.loc[step , 'laneE3VehOuts'] - stateDF.loc[step - 1, 'laneE3VehOuts'] +
                             stateDF.loc[step , 'laneM0VehOuts'] - stateDF.loc[step - 1, 'laneM0VehOuts'] +
                             stateDF.loc[step , 'laneN0VehOuts'] - stateDF.loc[step - 1, 'laneN0VehOuts'] +
                             stateDF.loc[step , 'laneN1VehOuts'] - stateDF.loc[step - 1, 'laneN1VehOuts'] +
                             stateDF.loc[step , 'laneP0VehOuts'] - stateDF.loc[step - 1, 'laneP0VehOuts'] )
                dz_reward = max(dz_reward, 0)
                agent_reward.append(step)
                agent_reward.append(ms_reward)
                agent_reward.append(mn_reward)
                agent_reward.append(pg_reward)
                agent_reward.append(hn_reward)
                agent_reward.append(dz_reward)
                reward_data.append(agent_reward)
                phase_data.append(n_p)
                print("ms reward: " + str(ms_reward))
                    #ms_ob, ms_reward = get_data()

                ## neightbor reward gamma
    

                nofirst = True 
                print("##############################################################")
                t_r +=  (ms_reward + mn_reward + pg_reward + hn_reward + dz_reward)   

            
        total_reward.append(t_r)
        
        s.sendall(b'restart\r\n')
    
    #reward_data = pd.DataFrame(reward_data, columns = cols).ffill()
    #reward_data.to_csv("reward.csv")
    cols = ["ms", "mn", "pg", "hn", "dz"]
    phase_data = pd.DataFrame(phase_data, columns = cols).ffill()
    phase_data.to_csv("phase.csv")
    print("###########################")
    print(total_reward)
    print("###########################")
    s.sendall(b'bye bye\r\n')
    stateDF.to_csv("stateDFdebug2.txt",sep='\t', header=True, index=True, mode='w', encoding = 'utf-8')
