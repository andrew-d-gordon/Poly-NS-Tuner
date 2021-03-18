import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy.signal import blackman
import numpy as np
import math
from freq_note_conversions import freq_to_note
# from scipy.io import wavfile as wav
import heapq

# CONSTANTS

# Harmonic Series based on, e.g. C3, overtones = C4(+12), G4(+19), C5(+24), and E5(+28)...
harmonic_series_mp = [12, 19, 24, 28, 31]
harmonic_series_weight = [2, 1.8, 1.6, 1.4, 1.2]

# Formant weights/mp intervals, soon...

# FUNCTIONS

def max_in_ft(yf, xf, audio_len):
    max_mag_idx = np.argmax(yf[:audio_len // 2], axis=0)  # get max idx
    # print(maxMagIdx, " ", yf[maxMagIdx], " ", xf[maxMagIdx])
    max_amp = yf[max_mag_idx]
    yf[max_mag_idx] = 0
    return xf[max_mag_idx], max_amp


def fft_plot(yf, xf, audio_len):
    fig, ax = plt.subplots()
    ax.plot(xf, 2.0 / audio_len * np.abs(yf[:audio_len // 2]))
    plt.grid()
    plt.xlabel("Frequency-->")
    plt.ylabel("Magnitude")
    return plt.show()


def compute_ft(audio, sr):
    audio_len = len(audio)
    window = blackman(audio_len)  # optional windowing to aide spectral leakage
    yf = fft(audio * window)
    T = 1 / sr
    xf = np.linspace(0.0, 1.0 / (2.0 * T), audio_len // 2)
    #fft_plot(yf, xf, audio_len)  # Optional fft plot
    return yf, xf, audio_len


def convert_magnitude(yf):
    return [math.sqrt(elem.real ** 2 + elem.imag ** 2) for elem in yf]


def collect_peaks(yf, xf, audio_len, num_candidates):
    current_peaks = []  # list for peak notes and scales
    current_peaks_freq = []  # list for peak frequencies
    current_peaks_amps = []  # list for peak amplitudes

    while len(current_peaks) < num_candidates:
        # Grab maximum magnitude and frequency, magnitude for frequency set to 0, initial mag returned to candidate_mag
        max_mag_freq, candidate_mag = max_in_ft(yf, xf, audio_len)

        # Translate to key (candidate)
        candidate_peak_ns = freq_to_note(max_mag_freq)

        # Check if same pitch already in current peaks
        if candidate_peak_ns not in current_peaks:
            current_peaks.append(candidate_peak_ns)
            current_peaks_freq.append(max_mag_freq)
            current_peaks_amps.append(candidate_mag)
            print("Candidate Peak Note, Freq, Magnitude (amp):", candidate_peak_ns, "|", max_mag_freq,
                  "|", candidate_mag)

    return current_peaks, current_peaks_freq, current_peaks_amps


def retrieve_n_best_fundamentals(current_peak_weights, current_peaks, num_pitches):
    fundamental_predictions = []
    pitches_selected = 0
    while pitches_selected < num_pitches:
        # Select largest weight, find idx and corresponding note, append to prediction list
        best_f0_idx = np.argmax(current_peak_weights)
        fundamental_predictions.append((current_peaks[best_f0_idx], current_peak_weights[best_f0_idx]))

        # Void value at most recent max, continue search for f0's until num_pitches f0's have been found
        current_peak_weights[best_f0_idx] = 0
        pitches_selected += 1

    return fundamental_predictions


def peak_to_f_harmonic_weight(f_mp, p_mp):  # Provides value of ti*ni
    if p_mp < f_mp:  # Base Case, returns if peak < f0
        return 1

    for idx in range(len(harmonic_series_mp)):
        if f_mp+harmonic_series_mp[idx] == p_mp:
            return harmonic_series_weight[idx]  # Peak is a multiple of F0

    # Peak is not a multiple of f0
    return 1


'''
Calculation behind weight function for peak's likelihood to be fundamental...

L(f) = Summation(i=0,k){ai*ti*ni}
Where k is number of peaks in the spectrum,
-ai is a factor depending on the amplitude of the ith peak,
-ti depends on how closely the ith peak is tuned to a multiple of fi
-ni depends on whether the peak is closest to a low or high multiple of f
'''


def compute_peak_likelihood(current_peaks_mp, current_peaks_amps, num_candidates):
    current_peak_weights = []

    for f in range(num_candidates):
        f_weight = 0
        for i in range(num_candidates):
            peak_weight = 0  # ai*ni*ti
            if i != f:  # skip fundamental whose likelihood is being calculated
                peak_weight += current_peaks_amps[i]  # ai
                peak_weight *= peak_to_f_harmonic_weight(current_peaks_mp[f], current_peaks_mp[i])  # ni*ti
                f_weight += peak_weight
            else:
                continue

        #print("This is weight for f:", current_peaks_mp[f], "->", f_weight)
        current_peak_weights.append(f_weight)

    return current_peak_weights
