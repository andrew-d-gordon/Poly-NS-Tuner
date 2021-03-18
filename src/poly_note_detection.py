import matplotlib.pyplot as plt
from librosa import load
from scipy.fftpack import fft
import numpy as np
import math
from freq_to_note import pitch
# from scipy.io import wavfile as wav
import heapq


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

def convert_magnitude(yf, audio_len):
    yfconvert = [math.sqrt(elem.real**2 + elem.imag**2) for elem in yf]
    return yfconvert

def collect_peaks(yf, xf, audio_len, num_candidates):
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
