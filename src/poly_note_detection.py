import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy.signal import blackman
import numpy as np
import math
from freq_note_conversions import freq_to_note
# from scipy.io import wavfile as wav
import heapq


def maxInFT(yf, xf, audio_len):
    max_mag_idx = np.argmax(yf[:audio_len // 2], axis=0)  # get max idx
    #print(maxMagIdx, " ", yf[maxMagIdx], " ", xf[maxMagIdx])
    max_amp = yf[max_mag_idx]
    yf[max_mag_idx] = 0
    return xf[max_mag_idx], max_amp


def fftplot(yf, xf, audio_len):
    fig, ax = plt.subplots()
    ax.plot(xf, 2.0 / audio_len * np.abs(yf[:audio_len // 2]))
    plt.grid()
    plt.xlabel("Frequency-->")
    plt.ylabel("Magnitude")
    return plt.show()


def compute_ft(audio, sr):
    audio_len = len(audio)
    T = 1 / sr
    window=blackman(audio_len)  # optional windowing to aide spectral leakage
    yf = fft(audio*window)
    xf = np.linspace(0.0, 1.0 / (2.0 * T), audio_len // 2)
    #fftplot(yf, xf, audio_len) #optional plot
    return yf, xf, audio_len


def convert_magnitude(yf, audio_len):
    yfconvert = [math.sqrt(elem.real**2 + elem.imag**2) for elem in yf]
    return yfconvert


def collect_peaks(yf, xf, audio_len, num_candidates):
    current_peaks = []  # list for peak notes and scales
    current_peaks_freq=[] # list for peak frequencies
    current_peaks_amps=[] # list for peak amplitudes

    while len(current_peaks) < num_candidates:
        # grab maximum magnitude and frequency, magnitude for frequency set to 0, initial mag returned to candidate_mag
        max_mag_freq, candidate_mag = maxInFT(yf, xf, audio_len)

        # translate to key (candidate)
        candidate_peak_ns = freq_to_note(max_mag_freq)

        # check if same pitch already in current peaks
        if candidate_peak_ns not in current_peaks:
            current_peaks.append(candidate_peak_ns)
            current_peaks_freq.append(max_mag_freq)
            current_peaks_amps.append(candidate_mag)
            print("Candidate Peak, Candidate Freq, Candidate Magnitude (amp):", candidate_peak_ns, "|", max_mag_freq, "|", candidate_mag)

    return current_peaks, current_peaks_freq, current_peaks_amps


def compute_peak_likelihood(peak_notes, peak_freqs, peak_mags):
    print("computing likelihood")
    '''
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

    #pieces:
    #1)amplitude decision, amp or db? what is threshold?
    #2)determine if self is harmonic overtone, if at least half db of "fundamental" do not dock weight
    #3)determine value of each overtone, if first octave *2, if first octave fifth *1.5, second octave *1, second octave third *.5
    #4)set exit decision criteria, how harsh to dock multiples of other frequencies, amplitude threshold, ...
    #overtone series: e.g. C3 then the overtones C4, G4, C5, and E5

    '''[('G', 4), ('D#', 4), ('D', 4), ('D', 5), ('G#', 4), ('F', 4), ('F', 5), ('D#', 5), ('E', 4), ('G#', 5)]'''
