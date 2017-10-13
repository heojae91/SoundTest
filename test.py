import numpy as np
import pyaudio
import matplotlib.pyplot as plt

def plotingSignal(object, filename) :
    fig = plt.figure()

    # axes = plt.gca()
    # axes.set_ylim([-1.5, 1.5])
    # axes.set_xlim([0.0, object.__len__()])

    s = fig.add_subplot(111)
    amplitude = np.fromstring(object, np.float32)
    s.plot(amplitude)
    fig.savefig("result/"+filename)
    fig.clear()

sinSig = (np.sin(np.arange(48000*1.0)*4000.0/48000)).astype(np.float32)
cosSig = (2 ** (1/2) * (np.cos(2*np.pi*np.arange(48000*1.0)*4000.0/48000)).astype(np.float32))

# plotingSignal(sinSig[:200], "sine_sig")
# plotingSignal(cosSig[:200], "cosine_sig")

upconvertedSig = np.convolve(sinSig[23500:24500], cosSig, 'same')
downconvertedSig = np.convolve(upconvertedSig[23500:24500], cosSig, 'same')

print(sinSig.__len__())
print(cosSig.__len__())

print(upconvertedSig.__len__())
print(downconvertedSig.__len__())
plotingSignal(upconvertedSig, "upconverted")
plotingSignal(downconvertedSig, "downconverted")
