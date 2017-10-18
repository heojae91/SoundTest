import numpy as np
import pyaudio
import matplotlib.pyplot as plt

volume = 0.5        # Set volume in 0.0 ~ 1.0 scale
fs = 48000          # Set sample rate 48000 Hz
duration = 2.0      # Set duration for 1 second
f = 20000.0         # Set carrier frequency in float
baudRate = 4000   # Set baud rate as 4000 Hz
CHUNKSIZE = 1024 # Size of chunk

# Get bit sequence from signal
def downconverter(signal, cosSignal) :
    return signal * cosSignal


def demod(recorded) :
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=48000,
                    input=True,
                    frames_per_buffer=CHUNKSIZE)
    data = stream.read(CHUNKSIZE)
    numpydata = np.fromstring(data, dtype=np.float32)

    stream.stop_stream()
    stream.close()
    p.terminate()

    print(numpydata)
    return

#
def getStream(sequence) :
    samples = sequence


    # def generateSequence():
    #     # Get sinusoid signal point in every point as float type
    #     samples = []
    #     prev = -1
    #     currentSign = 0  # 1 for 1, -1 for 0. Basically set to 1
    #     # Get sign value on array
    #     signArray = []
    #     # Generate samples
    #     for i in range(int(duration * fs)):
    #         currentIndex = int(i / samplesPerBaud)
    #
    #         if (currentIndex != prev):
    #             if (trainingSequence[int(currentIndex / 50) % 8][currentIndex % 50] == 1):
    #                 currentSign = 1
    #             else:
    #                 currentSign = -1
    #             prev = currentIndex
    #             #    print("Row : ", int(currentIndex / 50) % 8, ", Column : ", currentIndex % 50)
    #         samples.append(np.sin(2 * np.pi * i * f / fs * currentSign).astype(np.float32))
    #     return samples
