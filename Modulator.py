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
    samplesPerSymbol = int(fs / f)
    signArray = []
    for i in range(f) :
        if (sequence[int(i / 50) % 8][i % 50] == 1) :
            signArray = signArray + [1] * samplesPerSymbol
        else :
            signArray = signArray + [-1] * samplesPerSymbol
    return signArray

def getSinusoidSignal(fs=48000) :
    return np.sin(2 * np.pi * np.arange(1.0 * fs) * 4000 / fs)

def convolveSignal(signal, fs=48000) :
    cosineSignal = 2 ** (1 / 2) * np.cos(2 * np.pi * np.arange(1.0 * fs) * 16000 / fs)
    return signal * cosineSignal

def convolveSign(signArray, fs=48000) :
    cosineSignal = np.cos(2 * np.pi * np.arange(1.0 * fs) * 20000 / fs)
    result = []
    for i in range(fs) :
        result.append(cosineSignal[i] * signArray[i])
    return result