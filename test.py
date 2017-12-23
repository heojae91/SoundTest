import numpy as np
import pyaudio
import matplotlib.pyplot as plt
import wave

from scipy.signal import butter, lfilter
import Modulator
import Demodulator
import Filter
import Plotter

def butter_bandpass(lowcut, highcut, fs, order=5) :
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low,high], btype='bandpass')
    return b, a

# Applying bandpass signal to data signal
def butter_bandpass_filter(data, lowcut, highcut, fs, order=12) :
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

def butter_lowpass(cutoff, fs, order=5) :
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5) :
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y

fs = 48000
ts = 1.0/fs
t = np.arange(48000)
freq = 20000

sineSignal = 2 ** (1/2) * np.cos(2 * np.pi * np.arange(fs * 1.0)* freq / fs).astype(np.float32)

p = pyaudio.PyAudio()
p_receiver = pyaudio.PyAudio()

stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=fs,
                output=True)

volume = 0.5
stream.write(volume * sineSignal)

stream.stop_stream()
stream.close()
p.terminate()

Plotter.plotSpectrum(sineSignal, fs)

filteredSineSignal = Filter.butter_bandpass_filter(sineSignal, lowcut=18000, highcut=22000, fs=48000)
print(type(sineSignal[1]))

waveFile = wave.open('result/output.wav', 'wb')
waveFile.setnchannels(1)
waveFile.setsampwidth(4)
waveFile.setframerate(48000)
waveFile.writeframes(b''.join(sineSignal))
waveFile.close()