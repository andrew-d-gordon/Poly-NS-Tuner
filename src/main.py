# IMPORTS
from librosa import load
from poly_note_detection import *
from freq_note_conversions import *
from scale_detection import *
from audio_stream_test import decibelScale


# RUN ONE SECOND/REMAINING SAMPLES OF FILE TO POLY_NS_TUNER
def split_wav_by_seconds(data, location_in_audio, seconds_per_buffer):
    if len(data) - location_in_audio > seconds_per_buffer:
        return data[location_in_audio:location_in_audio+seconds_per_buffer]  # PROCESS ONE SECOND OF AUDIO
    else:
        return data[location_in_audio:]  # PROCESS REMAINING SAMPLES/LESS THAN ONE SEC AUDIO INPUT


# PREDICTS NUM_PITCHES PITCH PREDICTIONS AS MIDI_PITCH LIST
def poly_note_tuner(data, sr, num_candidates, num_pitches):
    # COMPUTE FOURIER TRANSFORM (VIA DFT)
    ft, xf, audio_len = compute_ft(data, sr)

    # CONVERT FT COMPLEX VALS TO AMP
    ft_amp = convert_magnitude(ft)

    # CANDIDATE PEAK SELECTION
    current_peaks, current_peaks_freqs, current_peaks_amps = collect_peaks(ft_amp, xf, audio_len, num_candidates)
    current_peaks_midi_pitch = [note_to_midi_pitch(elem[0], elem[1]) for elem in current_peaks]

    # PRINT CURRENT CANDIDATE PEAKS (NOTES, MIDI PITCHES, FREQS, AMPS)
    print("\nHere are feature lists for unique candidate peaks...\n")
    print("Current peaks notes:", current_peaks)
    print("Current peaks midi pitches:", current_peaks_midi_pitch)
    print("Current peaks freqs:", current_peaks_freqs)
    print("Current peaks amplitudes:", current_peaks_amps)

    # CANDIDATE PEAK LIKELIHOOD CALCULATION AND FUNDAMENTAL SELECTION
    current_peak_weights = compute_peak_likelihood(current_peaks_midi_pitch, current_peaks_amps, num_candidates)
    print("\nCurrent peaks weights:", current_peak_weights)

    fundamental_predictions = retrieve_n_best_fundamentals(current_peak_weights, current_peaks, num_pitches)
    fundamental_predictions_mp = [note_to_midi_pitch(elem[0], elem[1]) for elem in fundamental_predictions]
    print("Current fundamental predictions:", fundamental_predictions)

    return fundamental_predictions_mp

    # DURATION/END AND START NOTE MONITORING, pass most recent guessed notes list...


def main():
    # CONSTANTS
    num_pitches = 4
    num_candidates = 50
    num_pitches_for_scale_detection = 4
    seconds_per_buffer = 2

    # LOAD SAMPLE/PREP BUFFER
    data, sr = load('samples/piano_chords_melody_Cm_vanilla.wav')
    audio_len = len(data)
    samples_per_buffer = seconds_per_buffer*sr

    # LOAD FIRST BUFFER OF AUDIO TO PROCESS
    location_in_audio = 0
    audio_to_process = split_wav_by_seconds(data, location_in_audio, samples_per_buffer)

    # INIT SCALE DETECTION NOTE BUFFER AND SCALE DETECTION OBJECT
    all_note_predictions = []
    n = noteSet()

    while audio_to_process.size > 0:

        # PROCESS AUDIO, MOVE AUDIO FILE LOCATION PTR AHEAD
        new_note_predictions = poly_note_tuner(audio_to_process, sr, num_candidates, num_pitches)
        location_in_audio += samples_per_buffer

        # APPEND NOTES WHICH WERE PREDICTED TO SCALE GUESS LIST
        for note in new_note_predictions:
            all_note_predictions.append(note)
        print("\nNumber of note predictions:", len(all_note_predictions))
        print("Current note prediction history:", all_note_predictions)

        # RUN SCALE PREDICTION IF ENOUGH NOTES IN BUFFER
        if len(all_note_predictions) > num_pitches_for_scale_detection:
            n.setNoteAmounts(all_note_predictions)
            n.findClosestScale()
            print(n.closestScale)

        # CHECK IF MORE AUDIO TO PROCESS, IF NOT, EXIT
        if audio_len - location_in_audio > 0:
            audio_to_process = split_wav_by_seconds(data, location_in_audio, samples_per_buffer)
        else:
            break

    print("Fin")


if __name__ == "__main__":
    main()
