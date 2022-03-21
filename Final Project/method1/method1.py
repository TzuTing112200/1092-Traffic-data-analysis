#!/usr/bin/env python
# coding: utf-8

# In[1]:


import socket
import pandas as pd
import numpy as np
import time
import datetime
from t import *
import random


# In[2]:


HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 9091        # The port used by the server
times = 5000


# In[3]:


routeName = ['minSheng', 'minAn', 'pingAn', 'hengNan', 'eastRamp']

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

#stateDF = df_empty(stateAttributes, [int] * len(stateAttributes))


# In[4]:


def df_empty(columns, dtypes, index=None):
    df = pd.DataFrame(index=index)
    for c,d in zip(columns, dtypes):
        df[c] = pd.Series(dtype=d)
    return df


# In[5]:


base_number = [2, 2, 2, 3, 4]
def update_action(s, policy, phase, last_phase, noChangeTimes, stateDF, simTime, step):
    yellowCommand = bytearray()
    allredCommand = bytearray()
    newphaseCommand = bytearray()
    for i in range(5):
        last_phase[i] = phase[i]
        temp_policy = policy[i] + 1
        
        if temp_policy == phase[i]:
            noChangeTimes[i] += 1;
            continue
            
        else:
            noChangeTimes[i] = 0;

            yellowCommand += '{}P{}_{}Yellow\n'.format(routeName[i], phase[i], temp_policy).encode()
            allredCommand += '{}P{}_{}AllRed\n'.format(routeName[i], phase[i], temp_policy).encode()
            newphaseCommand += '{}P{}_{}Green\n'.format(routeName[i], phase[i], temp_policy).encode()
            phase[i] = temp_policy
        
    #print(yellowCommand)
    #print(allredCommand)
    #print(newphaseCommand)
    for i in range(5): # time
        simTime += 1
        if(i == 4):
            s.sendall(b'simStep 1\r\n'+getState)
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

            s.sendall(b'simStep 1\r\n')
            #print(stateDF.loc[step -1 , 'simTime'])

        
        
      #0 0 1 1 2 2 3 3 4 4| (y) 5 5   6 6 (red) 7 7 8 8 9 9  (green) | (y) 10 10 11 11
        
        
    return simTime, step


# In[6]:


now = datetime.datetime.now()
current_time = now.strftime("%H:%M:%S")
print("Current Time =", current_time)


# In[7]:


ms_policy = init_policy(n_s = 15, n_a = 2, n_w = 0, n_f = 3, agent_name = "ms")
mn_policy = init_policy(n_s = 15, n_a = 2, n_w = 0, n_f = 3, agent_name = "mn")
pg_policy = init_policy(n_s = 15, n_a = 2, n_w = 0, n_f = 3, agent_name = "pg")
hn_policy = init_policy(n_s = 19, n_a = 3, n_w = 0, n_f = 3, agent_name = "hn")
dz_policy = init_policy(n_s = 21, n_a = 4, n_w = 0, n_f = 3, agent_name = "dz")


# In[8]:


max_t_r = 0
last_t_r = 0
cont_t_r = 0

total_reward = []
n_p = [1, 1, 1, 1, 1]
noChangeTimes = [0, 0, 0, 0, 0]
temp_n_p = [1, 1, 1, 1, 1]
step = 0
nofirst = False

cols = ["step", "ms_reward","ms_phase","ms_policy", "mn_reward","mn_phase","mn_policy",
        "pg_reward", "pg_phase","pg_policy", "hn_reward", "hn_phase","hn_policy",
         "dz_reward", "dz_phase", "dz_policy"]
