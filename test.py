import numpy as np
import pyaudio
import matplotlib.pyplot as plt

p = pyaudio.PyAudio()

# 26-bit GSM Training Sequence
trainingSequence = ((0,0,1,0,0,1,0,1,1,1,0,0,0,0,1,0,0,0,1,0,0,1,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
                    (0,0,1,0,1,1,0,1,1,1,0,1,1,1,1,0,0,0,1,0,1,1,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
                    (0,1,0,0,0,0,1,1,1,0,1,1,1,0,1,0,0,1,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
                    (0,1,0,0,0,1,1,1,1,0,1,1,0,1,0,0,0,1,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
                    (0,0,0,1,1,0,1,0,1,1,1,0,0,1,0,0,0,0,0,1,1,0,1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
                    (0,1,0,0,1,1,1,0,1,0,1,1,0,0,0,0,0,1,0,0,1,1,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
                    (1,0,1,0,0,1,1,1,1,1,0,1,1,0,0,0,1,0,1,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
                    (1,1,1,0,1,1,1,1,0,0,0,1,0,0,1,0,1,1,1,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0))

volume = 0.5    # Set volume in 0.0 ~ 1.0 scale
fs = 48000      # Set sample rate 48000 Hz
duration = 1.0  # Set duration for 1 second
f = 20000.0      # Set carrier frequency in float

# Get sinusoid signal point in every point as float type
samples = []
prev = 0

# Generate samples
for i in range(48000) :
    currentSign = 1 # 1 for 1, -1 for 0. Basically set to 1
    currentIndex = int(i / 2.4) # Update index to scale of carrier frequency

    if (currentIndex != prev) :
        if (trainingSequence[int(currentIndex / 50) % 8][currentIndex % 50] == 1) :
            currentSign = 1
        else :
            #print("Current Row : ", int(currentIndex/50)%8, "Current Column : ", currentIndex%50, "Current Value : ", trainingSequence[int(currentIndex/50)%8][currentIndex%50])
            currentSign = -1
        prev = currentIndex
    print(i)
    samples.append(np.sin(2 * np.pi * i * f / fs * currentSign).astype(np.float32))

samples = np.array(samples)
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=fs,
                output=True)

stream.write(volume * samples)

stream.stop_stream()
stream.close()

p.terminate()

# 캐리어 주파수를 생성하는 함수
def generateCarrier(carrierFreq=18000) :
    return