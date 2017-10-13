import numpy as np
import pyaudio
import matplotlib.pyplot as plt

def plotingSignal(object, filename) :
    fig = plt.figure()

    axes = plt.gca()
    axes.set_ylim([-1.5, 1.5])
    axes.set_xlim([0.0, object.__len__()])

    s = fig.add_subplot(111)
    amplitude = np.fromstring(object, np.float32)
    s.plot(amplitude)
    fig.savefig("result/"+filename)
    fig.clear()

def upconverter(sampArray, carrierFreq) :
    for i in range(sampArray.__len__()) :
        sampArray[i] = sampArray[i] * np.cos(2 * np.pi * carrierFreq * i / fs) * (2 ** (1/2))
    for i in range(10) :
        print(sampArray[i])

p = pyaudio.PyAudio()

# 26-bit GSM Training Sequence
trainingSequence = ((0,0,1,0,0,1,0,1,1,1,0,0,0,0,1,0,0,0,1,0,0,1,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
                    (0,0,1,0,1,1,0,1,1,1,0,1,1,1,1,0,0,0,1,0,1,1,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
                    (0,1,0,0,0,0,1,1,1,0,1,1,1,0,1,0,0,1,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
                    (0,1,0,0,0,1,1,1,1,0,1,1,0,1,0,0,0,1,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
                    (0,0,0,1,1,0,1,0,1,1,1,0,0,1,0,0,0,0,0,1,1,0,1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
                    (0,1,0,0,1,1,1,0,1,0,1,1,0,0,0,0,0,1,0,0,1,1,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
                    (1,0,1,0,0,1,1,1,1,1,0,1,1,0,0,0,1,0,1,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
                    (1,1,1,0,1,1,1,1,0,0,0,1,0,0,1,0,1,1,1,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0))

volume = 0.5        # Set volume in 0.0 ~ 1.0 scale
fs = 48000          # Set sample rate 48000 Hz
duration = 1.0      # Set duration for 1 second
f = 4000.0         # Set carrier frequency in float
samplesPerBaud = fs / f

# Get sinusoid signal point in every point as float type
samples = []
prev = -1
currentSign = 0 # 1 for 1, -1 for 0. Basically set to 1
# Get sign value on array
signArray = []

# Generate samples
for i in range(int(duration * fs)) :
    currentIndex = int(i / samplesPerBaud)

    if (currentIndex != prev) :
        if (trainingSequence[int(currentIndex / 50) % 8][currentIndex % 50] == 1) :
            currentSign = 1
        else :
            currentSign = -1
        prev = currentIndex
#    print("Row : ", int(currentIndex / 50) % 8, ", Column : ", currentIndex % 50)
    print(currentIndex)
    signArray.append(currentSign)
    samples.append(np.sin(2 * np.pi * i * f / fs * currentSign).astype(np.float32))

standardSound = (np.sin(2*np.pi*np.arange(fs*duration)*f/fs)).astype(np.float32)

upconverter(samples, 20000)
print("maximum : ", np.amax(samples))
samples = np.array(samples)
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=fs,
                output=True)

stream.write(volume * samples)
print(2 ** (1/2))
for i in range(100,fs,100) :
    plotingSignal(samples[i-100:i], str(i) + 'plt.png')
    plotingSignal(standardSound[i-100:i], str(i) + 'std.png') 

stream.stop_stream()
stream.close()

p.terminate()