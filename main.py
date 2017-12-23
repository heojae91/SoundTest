import numpy as np
import pyaudio
import matplotlib.pyplot as plt
import wave
import scipy.io.wavfile as wav


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
t = np.arange(48000)
freq = 20000

sineSignal = Modulator.getSinusoidSignal(20000, 48000)

# sine_filtered = Filter.butter_bandpass_filter(sineSignal, 18000, 22000, 48000)
basebandSignal = Modulator.getBasebandSignal(trainingSequence)      # Generate baseband signal
modulatedSignal = Modulator.modulateSignal(basebandSignal)          # Generate passband signal

# Filtering passband signal
filteredSignal = Filter.butter_bandpass_filter(modulatedSignal, lowcut=18000, highcut=22000, fs=fs)

receivedSignal = Demodulator.downconverter(modulatedSignal)       # Retrieving baseband signal
resultSignal = Filter.butter_lowpass_filter(receivedSignal, cutoff=4000, fs=fs)

# testModulate = np.concatenate(modulatedSignal[100:], modulatedSignal[:100])
# print(testModulate)
# testReceivedSignal = Demodulator.downconverter(testModulate)
# testResultSignal = Filter.butter_lowpass_filter(testReceivedSignal, cutoff=4000, fs=fs)

p = pyaudio.PyAudio()
p_receiver = pyaudio.PyAudio()

# Plotter.plotSpectrum(resultSignal, fs)

stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=fs,
                output=True)

# Plotter.plotSpectrum(modulatedSignal, fs)
# Plotter.plotSpectrum(filteredSignal, fs)
Plotter.getSpecgram(sineSignal)

# plt.figure(1)
# plt.subplot(311)
# plt.plot(filteredSignal[:1200])
# plt.subplot(312)
# plt.plot(basebandSignal[:1200])
# plt.subplot(313)
# plt.plot(resultSignal[0:1200])
# plt.show()

volume = 0.5
stream.write(volume * filteredSignal)

stream.stop_stream()
stream.close()
p.terminate()

# Plotter.plotSpectrum(filteredSignal, fs)
filteredSignal = filteredSignal.astype(np.float32)
print(type(filteredSignal[1]))
wav.write('result/output2.wav', 48000, filteredSignal)
filteredSineSignal = Filter.butter_bandpass_filter(sineSignal, lowcut=18000, highcut=22000, fs=48000)
waveFile = wave.open('result/output.wav', 'wb')
waveFile.setnchannels(1)
# waveFile.setsampwidth(p.get_sample_size(pyaudio.paFloat32))
waveFile.setsampwidth(4)
waveFile.setframerate(48000)
waveFile.writeframes(b''.join(sineSignal))
waveFile.close()