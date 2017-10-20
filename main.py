import numpy as np
import pyaudio
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

fs = 48000
ts = 1.0/fs
t = np.arange(0, 1, ts)

basebandSignal = Modulator.getBasebandSignal(trainingSequence)      # Generate baseband signal
modulatedSignal = Modulator.modulateSignal(basebandSignal)          # Generate passband signal

# Filtering passband signal
filteredSignal = Filter.butter_bandpass_filter(modulatedSignal, lowcut=18000, highcut=20000, fs=fs)

receivedSignal = Modulator.upconvertSignal(modulatedSignal)       # Retrieving baseband signal
resultSignal = Filter.butter_lowpass_filter(receivedSignal, cutoff=4000, fs=fs)

p = pyaudio.PyAudio()
p_receiver = pyaudio.PyAudio()

Plotter.plotSpectrum(resultSignal, fs)

stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=fs,
                output=True)

# Plotter.plotSpectrum(filteredSignal, fs)

plt.figure(1)
plt.subplot(311)
plt.plot(modulatedSignal[:1200])
plt.subplot(312)
plt.plot(basebandSignal[:1200])
plt.subplot(313)
plt.plot(resultSignal[:1200])
plt.show()

volume = 0.5
stream.write(volume * filteredSignal)

stream.stop_stream()
stream.close()

p.terminate()