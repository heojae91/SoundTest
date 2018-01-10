import wave
import array
import struct
import time


def convert(fin, fout, chunk_size=1024*1024) :
    chunk_size *= 4

    waveout = wave.open(fout, "wb")
    waveout.setparams((1, 1, 48000, 0, "NONE", ""))

    while True:
        raw_floats = fin.read(chunk_size)
        if raw_floats == "":
            return

        floats = array.array('f', raw_floats[:len(raw_floats)-2])
        samples = [int(sample)* 32767
                   for sample in floats]
        print(type(samples[1]))
        raw_ints = struct.pack("<%dh" % len(samples), *samples)
        waveout.writeframes(raw_ints)

convert(open("result/output2.wav", "rb"), open("result/output3.wav", "wb"))