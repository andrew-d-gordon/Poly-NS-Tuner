# IMPORTS
from librosa import load
from poly_note_detection import *
from freq_note_conversions import *
from scale_detection import *
from pitch_tracking import *
from audio_stream_test import decibelScale


# RETRIEVE samples_per_buffer/REMAINING SAMPLES OF FILE FOR POLY_NOTE_TUNER
def split_wav_into_chunk(data, location_in_audio, samples_per_buffer, need_full_buffer=True):
    if len(data) - location_in_audio > samples_per_buffer:
        return data[location_in_audio:location_in_audio+samples_per_buffer]  # PROCESS ONE SECOND OF AUDIO
    else:
        if need_full_buffer:
            return np.array([])  # RETURN EMPTY LIST, DO NOT PROCESS REMAINING SAMPLES
        else:
            return data[location_in_audio:]  # PROCESS REMAINING SAMPLES/LESS THAN N SECONDS OF AUDIO


# PRINTS FOR PEAK RETRIEVAL LISTS
def peak_list_prints(current_peaks, current_peaks_midi_pitch, current_peaks_freqs, current_peaks_amps):
    print("\nHere are feature lists for unique candidate peaks...\n")
    print("Current peaks notes:", current_peaks)
    print("Current peaks midi pitches:", current_peaks_midi_pitch)
    print("Current peaks freqs:", current_peaks_freqs)
    print("Current peaks amplitudes:", current_peaks_amps)


# PREDICTS NUM_PITCHES PITCH PREDICTIONS AS MIDI_PITCH LIST
def poly_note_tuner(data, sr, num_candidates, num_pitches):
    # COMPUTE FOURIER TRANSFORM (VIA DFT)
    ft, xf, audio_len = compute_ft(data, sr)

    # CONVERT FT COMPLEX VALS TO AMP
    ft_amp = convert_magnitude(ft)

    # CANDIDATE PEAK SELECTION
    current_peaks, current_peaks_freqs, current_peaks_amps = collect_peaks(ft_amp, xf, audio_len, num_candidates)
    current_peaks_midi_pitch = [note_to_midi_pitch(elem[0], elem[1]) for elem in current_peaks]

    # OPTIONAL PRINT CURRENT CANDIDATE PEAKS (NOTES, MIDI PITCHES, FREQS, AMPS)
    # peak_list_prints(current_peaks, current_peaks_midi_pitch, current_peaks_freqs, current_peaks_amps)

    # CANDIDATE PEAK LIKELIHOOD CALCULATION AND FUNDAMENTAL SELECTION
    current_peak_weights = compute_peak_likelihood(current_peaks_midi_pitch, current_peaks_amps, num_candidates)
    fundamental_predictions = retrieve_n_best_fundamentals(current_peak_weights, current_peaks, num_pitches)
    fundamental_predictions_mp = [(note_to_midi_pitch(elem[0], elem[1]), elem[2]) for elem in fundamental_predictions]
    print("Current fundamental predictions MP:", fundamental_predictions_mp)

    return fundamental_predictions_mp

    # DURATION/END AND START NOTE MONITORING, pass most recent guessed notes list...


# main()
# Set # of candidates pitches and # of pitches to predict,
# Load sample, process samples_per_buffer samples of audio through poly_note_tuner,
# Take predictions from poly_note_tuner, pitch track them, send pitch tracked notes through to scale detection.
def main():
    # CONSTANTS
    num_pitches = 7
    num_candidates = 50
    num_pitches_for_scale_detection = 3
    min_pitch_track_frames = 3  # minimum num of frames for pitch to track

    # LOAD SAMPLE/PREP BUFFER
    data, sr = load('samples/piano_chords_melody_Cm_vanilla.wav')
    audio_len = len(data)
    samples_per_buffer = 4096  # optionally seconds_per_buffer * sr
    hop_size = samples_per_buffer // 2

    # LOAD FIRST BUFFER OF AUDIO TO PROCESS, INIT FRAME_COUNT
    location_in_audio = 0
    audio_to_process = split_wav_into_chunk(data, location_in_audio, samples_per_buffer)
    frame_count = 0

    # INIT PITCH TRACK BUFFERS, SCALE DETECTION OBJECT
    pitch_track_notes_all = []  # HAS NOTES AS: [MP, MAG, START_FRAME]
    pitch_track_notes_set = []  # HAS NOTES AS: MP
    recorded_notes = []  # HAS NOTES AS: [MP, MAG, START_FRAME, END_FRAME]
    recorded_notes_mp = []  # HAS NOTES AS: MP
    all_note_predictions = []
    n = noteSet()

    while audio_to_process.size > 0:

        # PROCESS AUDIO, MOVE AUDIO FILE LOCATION PTR AHEAD
        new_note_predictions = poly_note_tuner(audio_to_process, sr, num_candidates, num_pitches)
        location_in_audio += hop_size

        ''' #optional note_predictions list to maintain, can replace note buffer for noteSet object
        for note in new_note_predictions:
            all_note_predictions.append(note[0])
        '''

        # FORWARD PREDICTED NOTES TO PITCH TRACK MAINTENANCE
        new_pt_ended_notes, pitch_track_notes_all, pitch_track_notes_set = \
            update_pitch_track(new_note_predictions, pitch_track_notes_all, pitch_track_notes_set, frame_count)

        print("New ended notes:", new_pt_ended_notes)

        # append new_ended_notes to recorded lists (one with mp, mag, start, and end data and one with just mp)
        for note in new_pt_ended_notes:
            # FILTER OUT NOTES WITH LESS THAN min_pitch_track_frames DURATION, ADD NOTES WITH GOOD LEN TO RECORDED_NOTES
            if note[3] - note[2] > min_pitch_track_frames:
                recorded_notes.append(note)
                recorded_notes_mp.append(note[0])

        print("\nNumber of tracked note predictions:", len(recorded_notes_mp))
        print("Current tracked note prediction history:", recorded_notes_mp)

        # RUN SCALE PREDICTION IF ENOUGH NOTES IN PITCH TRACK BUFFER
        if len(recorded_notes_mp) > num_pitches_for_scale_detection:
            n.setNoteAmounts(recorded_notes_mp)
            n.findClosestScale()
            print(n.closestScale)

        # CHECK IF MORE AUDIO TO PROCESS, IF NOT, EXIT
        if audio_len - location_in_audio > 0:
            audio_to_process = split_wav_into_chunk(data, location_in_audio, samples_per_buffer)
            frame_count += 1
        else:
            break

    print("Fin")


if __name__ == "__main__":
    main()
