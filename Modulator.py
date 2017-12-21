import numpy as np

def getBasebandSignal(sequence, f=4000, fs=48000) :
    samplesPerSymbol = int(fs / f)
    signArray = []
    signArray = np.ndarray(signArray)
    for i in range(f) :
        if (sequence[int(i / 50) % 8][i % 50] == 1) :
            signArray = signArray + [1] * samplesPerSymbol
        else :
            signArray = signArray + [-1] * samplesPerSymbol
    print(signArray)
    return signArray

def getSinusoidSignal(freq=20000, fs=48000) :
    return 2 ** (1/2) * np.cos(2 * np.pi * np.arange(fs * 1.0)* freq / fs).astype(np.float32)

def modulateSignal(basebandSignal, freq=20000, fs=48000) :
    return basebandSignal* getSinusoidSignal(freq=freq, fs=fs)

def upconvertSignal(modulatedSignal, freq=20000, fs=48000)  :
    print(type(np.arange(1 * 1.0)))
    cosineSignal = getSinusoidSignal(freq, fs)
    return modulatedSignal * cosineSignal