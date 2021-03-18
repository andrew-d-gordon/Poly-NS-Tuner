import matplotlib.pyplot as plt
from librosa import load
# from scipy.io import wavfile as wav
from scipy.fftpack import fft
import numpy as np
import heapq
from freq_to_note import pitch


def maxInFT(yf, xf, audio_len):
    maxMagIdx = np.argmax(yf[:audio_len // 2], axis=0)  # get max idx
    #print(maxMagIdx, " ", yf[maxMagIdx], " ", xf[maxMagIdx])
    yf[maxMagIdx] = (0 + 0j)
    return xf[maxMagIdx]


def fftplot(yf, xf, audio_len):
    fig, ax = plt.subplots()
    ax.plot(xf, 2.0 / audio_len * np.abs(yf[:audio_len // 2]))
    plt.grid()
    plt.xlabel("Frequency-->")
    plt.ylabel("Magnitude")
    return plt.show()


def computeFT(audio, sr):
    audio_len = len(audio)
    T = 1 / sr
    yf = fft(audio)
    xf = np.linspace(0.0, 1.0 / (2.0 * T), audio_len // 2)
    fftplot(yf, xf, audio_len)
    return yf, xf, audio_len

def convert_magnitude(yf, xf, audio_len):
    print("converting magnitude")

def collect_peaks(num_candidates):
    current_peaks = []  # list for peaks
    candidate_peak_freqs = []

    while len(current_peaks) < num_candidates:
        # grab maximum, set magnitude to 0+0j
        maxMagFreq = maxInFT(yf, xf, audio_len)

        # translate to key (candidate)
        candidate_peak = pitch(maxMagFreq)

        # check if same pitch already in current peaks
        if candidate_peak not in current_peaks:
            current_peaks.append(candidate_peak)
            candidate_peak_freqs.append((candidate_peak, maxMagFreq))
            print("Candidate Peak and Max Mag Freq:", candidate_peak, ",", maxMagFreq)

    return current_peaks, candidate_peak_freqs

# SET CONSTANTS

num_pitches = 1
num_candidates = 5

# LOAD SAMPLE/PREP BUFFER
data, sr = load('samples/glocka52.wav')

# COMPUTE FOURIER TRANSFORM (VIA DFT)
yf, xf, audio_len = computeFT(data, sr)

# CANDIDATE PEAK SELECTION
current_peaks, candidate_peak_freqs = collect_peaks(num_candidates)

#PRINT CURRENT CANDIDATE PEAKS (FREQS AND KEYS)
print(current_peaks)
print(candidate_peak_freqs)

# CANDIDATE PEAK LIKELIHOOD AND PITCH SELECTION (magnitude, harmonics, duration?)

# DURATION/END AND START NOTE MONITORING

'''
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

# 5 peaks glocka2:

# [('A6', 1759.4416562107906),
# # ('D8', 4757.277289836888),
# # ('B8', 8031.116687578419),
# # ('D#9', 9788.58218318695),
# # ('A#6', 1812.1392722710164)]
