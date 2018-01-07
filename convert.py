import wave
import array
import struct


def convert(fin, fout, chunk_size=1024*1024) :
    chunk_size *= 4

    waveout = wave.open(fout, "wb")
    waveout.setparams((1, 1, 48000, 0, "NONE", ""))

    tmp = struct.pack('f', 3.1415982)
    print(tmp)
    print(type(tmp))

    while True:
        raw_floats = fin.read(chunk_size)
        if raw_floats == "":
            return
        floats = array.array('f', raw_floats)
        samples = [sample * 32767
                   for sample in floats]
        raw_ints = struct.pack("<%dh" % len(samples), *samples)
        waveout.writeframes(raw_ints)

convert(open("result/output2.wav", "rb"), open("result/output3.wav", "wb"))