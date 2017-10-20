import numpy as np

def getBasebandSignal(sequence, f=4000, fs=48000) :
    samplesPerSymbol = int(fs / f)
    signArray = []
    for i in range(f) :
        if (sequence[int(i / 50) % 8][i % 50] == 1) :
            signArray = signArray + [1] * samplesPerSymbol
        else :
            signArray = signArray + [-1] * samplesPerSymbol
    return signArray

def getSinusoidSignal(freq=20000, fs=48000) :
    return 2 ** (1/2) * np.cos(2 * np.pi * np.arange(1.0 * fs) * freq / fs)

def modulateSignal(basebandSignal, freq=20000, fs=48000) :
    return basebandSignal* getSinusoidSignal(freq=freq, fs=fs)

def upconvertSignal(modulatedSignal, freq=20000, fs=48000)  :
    cosineSignal = 2 ** (1 / 2) * np.cos(2 * np.pi * np.arange(1.0 * fs) * freq / fs)
    return modulatedSignal * cosineSignal