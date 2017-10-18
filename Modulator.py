import numpy as np
import pyaudio
import matplotlib.pyplot as plt
import scipy

def plotingSignal(object, filename) :
    fig = plt.figure()

    axes = plt.gca()
    axes.set_ylim([-1.5, 1.5])
    axes.set_xlim([0.0, object.__len__()])

    s = fig.add_subplot(111)
    amplitude = np.fromstring(object, np.float32)
    s.plot(amplitude)
    fig.savefig("result/"+filename)
    fig.clear()

def upconverter(sampArray, carrierFreq) :
    cosSig = []

    # Generate cosine signal to convolve with sampled signal
    # for i in range(sampArray.__len__()) :
    #     cosSig.append((2 ** (1/2)) * 2 * np.pi * i / )
    # for i in range(10) :
    #     print(sampArray[i])

p = pyaudio.PyAudio()

volume = 0.5  # Set volume in 0.0 ~ 1.0 scale
fs = 48000  # Set sample rate 48000 Hz
duration = 1.0  # Set duration for 1 second
f = 4000.0  # Set carrier frequency in float

def generateSequence(sequence) :
    # Get sinusoid signal point in every point as float type
    samples = []
    prev = -1
    currentSign = 0  # 1 for 1, -1 for 0. Basically set to 1
    # Get sign value on array
    signArray = []
    # Generate samples
    for i in range(int(duration * fs)):
        currentIndex = int(i / f)

        if (currentIndex != prev):
            if (sequence[int(currentIndex / 50) % 8][currentIndex % 50] == 1):
                currentSign = 1
            else:
                currentSign = -1
            prev = currentIndex
            #    print("Row : ", int(currentIndex / 50) % 8, ", Column : ", currentIndex % 50)
        samples.append(np.cos(2 * np.pi * i * f / fs * currentSign).astype(np.float32))
    cosineSignal = np.cos(2 * np.pi * np.arange(1.0 * fs) * 20000 / fs)
    return samples * cosineSignal

# volume = 0.5  # Set volume in 0.0 ~ 1.0 scale
# fs = 48000  # Set sample rate 48000 Hz
# duration = 1.0  # Set duration for 1 second
# f = 20000.0  # Set carrier frequency in float
# baudRate = 4000  # Set baud rate as 4000 Hz
# samplesPerBaud = fs / baudRate
# def generateSequence(sequence) :
#     trainingSequence = sequence
#     # Get sinusoid signal point in every point as float type
#     samples = []
#     prev = -1
#     currentSign = 0 # 1 for 1, -1 for 0. Basically set to 1
#     # Get sign value on array
#     signArray = []
#     # Generate samples
#     for i in range(int(duration * fs)) :
#         currentIndex = int(i / samplesPerBaud)
#
#         if (currentIndex != prev) :
#             if (trainingSequence[int(currentIndex / 50) % 8][currentIndex % 50] == 1) :
#                 currentSign = 1
#             else :
#                 currentSign = -1
#             prev = currentIndex
#     #    print("Row : ", int(currentIndex / 50) % 8, ", Column : ", currentIndex % 50)
#         samples.append(np.sin(2 * np.pi * i * f / fs * currentSign).astype(np.float32))
#     return samples