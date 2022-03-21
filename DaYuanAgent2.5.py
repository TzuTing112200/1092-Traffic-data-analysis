import socket
import pandas as pd
import numpy as np
import datetime as dt
import time

def df_empty(columns, dtypes, index=None):
    df = pd.DataFrame(index=index)
    for c,d in zip(columns, dtypes):
        df[c] = pd.Series(dtype=d)
    return df

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
getTotalVehOuts = b'getTotalVehOuts\n'
repaint = b'repaint\n'
simStep = b'simStep\n'

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
        'laneY2ForkVehOuts', 'laneY2SIForkVehOuts', 'laneY2SIForkVehI2OTT', 'laneY2SIForkVehO2OTT)', 'laneY2TIForkVehOuts', 'laneY2TIForkVehI2OTT', 'laneY2TIForkVehO2OTT', 'laneY2SIForkVehCyclese', 'laneY2TIForkVehCycles', 'laneY2FirstForkVehStoppedTime', 'laneY2FirstForkVehAccCycles',
        'laneI0VehOuts', 'laneI0SIVehOuts', 'laneI0SIVehI2OTT', 'laneI0SIVehO2OTT)', 'laneI0TIVehOuts', 'laneI0TIVehI2OTT', 'laneI0TIVehO2OTT', 'laneI0SIVehCycles', 'laneI0TIVehCycles', 'laneI0FirstVehStoppedTime', 'laneI0FirstVehAccCycles',
        'laneI1VehOuts', 'laneI1SIVehOuts', 'laneI1SIVehI2OTT', 'laneI1SIVehO2OTT)', 'laneI1TIVehOuts', 'laneI1TIVehI2OTT', 'laneI1TIVehO2OTT', 'laneI1SIVehCycles', 'laneI1TIVehCycles', 'laneI1FirstVehStoppedTime', 'laneI1FirstVehAccCycles',
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

T = 150
a = 0    
TSC = [(MSp1_2Y, 48), (MSp1_2R, 51), (MSp1_2G, 54),
       (MSp2_1Y, 144), (MSp2_1R, 147), (MSp2_1G, 0),
       (MAp1_2Y, 102), (MAp1_2R, 105), (MAp1_2G, 108),
       (MAp2_1Y, 144), (MAp2_1R, 147), (MAp2_1G, 0),
       (PAp1_2Y, 96), (PAp1_2R, 99), (PAp1_2G, 102),
       (PAp2_1Y, 144), (PAp2_1R, 147), (PAp2_1G, 0),
       (HNp1_2Y, 90), (HNp1_2R, 93), (HNp1_2G, 96),
       (HNp2_3Y, 108), (HNp2_3R, 111), (HNp2_3G, 114),
       (HNp3_1Y, 144), (HNp3_1R, 147), (HNp3_1G, 0),
       (ERp1_2Y, 84+a), (ERp1_2R, 87+a), (ERp1_2G, 90+a),
       (ERp2_3Y, 99+a), (ERp2_3R, 102+a), (ERp2_3G, 105+a),
       (ERp3_4Y, 129+a), (ERp3_4R, 132+a), (ERp3_4G, 135+a),
       (ERp4_1Y, 144+a), (ERp4_1R, 147+a), (ERp4_1G, (T+a)%T)
       ]    


TSC = [(MSp1_2Y, 48), (MSp1_2R, 51), (MSp1_2G, 54),
       (MSp2_1Y, 144), (MSp2_1R, 147), (MSp2_1G, 0),
       (MAp1_2Y, 102), (MAp1_2R, 105), (MAp1_2G, 108),
       (MAp2_1Y, 144), (MAp2_1R, 147), (MAp2_1G, 0),
       (PAp1_2Y, 96), (PAp1_2R, 99), (PAp1_2G, 102),
       (PAp2_1Y, 144), (PAp2_1R, 147), (PAp2_1G, 0),
       (HNp1_2Y, 90), (HNp1_2R, 93), (HNp1_2G, 96),
       (HNp2_3Y, 105), (HNp2_3R, 108), (HNp2_3G, 111),
       (HNp3_1Y, 141), (HNp3_1R, 144), (HNp3_1G, 147),
       (ERp1_2Y, 69+a), (ERp1_2R, 72+a), (ERp1_2G, 75+a),
       (ERp2_3Y, 81+a), (ERp2_3R, 84+a), (ERp2_3G, 87+a),
       (ERp3_4Y, 108+a), (ERp3_4R, 111+a), (ERp3_4G, 114+a),
       (ERp4_1Y, 123+a), (ERp4_1R, 126+a), (ERp4_1G, (129+a)%T)
       ]

