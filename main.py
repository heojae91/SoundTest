import numpy as np
import pyaudio
import matplotlib.pyplot as plt
import wave
import scipy.io.wavfile as wav
import sys
import array
import struct

import Modulator
import Demodulator
import Filter
import Plotter

def floatToInt(data) :
    for i in range(data.__len__()) :
        data[i] = data[i] * 32768
    return data

def convert(fin, fout, chunk_size=1024*1024) :
    chunk_size *= 4

    waveout = wave.open(fout, "wb")
    waveout.setparams((1, 1, 48000, 0, "NONE", ""))

    while True :
        raw_floats = fin.read(chunk_size)
        if raw_floats == "" :
            return

        floats = array.array('f', raw_floats)
        samples = [sample * 32767 for sample in floats]
        raw_ints = struct.pack("<%dh" % len(samples), *samples)
        waveout.writeframes(raw_ints)

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
print("BB")
basebandSignal = Modulator.getBasebandSignal(trainingSequence, round=10)      # Generate baseband signal
print("BM")
modulatedSignal = Modulator.modulateSignal(basebandSignal, round=10)          # Generate passband signal

# Filtering passband signal
filteredSignal = Filter.butter_bandpass_filter(modulatedSignal, lowcut=18000, highcut=22000, fs=fs)

# receivedSignal = Demodulator.downconverter(modulatedSignal)       # Retrieving baseband signal
# resultSignal = Filter.butter_lowpass_filter(receivedSignal, cutoff=4000, fs=fs)

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
# Plotter.getSpecgram(sineSignal)

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

max = 1000.0



# Plotter.plotSpectrum(filteredSignal, fs)
filteredSignal = filteredSignal.astype(np.float32)
# newFilteredSignal = floatToInt(filteredSignal).astype(np.int16)

# for i in range(filteredSignal.__len__()) :
#     print(filteredSignal[i])
for i in range(filteredSignal.__len__()) :
    if (filteredSignal[i] < max) :
        max = filteredSignal[i]
print("Maximum :  ", max)
wav.write('result/output2.wav', 48000, filteredSignal)

intSignal = np.array([0]*filteredSignal.__len__(), dtype=np.int16)
print("filter : ", filteredSignal.__len__(), "output : ", intSignal.__len__())
print(intSignal.dtype)

for i in range(filteredSignal.__len__()) :
    intSignal[i] = int(filteredSignal[i] * 32767 / 2.84389)

wav.write('result/output3.wav', 48000, intSignal)
waveFile = wave.open('result/output.wav', 'wb')
waveFile.setnchannels(1)
# waveFile.setsampwidth(p.get_sample_size(pyaudio.paFloat32))
waveFile.setsampwidth(2)
waveFile.setframerate(48000)
waveFile.writeframes(b''.join(sineSignal))
waveFile.close()
