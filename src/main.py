# IMPORTS
from librosa import load
from poly_note_detection import *
from freq_note_conversions import *
from scale_detection import *
from audio_stream_test import decibelScale

# CONSTANTS
num_pitches = 1
num_candidates = 20

# LOAD SAMPLE/PREP BUFFER
data, sr = load('samples/piano_chords_melody_Cm_vanilla.wav')

def poly_ns_tuner_main(data, sr):

    # COMPUTE FOURIER TRANSFORM (VIA DFT)
    ft, xf, audio_len = compute_ft(data, sr)

    # CONVERT FT COMPLEX VALS TO AMP
    ft_amp = convert_magnitude(ft)

    # CANDIDATE PEAK SELECTION
    current_peaks, current_peaks_freqs, current_peaks_amps = collect_peaks(ft_amp, xf, audio_len, num_candidates)
    current_peaks_midi_pitch = [note_to_midi_pitch(elem[0], elem[1]) for elem in current_peaks]  # create list w/midi pitch

    #PRINT CURRENT CANDIDATE PEAKS (NOTES, MIDI PITCHES, FREQS, AMPS)
    print("\nHere are feature lists for unique candidate peaks...\n")
    print("Current peaks notes:", current_peaks)
    print("Current peaks midi pitches:", current_peaks_midi_pitch)
    print("Current peaks freqs:", current_peaks_freqs)
    print("Current peaks amplitudes:", current_peaks_amps)

    # CANDIDATE PEAK LIKELIHOOD CALCULATION AND FUNDAMENTAL SELECTION
    current_peak_weights = compute_peak_likelihood(current_peaks_midi_pitch, current_peaks_amps, num_candidates)
    #print("\nCurrent peaks weights:", current_peak_weights)

    fundamental_predictions = retrieve_n_best_fundamentals(current_peak_weights, current_peaks, num_pitches)
    print("Current fundamental predictions:", fundamental_predictions)

    # DURATION/END AND START NOTE MONITORING

    #  ================================================= N/A

    # SCALE DETECTION (current_peaks_midi_pitch is input)
    n = noteSet()
    n.setNoteAmounts(current_peaks_midi_pitch) #ideally feed in fundamental_predictions instead (once stream works)
    n.findClosestScale()
    print(n.closestScale)

#test call
poly_ns_tuner_main(data, sr)