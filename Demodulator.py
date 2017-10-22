import numpy as np
import pyaudio
import matplotlib.pyplot as plt

import Modulator

"""
아리까리한점
1. 어떻게 스트림과 디모듈레이션을 동시에 수행할 수 있을까 
진행 스텝
1. 일단 수신한다.
2. 수신한 신호를 비트스트림으로 변경한다.
3. 비트 스트림을 분석하여 레퍼런스 시그널(트레이닝 시퀀스)와 일치시킨다.
4. phase를 비교한다
"""

volume = 0.5        # Set volume in 0.0 ~ 1.0 scale
fs = 48000          # Set sample rate 48000 Hz
duration = 2.0      # Set duration for 1 second
f = 20000.0         # Set carrier frequency in float
baudRate = 4000   # Set baud rate as 4000 Hz
CHUNKSIZE = 1024 # Size of chunk

# Get bit sequence from signal
def downconverter(signal) :
    return Modulator.upconvertSignal(signal)

def demod(samples) :
    print("Samples : ", samples[0:12])
