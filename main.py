import numpy as np
import pyaudio
from scipy import fft
import matplotlib.pyplot as plt

import Modulator
import Demodulator
import Filter
import Plotter

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
convolvedSignal = Modulator.convolveSignal(signal)

p = pyaudio.PyAudio()
p_receiver = pyaudio.PyAudio()

fs = 48000
ts = 1.0/fs
t = np.arange(0, 1, ts)

# plt.clf()
# plt.plot(convolvedSignal[0:500])
# plt.show()

filteredSignal = Filter.butter_bandpass_filter(convolvedSignal, lowcut=18000, highcut=22000, fs=fs)
#Plotter.plotSpectrum(filteredSignal, fs)
convolvedSignal= Modulator.convolveSignal(filteredSignal)
# filteredSignal = Filter.butter_bandpass_filter(convolvedSignal, lowcut=2000, highcut=6000, fs = fs)
#Plotter.plotSpectrum(filteredSignal, fs)
plt.show()

print(Modulator.generateSignSequence(trainingSequence))
volume = 0.5
print("Signal : ", signal[0:12])
Demodulator.demod(filteredSignal)
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=fs,
                output=True)
# plt.clf()
# plt.plot(convolvedSignal[0:500])
# plt.show()
stream.write(volume * filteredSignal)

stream.stop_stream()
stream.close()

p.terminate()