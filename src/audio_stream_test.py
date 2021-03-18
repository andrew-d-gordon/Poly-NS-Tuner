#PPD, fiddle~ notes/drafting

#!apt install libasound2-dev portaudio19-dev libportaudio2 libportaudiocpp0 ffmpeg
#!pip install pyaudio

import math
import struct
import time
from math import log10
import matplotlib.pyplot as plt

import pyaudio

p=pyaudio.PyAudio()

def decibelScale(value):
    return 20*log10(value)

def levelRMS(data):
    count = len(data)/2
    format = "%dh"%count
    shorts = struct.unpack(format, data)
    sum_squares = 0.0
    for sample in shorts:
        n = sample*(1.0/32678)
        sum_squares += n*n
    return decibelScale(math.sqrt(sum_squares / count))

def callback(in_data, frame_count, time_info, status):
  levels = []
  for _i in range(1024):
    levels.append(struct.unpack('<h', in_data[_i:_i+2])[0])
  avg_chunk = sum(levels)/len(levels)
  print("Level:", avg_chunk, "Time:", time_info['current_time'], "i:", _i, "rms:", levelRMS(in_data))

  #print(levels(stream.read(1024)))

  return (in_data, pyaudio.paContinue)

stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=48000,
                frames_per_buffer=1024,
                input=True,
                output=True,
                stream_callback=callback)

#print(levels(stream.read(1024)))

time.sleep(10)
stream.close()



'''
Notes/Pseudo:
Algo originally uses optimized discrete hartley transform, any reasonably fast dft algo should be fine.
Rob Mayer wrote traditionally used code for this algorithm, denoted "Fastest Fourier Transform in the West"

1) Fiddle~ computes a DFT of a block of input, zeropadded by a factor of four, three main steps:
    1.1) Initial Computation,
    1.2) Spectral interpolation, 
    1.3) and frequency domain windowing

1.1) Initial Computation
Suppose you have a real, length N signal x[n], and we modulate signal by complex exponential e^-j*(pi/2N)*n to obtain:
xmod[n] = x[n]*e^-j*(pi/2N)*n

We can compute DFT of this modulated signal as:

Xmod[k] = Summation(n=0, N-1){x[n]*(e^-j*(pi/2N)*n)*(e^-j*(2pi/N)*kn)} = Summation(n=0, N-1){x[n]*(e^-j*(pi/2N)*(4k+1)n)}
for k E [0, N-1].

Now suppose we take same signal x[n], and rather than modulate it, we zeropad it to length 4N to obtain a signal xzeropad[n].
DFT of this new signal is...
Xzeropad[k]=Summation(n=0, N-1){x[n]*(e^-j*(2pi/4N)*kn)}=Summation(n=0, N-1){x[n]*(e^-j*(pi/2N)*kn)}
for k E [0, 4N-1]. Note that...

Xmod[k] = Xzeropad[4k+1]

Guessing Fundamental Frequencies...

L(f) is a non-negative likelihood function where f is frequency. The presence of peaks at or near multiples of f increases
L(f) in a way which depends on the peak's amplitude and frequency as shown:

L(f) = Summation(i=0,k){ai*ti*ni}
Where k is number of peaks in the spectrum, 
-ai is a factor depending on the amplitude of the ith peak,
-ti depends on how closely the ith peak is tuned to a multiple of fi
-ni depends on whether the peak is closest to a low or high multiple of f

For monophonic pitch estimation, we simply output the value of f whose "likelihood" is highest.
For polyphonic pitch estimation, we successively take the values of f of greatest likelihood which are neither multiples
nor sub-multiples of a previous one.  (loosen up on being sub multiple for octaves)

In all cases, last criteria to determine if there is pitch (as L(f) will always have a maximum even if no pitch).
Our criterion is that there either be at least four peaks present or else that the fundamental be present and the total 
power of contributing peaks be at least a hundredth of the signal power.

'''