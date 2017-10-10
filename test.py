import numpy as np
import pyaudio
import matplotlib.pyplot as plt

def plotingSignal(object, filename) :
    fig = plt.figure()

    axes = plt.gca()
    axes.set_ylim([-1.0, 1.0])
    axes.set_xlim([0.0, object.__len__()])

    s = fig.add_subplot(111)
    amplitude = np.fromstring(object, np.float32)
    s.plot(amplitude)
    fig.savefig("result/"+filename)

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
f = 20000.0         # Set carrier frequency in float
baudRate = 4000   # Set baud rate as 4000 Hz
samplesPerBaud = fs / baudRate
signalPerBaud = int(f / baudRate)

# Get sinusoid signal point in every point as float type
samples = []
prev = 0

# Get sign value on array
signArray = []
# Generate samples
for i in range(fs) :
    currentSign = 1                 # 1 for 1, -1 for 0. Basically set to 1
    currentIndex = int((i / samplesPerBaud) / signalPerBaud)
    # currentIndex = int((i+1) / 2.4) # Update index to scale of carrier frequency

    if (currentIndex != prev) :
        if (trainingSequence[int(currentIndex / 50) % 8][currentIndex % 50] == 1) :
            currentSign = 1
        else :
            currentSign = -1
        prev = currentIndex
    # To examine sign
    # signArray.append(currentSign)
    print(currentIndex)
    print("Row : ", int(currentIndex / 50) % 8, ", Column : ", currentIndex % 50)
    samples.append(np.sin(2 * np.pi * i * f / fs * currentSign).astype(np.float32))

standardSound = (np.sin(2*np.pi*np.arange(fs*duration)*f/fs)).astype(np.float32)

samples = np.array(samples)
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=fs,
                output=True)

stream.write(volume * samples)

print("##### These are sample #####")
print(samples[:20])
print("##### These are standard #####")
print(standardSound[:20])
print("##### These are sign #####")
print(signArray)

for i in range(20) :
    print("samples : ", samples[i], " - standard : ", standardSound[i], ", result : ", samples[i] - standardSound[i])


plotingSignal(samples[:100], 'plt.png')
plotingSignal(standardSound[:100], 'std.png')
stream.stop_stream()
stream.close()

p.terminate()