#T = 90
#TSC = [(MSp1_2Y, 33), (MSp1_2R, 36), (MSp1_2G, 39),
#       (MSp2_1Y, 84), (MSp2_1R, 87), (MSp2_1G, 0),
#       (MAp1_2Y, 63), (MAp1_2R, 66), (MAp1_2G, 69),
#       (MAp2_1Y, 84), (MAp2_1R, 87), (MAp2_1G, 0),
#       (PAp1_2Y, 57), (PAp1_2R, 60), (PAp1_2G, 63),
#       (PAp2_1Y, 84), (PAp2_1R, 87), (PAp2_1G, 0),
#       (HNp1_2Y, 42), (HNp1_2R, 45), (HNp1_2G, 48),
#       (HNp2_3Y, 60), (HNp2_3R, 63), (HNp2_3G, 66),
#       (HNp3_1Y, 78), (HNp3_1R, 81), (HNp3_1G, 84),
#       (ERp1_2Y, 18+a), (ERp1_2R, 21+a), (ERp1_2G, 24+a),
#       (ERp2_3Y, 36+a), (ERp2_3R, 39+a), (ERp2_3G, 42+a),
#       (ERp3_4Y, 54+a), (ERp3_4R, 57+a), (ERp3_4G, 60+a),
#       (ERp4_1Y, 72+a), (ERp4_1R, 75+a), (ERp4_1G, (78+a)%T)
#       ]
       
T = 120
TSC = [(MSp1_2Y, 42), (MSp1_2R, 45), (MSp1_2G, 48),
       (MSp2_1Y, 114), (MSp2_1R, 117), (MSp2_1G, 0),
       (MAp1_2Y, 84), (MAp1_2R, 87), (MAp1_2G, 90),
       (MAp2_1Y, 114), (MAp2_1R, 117), (MAp2_1G, 0),
       (PAp1_2Y, 78), (PAp1_2R, 81), (PAp1_2G, 84),
       (PAp2_1Y, 114), (PAp2_1R, 117), (PAp2_1G, 0),
       (HNp1_2Y, 60), (HNp1_2R, 63), (HNp1_2G, 66),
       (HNp2_3Y, 72), (HNp2_3R, 75), (HNp2_3G, 78),
       (HNp3_1Y, 99), (HNp3_1R, 102), (HNp3_1G, 105),
       (ERp1_2Y, 42+a), (ERp1_2R, 45+a), (ERp1_2G, 48+a),
       (ERp2_3Y, 54+a), (ERp2_3R, 57+a), (ERp2_3G, 60+a),
       (ERp3_4Y, 75+a), (ERp3_4R, 78+a), (ERp3_4G, 81+a),
       (ERp4_1Y, 87+a), (ERp4_1R, 90+a), (ERp4_1G, (93+a)%T)
       ]
   
signal = {}
for i in range(0, T, 3):
    signal[i] = b''
    
for t in TSC:
    signal[t[1]] = signal[t[1]]+t[0]
    
stateDF = df_empty(stateAttributes, [int] * len(stateAttributes))

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 9091        # The port used by the server

now = dt.datetime.now()
#current_time = now.strftime("%H:%M:%S")
#print("Current Time =", current_time)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print('connected')
    
    simTime = 0
    while simTime < 3600:   
        s.sendall(b'simStep 3\n'+getState+repaint)
        simTime += 3;
        data = s.recv(8192)
        lst = data.decode('ascii')[:-2].split()
        state = [simTime] + [int(i) for i in lst]
        stateDF.loc[len(stateDF.index)] = state
        
        sec = simTime % T
        if signal[sec] != b'':
            s.sendall(signal[sec])

#        time.sleep(0.1)

    s.sendall(b'getTotalVehOuts\n')
    data = s.recv(8192)
    print('totalVehOuts: '+data.decode('ascii')[:-2])
    s.sendall(b'bye bye\n')
    stateDF.to_csv("stateDF2.txt",sep='\t', header=True, index=True, mode='w', encoding = 'utf-8')

#now = dt.datetime.now()
#current_time = now.strftime("%H:%M:%S")
#print("Current Time =", current_time)