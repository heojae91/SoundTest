import numpy as np

import Filter

class CostasReceiver:
    def __init__(self):
        self.phaseOffset = 0

    def I_productModulator(self, inputSignal, fc=20000, fs=48000):
        cosineWave = np.cos(2 * np.pi * np.arange(1.0 * fc) * fc / fs + self.phaseOffset)
        return inputSignal * cosineWave

    def Q_productModulator(self, inputSignal, fc=20000, fs=48000):
        sineWave = np.sin(2 * np.pi * np.arange(1.0 * fc) * fc / fs + self.phaseOffset)
        return inputSignal * sineWave

    def phaseDiscriminator(self, I_signal, Q_signal, fs=48000):
        filtered_ISignal = Filter.butter_lowpass_filter(I_signal, cutoff=4000, fs=fs)
        filtered_QSignal = Filter.butter_lowpass_filter(Q_signal, cutoff=4000, fs=fs)

        multipledSignal = filtered_ISignal * filtered_QSignal

    def __del__(self):
        return
