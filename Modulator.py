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

def generateSignSequence(sequence, f=4000, fs=48000) :
    samplesPerSymbol = fs / f
    signArray = []
    for i in range(fs) :
        if (sequence[i % (50 * samplesPerSymbol)][i % samplesPerSymbol] == 1) :
            signArray.append(1)
        else :
            signArray.append(-1)
    return signArray


def generateSequence(sequence) :
    fs = 48000  # Set sample rate 48000 Hz
    duration = 1.0  # Set duration for 1 second
    f = 4000.0  # Set carrier frequency in float

    # Get sinusoid signal point in every point as float type
    samples = []
    prev = -1
    currentSign = 0  # 1 for 1, -1 for 0. Basically set to 1
    # Get sign value on array
    signArray = []
    # Generate samples
    for i in range(int(duration * fs)) :
        currentIndex = int(i / (fs/f))
        if (currentIndex != prev):
            if (sequence[int(currentIndex / 50) % 8][currentIndex % 50] == 1):
                currentSign = 1
                signArray.append(currentSign)
            else:
                currentSign = -1
                signArray.append(currentSign)
            prev = currentIndex
            #    print("Row : ", int(currentIndex / 50) % 8, ", Column : ", currentIndex % 50)
        samples.append(np.sin(2 * np.pi * i * f / fs * currentSign).astype(np.float32))
    return samples

def convolveSignal(signal, fs=48000) :
    cosineSignal = 2 ** (1 / 2) * np.cos(2 * np.pi * np.arange(1.0 * fs) * 16000 / fs)
    return signal * cosineSignal
