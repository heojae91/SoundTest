import matplotlib.pyplot as plt
import numpy as np
from scipy import fft

def plotSpectrum(y, fs=48000) :
    n = len(y)
    k = np.arange(n)
    T = n/ fs
    frq = k / T
    frq = frq[range(int(n/2))]

    Y = fft(y) / n
    Y = Y[range(int(n/2))]

    plt.plot(frq, abs(Y), 'r')
    plt.xlabel('Freq (Hz)')
    plt.ylabel('|Y(freq)|')
    plt.show()
