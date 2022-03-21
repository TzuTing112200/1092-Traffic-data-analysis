import socket
import pandas as pd
import numpy as np
import time

def df_empty(columns, dtypes, index=None):
    df = pd.DataFrame(index=index)
    for c,d in zip(columns, dtypes):
        df[c] = pd.Series(dtype=d)
    return df

MSp1 = b'minShengPhase1\r\n'
MAp1 = b'minAnPhase1\r\n'
PAp1 = b'pingAnPhase1\r\n'
HNp1 = b'hengNanPhase1\r\n'
ERp1 = b'eastRampPhase1\r\n'

MSp1Y = b'minShengPhase1Yellow\n'
MAp1Y = b'minAnPhase1Yellow\n'
PAp1Y = b'pingAnPhase1Yellow\n'
HNp1Y = b'hengNanPhase1Yellow\n'
ERp1Y = b'eastRampPhase1Yellow\n'

MSp1R = b'minShengPhase1AllRed\n'
MAp1R = b'minAnPhase1AllRed\n'
PAp1R = b'pingAnPhase1AllRed\n'
HNp1R = b'hengNanPhase1AllRed\n'
ERp1R = b'eastRampPhase1AllRed\n'


MSp2 = b'minShengPhase2\r\n'
MAp2 = b'minAnPhase2\r\n'
PAp2 = b'pingAnPhase2\r\n'
HNp2 = b'hengNanPhase2\r\n'
ERp2 = b'eastRampPhase2\r\n'

MSp2Y = b'minShengPhase2Yellow\n'
MAp2Y = b'minAnPhase2Yellow\n'
PAp2Y = b'pingAnPhase2Yellow\n'
HNp2Y = b'hengNanPhase2Yellow\n'
ERp2Y = b'eastRampPhase2Yellow\n'

MSp2R = b'minShengPhase2AllRed\n'
MAp2R = b'minAnPhase2AllRed\n'
PAp2R = b'pingAnPhase2AllRed\n'
HNp2R = b'hengNanPhase2AllRed\n'
ERp2R = b'eastRampPhase2AllRed\n'

HNp3 = b'hengNanPhase3\r\n'
ERp3 = b'eastRampPhase3\r\n'

HNp3Y = b'hengNanPhase3Yellow\n'
ERp3Y = b'eastRampPhase3Yellow\n'

HNp3R = b'hengNanPhase3AllRed\n'
ERp3R = b'eastRampPhase3AllRed\n'


ERp4 = b'eastRampPhase4\r\n'

ERp4Y = b'eastRampPhase4Yellow\n'

ERp4R = b'eastRampPhase4AllRed\n'

getState = b'getState\r\n'
repaint = b'repaint\r\n'
simStep = b'simStep\r\n'

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

stateDF = df_empty(stateAttributes, [int] * len(stateAttributes))

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 9091        # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print('connected')
    
    simTime = 0
    
    while simTime < 860:
        simTime += 1
        
        if simTime %10 ==0:
            s.sendall(b'simStep 1\r\n'+getState+repaint)
        else:
            s.sendall(b'simStep 1\r\n'+getState+repaint)
        data = s.recv(1024)
        print(data)
        data = s.recv(4096)
        lst = data.decode('ascii')[:-2].split()
        state = [simTime] + [int(i) for i in lst] 
        
        stateDF.loc[len(stateDF.index)] = state
        
        sec = simTime % 30
        if sec==0:
            s.sendall(MSp1+MAp1+PAp1+HNp1+ERp1)
        
        if simTime > 900:
            time.sleep(0.2)
    
    s.sendall(b'bye bye\r\n')
    stateDF.to_csv("stateDFdebug.txt",sep='\t', header=True, index=True, mode='w', encoding = 'utf-8')
