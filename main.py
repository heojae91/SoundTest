import numpy as np
import pyaudio
from scipy import fft
import matplotlib.pyplot as plt

import Modulator
import Demodulator
import Filter

def plotSpectrum(y, fs) :
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


# 26-bit GSM Training Sequence
trainingSequence = ((0,0,1,0,0,1,0,1,1,1,0,0,0,0,1,0,0,0,1,0,0,1,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
                    (0,0,1,0,1,1,0,1,1,1,0,1,1,1,1,0,0,0,1,0,1,1,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
                    (0,1,0,0,0,0,1,1,1,0,1,1,1,0,1,0,0,1,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
                    (0,1,0,0,0,1,1,1,1,0,1,1,0,1,0,0,0,1,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
                    (0,0,0,1,1,0,1,0,1,1,1,0,0,1,0,0,0,0,0,1,1,0,1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
                    (0,1,0,0,1,1,1,0,1,0,1,1,0,0,0,0,0,1,0,0,1,1,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
                    (1,0,1,0,0,1,1,1,1,1,0,1,1,0,0,0,1,0,1,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
                    (1,1,1,0,1,1,1,1,0,0,0,1,0,0,1,0,1,1,1,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0))

signal = Modulator.generateSequence(trainingSequence)
samples = Demodulator.demod(signal)

p = pyaudio.PyAudio()
p_receiver = pyaudio.PyAudio()

fs = 48000
ts = 1.0/fs
t = np.arange(0, 1, ts)

filteredSignal = Filter.butter_bandpass_filter(signal, lowcut=18000, highcut=22000, fs=fs)
plotSpectrum(filteredSignal, fs)
plt.show()

volume = 0.5

signal = np.array(signal)
Demodulator.demod(signal)
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=fs,
                output=True)
plt.clf()
plt.plot(filteredSignal[100:200])
plt.show()
stream.write(volume * filteredSignal)

stream.stop_stream()
stream.close()

p.terminate()