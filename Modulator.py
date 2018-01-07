import numpy as np

def getBasebandSignal(sequence, f=4000, fs=48000, round=2) :
    samplesPerSymbol = int(fs / f)
    signArray = []
    signArray = np.array(signArray)

    for ro in range(round) :
        print(ro)
        for i in range(f) :
            if (sequence[int(i / 50) % 8][i % 50] == 1) :
                signArray = np.append(signArray, ([1] * samplesPerSymbol))
            else :
                signArray = np.append(signArray, ([-1] * samplesPerSymbol))
    print(signArray.__len__())
    return signArray.astype(np.float32)

def getSinusoidSignal(freq=20000, fs=48000, round=2) :
    return 2 ** (1/2) * np.cos(2 * np.pi * np.arange(fs * 1.0 * round)* freq / fs).astype(np.float32)

def modulateSignal(basebandSignal, freq=20000, fs=48000, round=2) :
    print("M")
    return basebandSignal* getSinusoidSignal(freq=freq, fs=fs, round=round)

def upconvertSignal(modulatedSignal, freq=20000, fs=48000, round=2)  :
    print(type(np.arange(1 * 1.0)))
    cosineSignal = getSinusoidSignal(freq, fs)
    return modulatedSignal * cosineSignal