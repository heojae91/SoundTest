from scipy.signal import butter, lfilter

# Used to filter bandpass signal
def butter_bandpass(lowcut, highcut, fs, order=5) :
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low,high], btype='bandpass')
    return b, a

# Applying bandpass signal to data signal
def butter_bandpass_filter(data, lowcut, highcut, fs, order=5) :
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y
