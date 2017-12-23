import matplotlib.pyplot as plt
from matplotlib import mlab
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

def getSpecgram(stream, Fs=48000) :
    N = 512
    f = np.arange(1, 9) * 2000
    t = np.arange(8 * Fs) / Fs
    print(f)
    x = np.empty(t.shape)
    for i in range(8):
        x[i * Fs:(i + 1) * Fs] = np.cos(2 * np.pi * f[i] * t[i * Fs:(i + 1) * Fs])

    w = np.hamming(N)
    ov = N - Fs // 1000  # e.g. 512 - 48000 // 1000 == 464
    Pxx, freqs, bins = mlab.specgram(x, NFFT=N, Fs=Fs, window=w,
                                     noverlap=ov)

    # plot the spectrogram in dB

    Pxx_dB = np.log10(Pxx)
    plt.subplots_adjust(hspace=0.4)

    plt.subplot(211)
    ex1 = bins[0], bins[-1], freqs[0], freqs[-1]
    plt.imshow(np.flipud(Pxx_dB), extent=ex1)
    plt.axis('auto')
    plt.axis(ex1)
    plt.xlabel('time (s)')
    plt.ylabel('freq (Hz)')

    # zoom in at t=4s to show transient

    plt.subplot(212)
    n1, n2 = int(3.991 / 8 * len(bins)), int(4.009 / 8 * len(bins))
    ex2 = bins[n1], bins[n2], freqs[0], freqs[-1]
    plt.imshow(np.flipud(Pxx_dB[:, n1:n2]), extent=ex2)
    plt.axis('auto')
    plt.axis(ex2)
    plt.xlabel('time (s)')
    plt.ylabel('freq (Hz)')

    plt.show()
