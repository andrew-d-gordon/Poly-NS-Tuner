from math import log2, pow

A4 = 440
C0 = A4 * pow(2, -4.75)
name = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

def pitch(freq):
    h = round(12 * log2(freq / C0)) #can also use log(x)/log(2) to replace log2
    octave = h // 12
    n = h % 12
    return name[n] + str(octave)