reward_data = []

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print('connected')
    
    for i in range(times): #range(201):
        old_get_reward = 0
        simTime = 0
        t_r = 0
        n_p = [1, 1, 1, 1, 1]
        noChangeTimes = [0, 0, 0, 0, 0]
        temp_n_p = [1, 1, 1, 1, 1]
        policy = [0, 0, 0, 0, 0]
        step = 0
        nofirst = False
        gamma = 0.9
        episod = 0.9
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
                    s.sendall(b'simStep 1\r\n'+getState)
                    data = s.recv(8192)
                    lst = data.decode('ascii')[:-2].split()
                    state = [step] + [int(i) for i in lst]
                    stateDF.loc[len(stateDF.index)] = state
                    s.sendall(MSp2_1G+MAp2_1G+PAp2_1G+HNp3_1G+ERp4_1G)

                else:
                    s.sendall(b'simStep 1\r\n')
            
                sec = simTime % 150
                if sec==0:
                    s.sendall(MSp2_1G + MAp2_1G + PAp2_1G + HNp3_1G + ERp4_1G)
                elif sec==57:
                    s.sendall(ERp1_3Y)
                elif sec==60:
                    s.sendall(ERp1_3R)
                elif sec==63:
                    s.sendall(ERp1_3G)
                elif sec==72:
                    s.sendall(MSp1_2Y + ERp3_2Y + PAp1_2Y + HNp1_2Y)
                elif sec==75:
                    s.sendall(MSp1_2R + ERp3_2R + PAp1_2R + HNp1_2R)
                elif sec==78:
                    s.sendall(MSp1_2G + ERp3_2G + PAp1_2G + HNp1_2G)
                elif sec==84:
                    s.sendall(HNp2_1Y)
                elif sec==87:
                    s.sendall(HNp2_1R)
                elif sec==90:
                    s.sendall(HNp2_1G)
                elif sec==99:
                    s.sendall(MSp2_1Y + MAp1_2Y + ERp2_1Y)
                elif sec==102:
                    s.sendall(MSp2_1R + MAp1_2R + PAp2_1Y + ERp2_1R)
                elif sec==105:
                    s.sendall(MSp2_1G + MAp1_2G + PAp2_1R + ERp2_1G)
                elif sec==108:
                    s.sendall(PAp2_1G)
                elif sec==117:
                    s.sendall(MAp2_1Y + ERp1_3Y)
                elif sec==120:
                    s.sendall(MSp1_2Y + MAp2_1R + ERp1_3R)
                elif sec==123:
                    s.sendall(MSp1_2R + MAp2_1G + HNp1_2Y + ERp1_3G)
                elif sec==126:
                    s.sendall(MSp1_2G + PAp1_2Y + HNp1_2R + ERp3_4Y)
                elif sec==129:
                    s.sendall(PAp1_2R + HNp1_2G + ERp3_4R)
                elif sec==132:
                    s.sendall(PAp1_2G + HNp2_3Y + ERp3_4G)
                elif sec==135:
                    s.sendall(HNp2_3R)
                elif sec==138:
                    s.sendall(HNp2_3G)
                elif sec==144:
                    s.sendall(MSp2_1Y + MAp2_1Y + PAp2_1Y + HNp3_1Y + ERp4_1Y)
                elif sec==147:
                    s.sendall(MSp2_1R + MAp2_1R + PAp2_1R + HNp3_1R + ERp4_1R)

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
                for ii in range(2):
                    if n_p[0] == ii:
                        n_s_ms.append(1)
                    else:
                        n_s_ms.append(0)
                        
                n_s_ms.append(stateDF.loc[step, 'laneA0Q']
                              +stateDF.loc[step, 'laneA1Q']
                              +stateDF.loc[step, 'laneU0Q']
                              +stateDF.loc[step, 'laneU1Q']
                              +stateDF.loc[step, 'laneU2Q'])
                n_s_ms.append(stateDF.loc[step, 'laneI0Q']
                              +stateDF.loc[step, 'laneI1Q']
                              +stateDF.loc[step, 'laneU2Q'])
                
                n_s_ms.append(max(stateDF.loc[step, 'laneA0FirstVehStoppedTime']
                              , stateDF.loc[step, 'laneA1FirstVehStoppedTime']))
                n_s_ms.append(max(stateDF.loc[step, 'laneI0FirstVehStoppedTime']
                              , stateDF.loc[step, 'laneI1FirstVehStoppedTime']))
                n_s_ms.append(max(stateDF.loc[step, 'laneU0FirstVehStoppedTime']
                              , stateDF.loc[step, 'laneU1FirstVehStoppedTime']
                              , stateDF.loc[step, 'laneU2FirstVehStoppedTime']))
                ##mn
                n_s_ms.append(stateDF.loc[step, 'laneB0Q']
                              +stateDF.loc[step, 'laneB1Q'])
                n_s_ms.append(stateDF.loc[step, 'laneV0Q']
                              +stateDF.loc[step, 'laneV1Q']
                              +stateDF.loc[step, 'laneV2Q'])
                # n_s_ms.append(-stateDF.loc[step, 'laneJ0Q'])

                n_s_ms.append(stateDF.loc[step, 'laneC0Q']
                              +stateDF.loc[step, 'laneC1Q'])
                n_s_ms.append(stateDF.loc[step, 'laneW0Q']
                              +stateDF.loc[step, 'laneW1Q']
                              +stateDF.loc[step, 'laneW2Q'])
                # n_s_ms.append(-stateDF.loc[step, 'laneK0Q'])

                #finger
                n_s_ms.append(temp_n_p[0])
                n_s_ms.append(n_p[0])
                n_s_ms.append(n_p[1])
                n_s_ms.append(n_p[2])
                
                n_s_ms.append(noChangeTimes[0])
                n_s_ms.append(noChangeTimes[1])
                n_s_ms.append(noChangeTimes[2])
                ###################################################################
                n_s_mn = []
                
                for ii in range(2):
                    if n_p[1] == ii:
                        n_s_mn.append(1)
                    else:
                        n_s_mn.append(0)
                        
                n_s_mn.append(stateDF.loc[step, 'laneB0Q']
                              +stateDF.loc[step, 'laneB1Q']
                              +stateDF.loc[step, 'laneV0Q']
                              +stateDF.loc[step, 'laneV1Q']
                              +stateDF.loc[step, 'laneV2Q'])
                n_s_mn.append(stateDF.loc[step, 'laneJ0Q'])
                
                n_s_mn.append(max(stateDF.loc[step, 'laneB0FirstVehStoppedTime']
                              , stateDF.loc[step, 'laneB1FirstVehStoppedTime']))
                n_s_mn.append(max(stateDF.loc[step, 'laneV0FirstVehStoppedTime']
                              , stateDF.loc[step, 'laneV1FirstVehStoppedTime']
                              , stateDF.loc[step, 'laneV2FirstVehStoppedTime']))
                n_s_mn.append(stateDF.loc[step, 'laneJ0FirstVehStoppedTime'])

                n_s_mn.append(stateDF.loc[step, 'laneA0Q']
                              +stateDF.loc[step, 'laneA1Q'])
                # n_s_mn.append(-stateDF.loc[step, 'laneI0Q'])
                # n_s_mn.append(-stateDF.loc[step, 'laneI1Q'])
                n_s_mn.append(stateDF.loc[step, 'laneU0Q']
                              +stateDF.loc[step, 'laneU1Q']
                              +stateDF.loc[step, 'laneU2Q'])

                n_s_mn.append(stateDF.loc[step, 'laneC0Q']
                              +stateDF.loc[step, 'laneC1Q'])
                n_s_mn.append(stateDF.loc[step, 'laneW0Q']
                              +stateDF.loc[step, 'laneW1Q']
                              +stateDF.loc[step, 'laneW2Q'])
                # n_s_mn.append(-stateDF.loc[step, 'laneK0Q'])

                n_s_mn.append(temp_n_p[1])
                n_s_mn.append(n_p[1])
                n_s_mn.append(n_p[0])
                n_s_mn.append(n_p[2])
                # n_s_mn.append(n_p[3])
                
                n_s_mn.append(noChangeTimes[1])
                n_s_mn.append(noChangeTimes[0])
                n_s_mn.append(noChangeTimes[2])
                # n_s_mn.append(noChangeTimes[3])
                ####################################################################

                n_s_pg = []
                
                for ii in range(2):
                    if n_p[2] == ii:
                        n_s_pg.append(1)
                    else:
                        n_s_pg.append(0)
                        
                n_s_pg.append(stateDF.loc[step, 'laneC0Q']
                              +stateDF.loc[step, 'laneC1Q']
                              +stateDF.loc[step, 'laneW0Q'])
                n_s_pg.append(stateDF.loc[step, 'laneW1Q']
                              +stateDF.loc[step, 'laneW2Q']
                              +stateDF.loc[step, 'laneK0Q'])
                
                n_s_pg.append(max(stateDF.loc[step, 'laneC0FirstVehStoppedTime']
                              , stateDF.loc[step, 'laneC1FirstVehStoppedTime']))
                n_s_pg.append(max(stateDF.loc[step, 'laneW0FirstVehStoppedTime']
                              , stateDF.loc[step, 'laneW1FirstVehStoppedTime']
                              , stateDF.loc[step, 'laneW2FirstVehStoppedTime']))
                n_s_pg.append(stateDF.loc[step, 'laneK0FirstVehStoppedTime'])

                n_s_pg.append(stateDF.loc[step, 'laneD0Q']
                              +stateDF.loc[step, 'laneD1Q']
                              +stateDF.loc[step, 'laneD2Q'])
                n_s_pg.append(stateDF.loc[step, 'laneX0Q']
                              +stateDF.loc[step, 'laneX1Q']
                              +stateDF.loc[step, 'laneX2Q'])
                # n_s_pg.append(-stateDF.loc[step, 'laneL0Q'])
                # n_s_pg.append(-stateDF.loc[step, 'laneO0Q'])

                n_s_pg.append(stateDF.loc[step, 'laneB0Q']
                              +stateDF.loc[step, 'laneB1Q'])
                n_s_pg.append(stateDF.loc[step, 'laneV0Q']
                              +stateDF.loc[step, 'laneV1Q']
                              +stateDF.loc[step, 'laneV2Q'])
                # n_s_pg.append(-stateDF.loc[step, 'laneJ0Q'])

                n_s_pg.append(temp_n_p[2])
                n_s_pg.append(n_p[2])
                n_s_pg.append(n_p[1])
                # n_s_pg.append(n_p[0])
                n_s_pg.append(n_p[3])
                # n_s_pg.append(n_p[4])
                
                n_s_pg.append(noChangeTimes[2])
                n_s_pg.append(noChangeTimes[1])
                # n_s_pg.append(noChangeTimes[0])
                n_s_pg.append(noChangeTimes[3])
                # n_s_pg.append(noChangeTimes[4])
                    ####################################################################

                n_s_hn = []
                
                for ii in range(3):
                    if n_p[3] == ii:
                        n_s_hn.append(1)
                    else:
                        n_s_hn.append(0)
                        
                n_s_hn.append(stateDF.loc[step, 'laneD0Q']
                              +stateDF.loc[step, 'laneD1Q']
                              +stateDF.loc[step, 'laneD2Q']
                              +stateDF.loc[step, 'laneX1Q']
                              +stateDF.loc[step, 'laneX2Q'])
                n_s_hn.append(stateDF.loc[step, 'laneX0Q']
                              +stateDF.loc[step, 'laneO0Q'])
                n_s_hn.append(stateDF.loc[step, 'laneL0Q']
                              +stateDF.loc[step, 'laneO0Q'])
                
                n_s_hn.append(max(stateDF.loc[step, 'laneD0FirstVehStoppedTime']
                              , stateDF.loc[step, 'laneD1FirstVehStoppedTime']
                              , stateDF.loc[step, 'laneD2FirstVehStoppedTime']))
                n_s_hn.append(max(stateDF.loc[step, 'laneX0FirstVehStoppedTime']
                              , stateDF.loc[step, 'laneX1FirstVehStoppedTime']))
                n_s_hn.append(stateDF.loc[step, 'laneX2FirstVehStoppedTime'])
                n_s_hn.append(stateDF.loc[step, 'laneL0FirstVehStoppedTime'])
                n_s_hn.append(stateDF.loc[step, 'laneO0FirstVehStoppedTime'])

                n_s_hn.append(stateDF.loc[step, 'laneE0Q']
                              +stateDF.loc[step, 'laneE1Q']
                              +stateDF.loc[step, 'laneE2Q']
                              +stateDF.loc[step, 'laneE3Q'])
                n_s_hn.append(stateDF.loc[step, 'laneY0Q']
                              +stateDF.loc[step, 'laneY1Q']
                              +stateDF.loc[step, 'laneY2Q'])
                # n_s_hn.append(-stateDF.loc[step, 'laneP0Q'])
                # n_s_hn.append(-stateDF.loc[step, 'laneM0Q'])
                # n_s_hn.append(-stateDF.loc[step, 'laneN0Q'])
                # n_s_hn.append(-stateDF.loc[step, 'laneN1Q'])
                    
                n_s_hn.append(stateDF.loc[step, 'laneC0Q']
                              +stateDF.loc[step, 'laneC1Q'])
                n_s_hn.append(stateDF.loc[step, 'laneW0Q']
                              +stateDF.loc[step, 'laneW1Q']
                              +stateDF.loc[step, 'laneW2Q'])
                # n_s_hn.append(-stateDF.loc[step, 'laneK0Q'])

                n_s_hn.append(temp_n_p[3])
                n_s_hn.append(n_p[3])
                n_s_hn.append(n_p[2])
                # n_s_hn.append(n_p[1])
                n_s_hn.append(n_p[4])

                n_s_hn.append(noChangeTimes[3])
                n_s_hn.append(noChangeTimes[2])
                # n_s_hn.append(noChangeTimes[1])
                n_s_hn.append(noChangeTimes[4])
                    #######################################################################

                n_s_dz = []
                
                for ii in range(4):
                    if n_p[4] == ii:
                        n_s_dz.append(1)
                    else:
                        n_s_dz.append(0)
                        
                n_s_dz.append(stateDF.loc[step, 'laneE0Q']
                              +stateDF.loc[step, 'laneE1Q']
                              +stateDF.loc[step, 'laneE2Q']
                              +stateDF.loc[step, 'laneE3Q']
                              +stateDF.loc[step, 'laneY1Q']
                              +stateDF.loc[step, 'laneY2Q'])
                n_s_dz.append(stateDF.loc[step, 'laneY0Q']
                              +stateDF.loc[step, 'laneY1Q']
                              +stateDF.loc[step, 'laneY2Q'])
                n_s_dz.append(stateDF.loc[step, 'laneP0Q']
                              +stateDF.loc[step, 'laneN0Q']
                              +stateDF.loc[step, 'laneN1Q'])
                n_s_dz.append(stateDF.loc[step, 'laneM0Q'])
                
                n_s_dz.append(max(stateDF.loc[step, 'laneE0FirstVehStoppedTime']
                              , stateDF.loc[step, 'laneE1FirstVehStoppedTime']
                              , stateDF.loc[step, 'laneE2FirstVehStoppedTime']
                              , stateDF.loc[step, 'laneE3FirstVehStoppedTime']))
                n_s_dz.append(max(stateDF.loc[step, 'laneY0FirstVehStoppedTime']
                              , stateDF.loc[step, 'laneY1FirstVehStoppedTime']
                              , stateDF.loc[step, 'laneY2FirstVehStoppedTime']))
                n_s_dz.append(stateDF.loc[step, 'laneP0FirstVehStoppedTime'])
                n_s_dz.append(stateDF.loc[step, 'laneM0FirstVehStoppedTime'])
                n_s_dz.append(max(stateDF.loc[step, 'laneN0FirstVehStoppedTime']
                              , stateDF.loc[step, 'laneN1FirstVehStoppedTime']))
     
                n_s_dz.append(stateDF.loc[step, 'laneD0Q']
                              +stateDF.loc[step, 'laneD1Q']
                              +stateDF.loc[step, 'laneD2Q'])
                n_s_dz.append(stateDF.loc[step, 'laneX0Q']
                              +stateDF.loc[step, 'laneX1Q']
                              +stateDF.loc[step, 'laneX2Q'])
                # n_s_dz.append(-stateDF.loc[step, 'laneL0Q'])
                # n_s_dz.append(-stateDF.loc[step, 'laneO0Q'])
                
                n_s_dz.append(stateDF.loc[step, 'laneC0Q']
                              +stateDF.loc[step, 'laneC1Q'])
                n_s_dz.append(stateDF.loc[step, 'laneW0Q']
                              +stateDF.loc[step, 'laneW1Q']
                              +stateDF.loc[step, 'laneW2Q'])
                # n_s_dz.append(-stateDF.loc[step, 'laneK0Q'])

                n_s_dz.append(temp_n_p[4])
                n_s_dz.append(n_p[4])
                n_s_dz.append(n_p[3])
                n_s_dz.append(n_p[2])

                n_s_dz.append(noChangeTimes[4])
                n_s_dz.append(noChangeTimes[3])
                n_s_dz.append(noChangeTimes[2])

                done = False

                if((step % 40 == 0) & (nofirst)):

                    #print("start backward")
                    ms_R = ms_policy.forward(n_s_ms, False, 'v')
                    ms_policy.backward(ms_R)
                    mn_R = mn_policy.forward(n_s_mn, False, 'v')
                    mn_policy.backward(mn_R)
                    pg_R = pg_policy.forward(n_s_pg, False, 'v')
                    pg_policy.backward(pg_R)
                    hn_R = hn_policy.forward(n_s_hn, False, 'v')
                    hn_policy.backward(hn_R)
                    dz_R = dz_policy.forward(n_s_dz, False, 'v')
                    dz_policy.backward(dz_R)

                fw_ms = ms_policy.forward(n_s_ms, done, 'pv')
                fw_mn = mn_policy.forward(n_s_mn, done, 'pv')
                fw_pg = pg_policy.forward(n_s_pg, done, 'pv')
                fw_hn = hn_policy.forward(n_s_hn, done, 'pv')
                fw_dz = dz_policy.forward(n_s_dz, done, 'pv')
                # print(fw_ms)
                # print(fw_mn)
                # print(fw_pg)
                # print(fw_hn)
                # print(fw_dz)
                # input()
                
                old_policy = []
                old_policy = policy
                policy = []
                
                '''
                episod = [0, 1]
                p1 = [0, 1]

                random_ms = random.choices(episod, weights=[90, 10])
                #print(random_ms)
                if(random_ms == 1):
                    p = random.choices(p1, weights=[50, 50])
                    policy.append(p)
                else:
                    policy.append(np.argmax(fw_ms[0]))

                random_mn = random.choices(episod, weights=[90, 10])
                if(random_mn == 1):
                    p = random.choices(p1, weights=[50, 50])
                    policy.append(p)
                else:
                    policy.append(np.argmax(fw_mn[0]))

                random_pg = random.choices(episod, weights=[90, 10])
                if(random_pg == 1):
                    p = random.choices(p1, weights=[50, 50])
                    policy.append(p)
                else:
                    policy.append(np.argmax(fw_pg[0]))

                random_hn = random.choices(episod, weights=[90, 10])
                if(random_hn == 1):
                    p = random.choices(p1, weights=[50, 50])
                    policy.append(p)
                else:
                    policy.append(np.argmax(fw_hn[0]))

                random_dz = random.choices(episod, weights=[90, 10])
                if(random_dz == 1):
                    p = random.choices(p1, weights=[50, 50])
                    policy.append(p)
                else:
                    policy.append(np.argmax(fw_dz[0]))
                '''
                
                exploration = 0.1
                random.random()
                p1 = [0, 1]
                p2 = [0, 1, 2]
                p3 = [0, 1, 2, 3]

                #print(random_ms)
                if noChangeTimes[0] < 3 or noChangeTimes[1] < 3 or noChangeTimes[2] < 3                or noChangeTimes[3] < 3 or noChangeTimes[4] < 3 :
                    policy = old_policy
                elif(noChangeTimes[0] > 6 and old_policy[0] != 0) or (noChangeTimes[0] < 18 and old_policy[0] == 0)                 or (noChangeTimes[1] > 6 and old_policy[1] != 0) or (noChangeTimes[1] < 18 and old_policy[1] == 0)                 or (noChangeTimes[2] > 6 and old_policy[2] != 0) or (noChangeTimes[2] < 18 and old_policy[2] == 0)                 or (noChangeTimes[3] > 6 and old_policy[3] != 0) or (noChangeTimes[3] < 18 and old_policy[3] == 0)                 or (noChangeTimes[4] > 6 and old_policy[4] not in [0, 2]) or (noChangeTimes[4] < 18 and old_policy[4] in [0, 2]):
                    policy = [0, 0, 0, 0]
                    
                    if old_policy[4] in [0, 2]:
                        policy.append(old_policy[4])
                    else:
                        p = np.argmax(fw_dz[0])
                        if p in [0, 2]:
                            policy.append(p)
                        else:
                            policy.append(0)
                else:
                    p = [0, 0, 0, 0, 0]
                    vote = [0, 0]
                    p[0] = np.argmax(fw_ms[0])
                    p[1] = np.argmax(fw_mn[0])
                    p[2] = np.argmax(fw_pg[0])
                    p[3] = np.argmax(fw_hn[0])
                    p[4] = np.argmax(fw_dz[0])
                    
                    for pp in [p[0], p[1], p[2], p[3]]:
                        if pp == 0:
                            vote[0] += 1
                        else:
                            vote[1] += 1
                            
                    if p[4] in [0, 2]:
                        vote[0] += 1
                    else:
                        vote[1] += 1
                            
                    if vote[0] > vote [1]:
                        policy = [0, 0, 0, 0]
                        
                        if p[4] in [0, 2]:
                            policy.append(p[4])
                        else:
                            policy.append(0)
                    else:
                        policy = [1, 1, 1]
                        
                        if p[3] == 0:
                            policy.append(1)
                        else: policy.append(p[3])
                            
                        
                        if p[4] not in [0, 2]:
                            policy.append(p[4])
                        else:
                            policy.append(3)
                    
                #print(policy)
                '''
                policy.append(np.argmax(fw_ms[0]))
                policy.append(np.argmax(fw_mn[0]))
                policy.append(np.argmax(fw_pg[0]))
                policy.append(np.argmax(fw_hn[0]))
                policy.append(np.argmax(fw_dz[0]))
                '''
                old_p = []
                old_p.append(n_p[0])
                old_p.append(n_p[1])
                old_p.append(n_p[2])
                old_p.append(n_p[3])
                old_p.append(n_p[4])
                
                v = []
                ##Q value
                '''
                v.append(fw_ms[1])
                v.append(fw_mn[1])
                v.append(fw_pg[1])
                v.append(fw_hn[1])
                v.append(fw_dz[1])
                '''
                #print(policy)
                simTime, step = update_action(s, policy, n_p, temp_n_p, noChangeTimes, stateDF, simTime, step)
                #print(n_p)
                #print(v)
                #print("########")
                #print(stateDF)
                #print(step)
                #print(simTime)
                    ##index  max(0 , -X)

                weight = [0, 0, 0, 0, 0]
                
                agent_reward = []
                ms_reward = (stateDF.loc[step , 'laneA0VehOuts'] + # stateDF.loc[step , 'laneA0SIVehOuts'] + # - stateDF.loc[step - 1, 'laneA0VehOuts'] +
                             stateDF.loc[step , 'laneA1VehOuts'] + # stateDF.loc[step , 'laneA1SIVehOuts'] + # - stateDF.loc[step - 1, 'laneA1VehOuts'] +
                             stateDF.loc[step , 'laneU0VehOuts'] + # stateDF.loc[step , 'laneU0SIVehOuts'] + # - stateDF.loc[step - 1, 'laneU0VehOuts'] +
                             stateDF.loc[step , 'laneU1VehOuts'] + # stateDF.loc[step , 'laneU1SIVehOuts'] + # - stateDF.loc[step - 1, 'laneU1VehOuts'] +
                             stateDF.loc[step , 'laneU2VehOuts'] + # stateDF.loc[step , 'laneU2SIVehOuts'] + # - stateDF.loc[step - 1, 'laneU2VehOuts'] +
                             stateDF.loc[step , 'laneI0VehOuts'] + # - stateDF.loc[step - 1, 'laneI0VehOuts'] +
                             stateDF.loc[step , 'laneI1VehOuts']) # - stateDF.loc[step - 1, 'laneI1VehOuts'] )
                weight[0] += stateDF.loc[step , 'laneI0VehOuts']
                weight[0] += stateDF.loc[step , 'laneI1VehOuts']
                
                mn_reward = (stateDF.loc[step , 'laneB0VehOuts'] + # stateDF.loc[step , 'laneB0SIVehOuts'] + # - stateDF.loc[step - 1, 'laneB0VehOuts'] +
                             stateDF.loc[step , 'laneB1VehOuts'] + # stateDF.loc[step , 'laneB1SIVehOuts'] + # - stateDF.loc[step - 1, 'laneB1VehOuts'] +
                             stateDF.loc[step , 'laneV0VehOuts'] + # stateDF.loc[step , 'laneV0SIVehOuts'] + # - stateDF.loc[step - 1, 'laneV0VehOuts'] +
                             stateDF.loc[step , 'laneV1VehOuts'] + # stateDF.loc[step , 'laneV1SIVehOuts'] + # - stateDF.loc[step - 1, 'laneV1VehOuts'] +
                             stateDF.loc[step , 'laneV2VehOuts'] + # stateDF.loc[step , 'laneV2SIVehOuts'] + # - stateDF.loc[step - 1, 'laneV2VehOuts'] +
                             stateDF.loc[step , 'laneJ0VehOuts']) # - stateDF.loc[step - 1, 'laneJ0VehOuts'] )
                weight[1] += stateDF.loc[step , 'laneJ0VehOuts']
                
                pg_reward = (stateDF.loc[step , 'laneC0VehOuts'] + # stateDF.loc[step , 'laneC0SIVehOuts'] + # - stateDF.loc[step - 1, 'laneC0VehOuts'] +
                             stateDF.loc[step , 'laneC1VehOuts'] + # stateDF.loc[step , 'laneC1SIVehOuts'] + # - stateDF.loc[step - 1, 'laneC1VehOuts'] +
                             stateDF.loc[step , 'laneW0VehOuts'] + # stateDF.loc[step , 'laneW0SIVehOuts'] + # - stateDF.loc[step - 1, 'laneW0VehOuts'] +
                             stateDF.loc[step , 'laneW1VehOuts'] + # stateDF.loc[step , 'laneW1SIVehOuts'] + # - stateDF.loc[step - 1, 'laneW1VehOuts'] +
                             stateDF.loc[step , 'laneW2VehOuts'] + # stateDF.loc[step , 'laneW2SIVehOuts'] + # - stateDF.loc[step - 1, 'laneW2VehOuts'] +
                             stateDF.loc[step , 'laneK0VehOuts']) # - stateDF.loc[step - 1, 'laneK0VehOuts'] )
                weight[2] += stateDF.loc[step , 'laneK0VehOuts']

                hn_reward = (stateDF.loc[step , 'laneD0VehOuts'] + # stateDF.loc[step , 'laneD0SIVehOuts'] + # - stateDF.loc[step - 1, 'laneD0VehOuts'] +
                             stateDF.loc[step , 'laneD1VehOuts'] + # stateDF.loc[step , 'laneD1SIVehOuts'] + # - stateDF.loc[step - 1, 'laneD1VehOuts'] +
                             stateDF.loc[step , 'laneD2VehOuts'] + # stateDF.loc[step , 'laneD2SIVehOuts'] + # - stateDF.loc[step - 1, 'laneD2VehOuts'] +
                             stateDF.loc[step , 'laneX0VehOuts'] + # stateDF.loc[step , 'laneX0SIVehOuts'] + # - stateDF.loc[step - 1, 'laneX0VehOuts'] +
                             stateDF.loc[step , 'laneX1VehOuts'] + # stateDF.loc[step , 'laneX1SIVehOuts'] + # - stateDF.loc[step - 1, 'laneX1VehOuts'] +
                             stateDF.loc[step , 'laneX2VehOuts'] + # stateDF.loc[step , 'laneX2SIVehOuts'] + # - stateDF.loc[step - 1, 'laneX2VehOuts'] +
                             stateDF.loc[step , 'laneL0VehOuts']+ # - stateDF.loc[step - 1, 'laneL0VehOuts'] +
                             stateDF.loc[step , 'laneO0VehOuts']) # - stateDF.loc[step - 1, 'laneO0VehOuts'] )
                weight[3] += stateDF.loc[step , 'laneL0VehOuts']
                weight[3] += stateDF.loc[step , 'laneO0VehOuts']

                dz_reward = (stateDF.loc[step , 'laneE0VehOuts'] + # stateDF.loc[step , 'laneE0SIVehOuts'] + # - stateDF.loc[step - 1, 'laneE0VehOuts'] +
                             stateDF.loc[step , 'laneE1VehOuts'] + # stateDF.loc[step , 'laneE1SIVehOuts'] + # - stateDF.loc[step - 1, 'laneE1VehOuts'] +
                             stateDF.loc[step , 'laneE2VehOuts'] + # stateDF.loc[step , 'laneE2SIVehOuts'] + # - stateDF.loc[step - 1, 'laneE2VehOuts'] +
                             stateDF.loc[step , 'laneE3VehOuts'] + # stateDF.loc[step , 'laneE3SIVehOuts'] + # - stateDF.loc[step - 1, 'laneE3VehOuts'] +
                             stateDF.loc[step , 'laneY0VehOuts'] + # stateDF.loc[step , 'laneY0SIVehOuts'] + # - stateDF.loc[step - 1, 'laneY0VehOuts'] +
                             stateDF.loc[step , 'laneY1VehOuts'] + # stateDF.loc[step , 'laneY1SIVehOuts'] + # - stateDF.loc[step - 1, 'laneY1VehOuts'] +
                             stateDF.loc[step , 'laneY2VehOuts'] + # stateDF.loc[step , 'laneY2SIVehOuts'] + # - stateDF.loc[step - 1, 'laneY2VehOuts'] +
                             stateDF.loc[step , 'laneM0VehOuts'] + # - stateDF.loc[step - 1, 'laneM0VehOuts'] +
                             stateDF.loc[step , 'laneN0VehOuts'] + # - stateDF.loc[step - 1, 'laneN0VehOuts'] +
                             stateDF.loc[step , 'laneN1VehOuts'] + # - stateDF.loc[step - 1, 'laneN1VehOuts'] +
                             stateDF.loc[step , 'laneP0VehOuts']) # - stateDF.loc[step - 1, 'laneP0VehOuts'] )
                weight[4] += stateDF.loc[step , 'laneM0VehOuts']
                weight[4] += stateDF.loc[step , 'laneN0VehOuts']
                weight[4] += stateDF.loc[step , 'laneN1VehOuts']
                weight[4] += stateDF.loc[step , 'laneP0VehOuts']
                '''
                ms_punish = (stateDF.loc[step , 'laneA0FirstVehStoppedTime'] * stateDF.loc[step , 'laneA0Q'] - stateDF.loc[step - 1, 'laneA0FirstVehStoppedTime'] * stateDF.loc[step - 1, 'laneA0Q'] +
                             stateDF.loc[step , 'laneA1FirstVehStoppedTime'] * stateDF.loc[step , 'laneA1Q'] - stateDF.loc[step - 1, 'laneA1FirstVehStoppedTime'] * stateDF.loc[step - 1, 'laneA1Q'] +
                             stateDF.loc[step , 'laneU0FirstVehStoppedTime'] * stateDF.loc[step , 'laneU0Q'] - stateDF.loc[step - 1, 'laneU0FirstVehStoppedTime'] * stateDF.loc[step - 1, 'laneU0Q'] +
                             stateDF.loc[step , 'laneU1FirstVehStoppedTime'] * stateDF.loc[step , 'laneU1Q'] - stateDF.loc[step - 1, 'laneU1FirstVehStoppedTime'] * stateDF.loc[step - 1, 'laneU1Q'] +
                             stateDF.loc[step , 'laneU2FirstVehStoppedTime'] * stateDF.loc[step , 'laneU2Q'] - stateDF.loc[step - 1, 'laneU2FirstVehStoppedTime'] * stateDF.loc[step - 1, 'laneU2Q'] +
                             stateDF.loc[step , 'laneI0FirstVehStoppedTime'] * stateDF.loc[step , 'laneI0Q'] + # - stateDF.loc[step - 1, 'laneI0FirstVehStoppedTime'] * stateDF.loc[step - 1, 'laneI0Q'] +
                             stateDF.loc[step , 'laneI1FirstVehStoppedTime'] * stateDF.loc[step , 'laneI1Q'] ) # - stateDF.loc[step - 1, 'laneI1FirstVehStoppedTime'] * stateDF.loc[step - 1, 'laneI1Q'] )

                mn_punish = (stateDF.loc[step , 'laneB0FirstVehStoppedTime'] * stateDF.loc[step , 'laneB0Q'] - stateDF.loc[step - 1, 'laneB0FirstVehStoppedTime'] * stateDF.loc[step - 1, 'laneB0Q'] +
                             stateDF.loc[step , 'laneB1FirstVehStoppedTime'] * stateDF.loc[step , 'laneB1Q'] - stateDF.loc[step - 1, 'laneB1FirstVehStoppedTime'] * stateDF.loc[step - 1, 'laneB1Q'] +
                             stateDF.loc[step , 'laneV0FirstVehStoppedTime'] * stateDF.loc[step , 'laneV0Q'] - stateDF.loc[step - 1, 'laneV0FirstVehStoppedTime'] * stateDF.loc[step - 1, 'laneV0Q'] +
                             stateDF.loc[step , 'laneV1FirstVehStoppedTime'] * stateDF.loc[step , 'laneV1Q'] - stateDF.loc[step - 1, 'laneV1FirstVehStoppedTime'] * stateDF.loc[step - 1, 'laneV1Q'] +
                             stateDF.loc[step , 'laneV2FirstVehStoppedTime'] * stateDF.loc[step , 'laneV2Q'] - stateDF.loc[step - 1, 'laneV2FirstVehStoppedTime'] * stateDF.loc[step - 1, 'laneV2Q'] +
                             stateDF.loc[step , 'laneJ0FirstVehStoppedTime'] * stateDF.loc[step , 'laneJ0Q'] ) # - stateDF.loc[step - 1, 'laneJ0FirstVehStoppedTime'] * stateDF.loc[step - 1, 'laneJ0Q'] )

                pg_punish = (stateDF.loc[step , 'laneC0FirstVehStoppedTime'] * stateDF.loc[step , 'laneC0Q'] - stateDF.loc[step - 1, 'laneC0FirstVehStoppedTime'] * stateDF.loc[step - 1, 'laneC0Q'] +
                             stateDF.loc[step , 'laneC1FirstVehStoppedTime'] * stateDF.loc[step , 'laneC1Q'] - stateDF.loc[step - 1, 'laneC1FirstVehStoppedTime'] * stateDF.loc[step - 1, 'laneC1Q'] +
                             stateDF.loc[step , 'laneW0FirstVehStoppedTime'] * stateDF.loc[step , 'laneW0Q'] - stateDF.loc[step - 1, 'laneW0FirstVehStoppedTime'] * stateDF.loc[step - 1, 'laneW0Q'] +
                             stateDF.loc[step , 'laneW1FirstVehStoppedTime'] * stateDF.loc[step , 'laneW1Q'] - stateDF.loc[step - 1, 'laneW1FirstVehStoppedTime'] * stateDF.loc[step - 1, 'laneW1Q'] +
                             stateDF.loc[step , 'laneW2FirstVehStoppedTime'] * stateDF.loc[step , 'laneW2Q'] - stateDF.loc[step - 1, 'laneW2FirstVehStoppedTime'] * stateDF.loc[step - 1, 'laneW2Q'] +
                             stateDF.loc[step , 'laneK0FirstVehStoppedTime'] * stateDF.loc[step , 'laneK0Q'] ) # - stateDF.loc[step - 1, 'laneK0FirstVehStoppedTime'] * stateDF.loc[step - 1, 'laneK0Q'] )

                hn_punish = (stateDF.loc[step , 'laneD0FirstVehStoppedTime'] * stateDF.loc[step , 'laneD0Q'] - stateDF.loc[step - 1, 'laneD0FirstVehStoppedTime'] * stateDF.loc[step - 1, 'laneD0Q'] +
                             stateDF.loc[step , 'laneD1FirstVehStoppedTime'] * stateDF.loc[step , 'laneD1Q'] - stateDF.loc[step - 1, 'laneD1FirstVehStoppedTime'] * stateDF.loc[step - 1, 'laneD1Q'] +
                             stateDF.loc[step , 'laneD2FirstVehStoppedTime'] * stateDF.loc[step , 'laneD2Q'] - stateDF.loc[step - 1, 'laneD2FirstVehStoppedTime'] * stateDF.loc[step - 1, 'laneD2Q'] +
                             stateDF.loc[step , 'laneX0FirstVehStoppedTime'] * stateDF.loc[step , 'laneX0Q'] - stateDF.loc[step - 1, 'laneX0FirstVehStoppedTime'] * stateDF.loc[step - 1, 'laneX0Q'] +
                             stateDF.loc[step , 'laneX1FirstVehStoppedTime'] * stateDF.loc[step , 'laneX1Q'] - stateDF.loc[step - 1, 'laneX1FirstVehStoppedTime'] * stateDF.loc[step - 1, 'laneX1Q'] +
                             stateDF.loc[step , 'laneX2FirstVehStoppedTime'] * stateDF.loc[step , 'laneX2Q'] - stateDF.loc[step - 1, 'laneX2FirstVehStoppedTime'] * stateDF.loc[step - 1, 'laneX2Q'] +
                             stateDF.loc[step , 'laneL0FirstVehStoppedTime'] * stateDF.loc[step , 'laneL0Q'] + # - stateDF.loc[step - 1, 'laneL0FirstVehStoppedTime'] * stateDF.loc[step - 1, 'laneL0Q'] +
                             stateDF.loc[step , 'laneO0FirstVehStoppedTime'] * stateDF.loc[step , 'laneO0Q'] ) # - stateDF.loc[step - 1, 'laneO0FirstVehStoppedTime'] * stateDF.loc[step - 1, 'laneO0Q'] )

                dz_punish = (stateDF.loc[step , 'laneE0FirstVehStoppedTime'] * stateDF.loc[step , 'laneE0Q'] - stateDF.loc[step - 1, 'laneE0FirstVehStoppedTime'] * stateDF.loc[step - 1, 'laneE0Q'] +
                             stateDF.loc[step , 'laneE1FirstVehStoppedTime'] * stateDF.loc[step , 'laneE1Q'] - stateDF.loc[step - 1, 'laneE1FirstVehStoppedTime'] * stateDF.loc[step - 1, 'laneE1Q'] +
                             stateDF.loc[step , 'laneE2FirstVehStoppedTime'] * stateDF.loc[step , 'laneE2Q'] - stateDF.loc[step - 1, 'laneE2FirstVehStoppedTime'] * stateDF.loc[step - 1, 'laneE2Q'] +
                             stateDF.loc[step , 'laneE3FirstVehStoppedTime'] * stateDF.loc[step , 'laneE3Q'] - stateDF.loc[step - 1, 'laneE3FirstVehStoppedTime'] * stateDF.loc[step - 1, 'laneE3Q'] +
                             stateDF.loc[step , 'laneY0FirstVehStoppedTime'] * stateDF.loc[step , 'laneY0Q'] - stateDF.loc[step - 1, 'laneY0FirstVehStoppedTime'] * stateDF.loc[step - 1, 'laneY0Q'] +
                             stateDF.loc[step , 'laneY1FirstVehStoppedTime'] * stateDF.loc[step , 'laneY1Q'] - stateDF.loc[step - 1, 'laneY1FirstVehStoppedTime'] * stateDF.loc[step - 1, 'laneY1Q'] +
                             stateDF.loc[step , 'laneY2FirstVehStoppedTime'] * stateDF.loc[step , 'laneY2Q'] - stateDF.loc[step - 1, 'laneY2FirstVehStoppedTime'] * stateDF.loc[step - 1, 'laneY2Q'] +
                             stateDF.loc[step , 'laneM0FirstVehStoppedTime'] * stateDF.loc[step , 'laneM0Q'] + # - stateDF.loc[step - 1, 'laneM0FirstVehStoppedTime'] * stateDF.loc[step - 1, 'laneM0Q'] +
                             stateDF.loc[step , 'laneN0FirstVehStoppedTime'] * stateDF.loc[step , 'laneN0Q'] + # - stateDF.loc[step - 1, 'laneN0FirstVehStoppedTime'] * stateDF.loc[step - 1, 'laneN0Q'] +
                             stateDF.loc[step , 'laneN1FirstVehStoppedTime'] * stateDF.loc[step , 'laneN1Q'] + # - stateDF.loc[step - 1, 'laneN1FirstVehStoppedTime'] * stateDF.loc[step - 1, 'laneN1Q'] +
                             stateDF.loc[step , 'laneP0FirstVehStoppedTime'] * stateDF.loc[step , 'laneP0Q'] ) # - stateDF.loc[step - 1, 'laneP0FirstVehStoppedTime'] * stateDF.loc[step - 1, 'laneP0Q'] )
                '''
                ms_punish = (max(stateDF.loc[step , 'laneA0FirstVehStoppedTime'] # , stateDF.loc[step , 'laneA0SIFirstVehStoppedTime'] # - , stateDF.loc[step - 1, 'laneA0FirstVehStoppedTime']
                             , stateDF.loc[step , 'laneA1FirstVehStoppedTime'] # , stateDF.loc[step , 'laneA1SIFirstVehStoppedTime'] # - , stateDF.loc[step - 1, 'laneA1FirstVehStoppedTime']
                             , stateDF.loc[step , 'laneU0FirstVehStoppedTime'] # , stateDF.loc[step , 'laneU0SIFirstVehStoppedTime'] # - , stateDF.loc[step - 1, 'laneU0FirstVehStoppedTime']
                             , stateDF.loc[step , 'laneU1FirstVehStoppedTime'] # , stateDF.loc[step , 'laneU1SIFirstVehStoppedTime'] # - , stateDF.loc[step - 1, 'laneU1FirstVehStoppedTime']
                             , stateDF.loc[step , 'laneU2FirstVehStoppedTime']) * 1 +  # , stateDF.loc[step , 'laneU2SIFirstVehStoppedTime'] # - , stateDF.loc[step - 1, 'laneU2FirstVehStoppedTime']
                             max(stateDF.loc[step , 'laneI0FirstVehStoppedTime'] # - , stateDF.loc[step - 1, 'laneI0FirstVehStoppedTime']
                             , stateDF.loc[step , 'laneI1FirstVehStoppedTime']) * 1) # - , stateDF.loc[step - 1, 'laneI1Q'] )
                
                mn_punish = (max(stateDF.loc[step , 'laneB0FirstVehStoppedTime'] # , stateDF.loc[step , 'laneB0SIFirstVehStoppedTime'] # - , stateDF.loc[step - 1, 'laneB0FirstVehStoppedTime']
                             , stateDF.loc[step , 'laneB1FirstVehStoppedTime'] # , stateDF.loc[step , 'laneB1SIFirstVehStoppedTime'] # - , stateDF.loc[step - 1, 'laneB1FirstVehStoppedTime']
                             , stateDF.loc[step , 'laneV0FirstVehStoppedTime'] # , stateDF.loc[step , 'laneV0SIFirstVehStoppedTime'] # - , stateDF.loc[step - 1, 'laneV0FirstVehStoppedTime']
                             , stateDF.loc[step , 'laneV1FirstVehStoppedTime'] # , stateDF.loc[step , 'laneV1SIFirstVehStoppedTime'] # - , stateDF.loc[step - 1, 'laneV1FirstVehStoppedTime']
                             , stateDF.loc[step , 'laneV2FirstVehStoppedTime']) * 1 + # , stateDF.loc[step , 'laneV2SIFirstVehStoppedTime'] # - , stateDF.loc[step - 1, 'laneV2FirstVehStoppedTime']
                             stateDF.loc[step , 'laneJ0FirstVehStoppedTime']) # - , stateDF.loc[step - 1, 'laneJ0Q'] )
                
                pg_punish = (max(stateDF.loc[step , 'laneC0FirstVehStoppedTime'] # , stateDF.loc[step , 'laneC0SIFirstVehStoppedTime'] # - , stateDF.loc[step - 1, 'laneC0FirstVehStoppedTime']
                             , stateDF.loc[step , 'laneC1FirstVehStoppedTime'] # , stateDF.loc[step , 'laneC1SIFirstVehStoppedTime'] # - , stateDF.loc[step - 1, 'laneC1FirstVehStoppedTime']
                             , stateDF.loc[step , 'laneW0FirstVehStoppedTime'] # , stateDF.loc[step , 'laneW0SIFirstVehStoppedTime'] # - , stateDF.loc[step - 1, 'laneW0FirstVehStoppedTime']
                             , stateDF.loc[step , 'laneW1FirstVehStoppedTime'] # , stateDF.loc[step , 'laneW1SIFirstVehStoppedTime'] # - , stateDF.loc[step - 1, 'laneW1FirstVehStoppedTime']
                             , stateDF.loc[step , 'laneW2FirstVehStoppedTime']) * 1 + # , stateDF.loc[step , 'laneW2SIFirstVehStoppedTime'] # - , stateDF.loc[step - 1, 'laneW2FirstVehStoppedTime']
                             stateDF.loc[step , 'laneK0FirstVehStoppedTime']) # - , stateDF.loc[step - 1, 'laneK0Q'] )

                hn_punish = (max(stateDF.loc[step , 'laneD0FirstVehStoppedTime'] # , stateDF.loc[step , 'laneD0SIFirstVehStoppedTime'] # - , stateDF.loc[step - 1, 'laneD0FirstVehStoppedTime']
                             , stateDF.loc[step , 'laneD1FirstVehStoppedTime'] # , stateDF.loc[step , 'laneD1SIFirstVehStoppedTime'] # - , stateDF.loc[step - 1, 'laneD1FirstVehStoppedTime']
                             , stateDF.loc[step , 'laneD2FirstVehStoppedTime'] # , stateDF.loc[step , 'laneD2SIFirstVehStoppedTime'] # - , stateDF.loc[step - 1, 'laneD2FirstVehStoppedTime']
                             , stateDF.loc[step , 'laneX0FirstVehStoppedTime'] # , stateDF.loc[step , 'laneX0SIFirstVehStoppedTime'] # - , stateDF.loc[step - 1, 'laneX0FirstVehStoppedTime']
                             , stateDF.loc[step , 'laneX1FirstVehStoppedTime'] # , stateDF.loc[step , 'laneX1SIFirstVehStoppedTime'] # - , stateDF.loc[step - 1, 'laneX1FirstVehStoppedTime']
                             , stateDF.loc[step , 'laneX2FirstVehStoppedTime']) * 1 + # , stateDF.loc[step , 'laneX2SIFirstVehStoppedTime'] # - , stateDF.loc[step - 1, 'laneX2FirstVehStoppedTime']
                             max(stateDF.loc[step , 'laneL0FirstVehStoppedTime'] # - , stateDF.loc[step - 1, 'laneL0FirstVehStoppedTime']
                             , stateDF.loc[step , 'laneO0FirstVehStoppedTime']) * 1) # - , stateDF.loc[step - 1, 'laneO0Q'] )

                dz_punish = (max(stateDF.loc[step , 'laneE0FirstVehStoppedTime'] # , stateDF.loc[step , 'laneE0SIFirstVehStoppedTime'] # - , stateDF.loc[step - 1, 'laneE0FirstVehStoppedTime']
                             , stateDF.loc[step , 'laneE1FirstVehStoppedTime'] # , stateDF.loc[step , 'laneE1SIFirstVehStoppedTime'] # - , stateDF.loc[step - 1, 'laneE1FirstVehStoppedTime']
                             , stateDF.loc[step , 'laneE2FirstVehStoppedTime'] # , stateDF.loc[step , 'laneE2SIFirstVehStoppedTime'] # - , stateDF.loc[step - 1, 'laneE2FirstVehStoppedTime']
                             , stateDF.loc[step , 'laneE3FirstVehStoppedTime'] # , stateDF.loc[step , 'laneE3SIFirstVehStoppedTime'] # - , stateDF.loc[step - 1, 'laneE3FirstVehStoppedTime']
                             , stateDF.loc[step , 'laneY0FirstVehStoppedTime'] # , stateDF.loc[step , 'laneY0SIFirstVehStoppedTime'] # - , stateDF.loc[step - 1, 'laneY0FirstVehStoppedTime']
                             , stateDF.loc[step , 'laneY1FirstVehStoppedTime'] # , stateDF.loc[step , 'laneY1SIFirstVehStoppedTime'] # - , stateDF.loc[step - 1, 'laneY1FirstVehStoppedTime']
                             , stateDF.loc[step , 'laneY2FirstVehStoppedTime']) * 1 + # , stateDF.loc[step , 'laneY2SIFirstVehStoppedTime'] # - , stateDF.loc[step - 1, 'laneY2FirstVehStoppedTime']
                             max(stateDF.loc[step , 'laneM0FirstVehStoppedTime'] # - , stateDF.loc[step - 1, 'laneM0FirstVehStoppedTime']
                             , stateDF.loc[step , 'laneN0FirstVehStoppedTime'] # - , stateDF.loc[step - 1, 'laneN0FirstVehStoppedTime']
                             , stateDF.loc[step , 'laneN1FirstVehStoppedTime'] # - , stateDF.loc[step - 1, 'laneN1FirstVehStoppedTime']
                             , stateDF.loc[step , 'laneP0FirstVehStoppedTime']) * 1) # - , stateDF.loc[step - 1, 'laneP0Q'] )
                
                ms_reward -= ms_punish // 4
                mn_reward -= mn_punish // 8
                pg_reward -= pg_punish // 8
                hn_reward -= hn_punish // 8
                dz_reward -= dz_punish // 4
                
                agent_reward.append(simTime-5)
                agent_reward.append(ms_reward)
                agent_reward.append(old_p[0])
                agent_reward.append(fw_ms[0])
                agent_reward.append(mn_reward)
                agent_reward.append(old_p[1])
                agent_reward.append(fw_mn[0])
                agent_reward.append(pg_reward)
                agent_reward.append(old_p[2])
                agent_reward.append(fw_pg[0])
                agent_reward.append(hn_reward)
                agent_reward.append(old_p[3])
                agent_reward.append(fw_hn[0])
                agent_reward.append(dz_reward)
                agent_reward.append(old_p[4])
                agent_reward.append(fw_dz[0])
                reward_data.append(agent_reward)
                #print("ms reward: " + str(ms_reward))
                    #ms_ob, ms_reward = get_data()

                ## neightbor reward gamma
                if step <= 640:  
                    
                    ms_policy.add_transition(n_s_ms, n_p[0], ms_reward, fw_ms[1], done)
                    mn_policy.add_transition(n_s_mn, n_p[1], mn_reward, fw_mn[1], done)
                    pg_policy.add_transition(n_s_pg, n_p[2], pg_reward, fw_pg[1], done)
                    hn_policy.add_transition(n_s_hn, n_p[3], hn_reward, fw_hn[1], done)
                    dz_policy.add_transition(n_s_dz, n_p[4], dz_reward, fw_dz[1], done)

                nofirst = True 
                #print("##############################################################")
                t_r +=  (ms_reward + mn_reward + pg_reward + hn_reward + dz_reward)   
                        
    #        if simTime > 300:
    #            time.sleep(0.2)
        '''
        t_r =( stateDF.loc[simTime -1 , 'laneA0VehOuts'] + stateDF.loc[simTime -1 , 'laneA1VehOuts'] +
            stateDF.loc[simTime -1 , 'laneU0VehOuts'] + stateDF.loc[simTime -1 , 'laneU1VehOuts'] +
            stateDF.loc[simTime -1 , 'laneU2VehOuts'] + stateDF.loc[simTime -1 , 'laneI0VehOuts'] +
                              stateDF.loc[simTime -1 , 'laneI1VehOuts'] + stateDF.loc[simTime -1 , 'laneB0VehOuts'] +
                              stateDF.loc[simTime -1 , 'laneB1VehOuts'] + stateDF.loc[simTime -1 , 'laneV0VehOuts'] +
                              stateDF.loc[simTime -1 , 'laneV1VehOuts'] + stateDF.loc[simTime -1 , 'laneV2VehOuts'] +
                              stateDF.loc[simTime -1 , 'laneJ0VehOuts'] + stateDF.loc[simTime -1 , 'laneW2VehOuts'] +
                              stateDF.loc[simTime -1 , 'laneC0VehOuts'] + stateDF.loc[simTime -1 , 'laneK0VehOuts'] +
                              stateDF.loc[simTime -1 , 'laneC1VehOuts'] + stateDF.loc[simTime -1 , 'laneD0VehOuts'] +
                              stateDF.loc[simTime -1 , 'laneW0VehOuts'] + stateDF.loc[simTime -1 , 'laneD1VehOuts'] +
                              stateDF.loc[simTime -1 , 'laneW1VehOuts'] + stateDF.loc[simTime -1 , 'laneD2VehOuts'] +
                              stateDF.loc[simTime -1 , 'laneX0VehOuts'] + stateDF.loc[simTime -1 , 'laneO0VehOuts'] +
                              stateDF.loc[simTime -1 , 'laneX1VehOuts'] + stateDF.loc[simTime -1 , 'laneE0VehOuts'] +
                              stateDF.loc[simTime -1 , 'laneX2VehOuts'] + stateDF.loc[simTime -1 , 'laneE1VehOuts'] +
                              stateDF.loc[simTime -1 , 'laneL0VehOuts'] + stateDF.loc[simTime -1 , 'laneE2VehOuts'] +
                              stateDF.loc[simTime -1 , 'laneE3VehOuts'] + stateDF.loc[simTime -1 , 'laneN1VehOuts'] +
                              stateDF.loc[simTime -1 , 'laneM0VehOuts'] + stateDF.loc[simTime -1 , 'laneP0VehOuts'] +
                              stateDF.loc[simTime -1 , 'laneN0VehOuts'])
        total_reward.append(t_r)
        print("#################################")
        print(t_r)
        print("#################################")
        '''
        print(t_r)
        print("-" * 50)    
        total_reward.append(t_r)    
        
        s.sendall(b'getTotalVehOuts\n')
        data = s.recv(8192)
        data = data.decode('ascii')[:-2]
        print('totalVehOuts: ' + data)
        data = int(data)
        print("#" * 50)   
        
        #s.sendall(repaint)
        #if(i % 20 == 0):
            #s.sendall(repaint)
        #'''
        if data > max_t_r or i == times - 1: # or (i%2000 == 0):
            if i != 0 and data > max_t_r:
                max_t_r = data
            ms_policy.save('C:\\workspace\\Aanaconda\\Traffic_Data_Analysis\\TLC\\records\\ms_', i)
            mn_policy.save('C:\\workspace\\Aanaconda\\Traffic_Data_Analysis\\TLC\\records\\mn_', i)
            pg_policy.save('C:\\workspace\\Aanaconda\\Traffic_Data_Analysis\\TLC\\records\\pg_', i)
            hn_policy.save('C:\\workspace\\Aanaconda\\Traffic_Data_Analysis\\TLC\\records\\hn_', i)
            dz_policy.save('C:\\workspace\\Aanaconda\\Traffic_Data_Analysis\\TLC\\records\\dz_', i)
            
            reward_data = pd.DataFrame(reward_data, columns = cols).ffill()
            reward_data.to_csv("C:\\workspace\\Aanaconda\\Traffic_Data_Analysis\\TLC\\records\\reward" + str(i) +".csv")
            stateDF.to_csv("stateDFdebug2.txt",sep='\t', header=True, index=True, mode='w', encoding = 'utf-8')    
        #''' 
        
        '''
        if t_r == last_t_r:
            cont_t_r += 1
            if cont_t_r > 150:
                break
        else:
            last_t_r = t_r
            cont_t_r = 0
        '''
            
        s.sendall(b'restart\r\n')
    
    #reward_data = pd.DataFrame(reward_data, columns = cols).ffill()
    #reward_data.to_csv("reward.csv")
    print("###########################")
    print(total_reward)
    print("###########################")
    s.sendall(b'bye bye\r\n')


# In[9]:


now = datetime.datetime.now()
current_time = now.strftime("%H:%M:%S")
print("Current Time =", current_time)


# In[ ]:




