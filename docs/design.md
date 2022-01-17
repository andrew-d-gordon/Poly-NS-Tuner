# Design

**Overview**

Poly NS Tuner is currently a Python library (being developed in 3.6^) which can be run from main.py. Input files can
be specified for the run (input audio) and if specified midi files can be generated from the notes detected, and
console output will show scale detection information for given frames being analyzed. The number of fundamentals
you would like to parse from any given instant of the audio is also available to you (however if not enough "valid" 
fundamentals are present then less than specified are detected).

**Vocabulary**

- `Fundamental Pitch`: A note which is not an overtone of another note and whose frequencies are stronger
- `Sample`: A sample of audio is an instantaneous number representing the amplitude of a signal at a given time.
- `Sample Rate`: The rate at which samples are taken for a given audio file. e.g. 48Khz = 48,000 Samples / Sec.
- `Frame`: A list of a specific number of samples.
- `Valid Candidate`: A pitch which has enough weight to be a fundamental pitch (in relation to its amplitude, harmonic
weight, and its weight compared to other candidates in the same frame)

**Use**

To be written. Addition of flags to improve usability to be added soon.

**Modules**

- `main.py`: Primary driver for the Poly NS Tuner, utilizes other modules to orchestrate detection of pitches, scale
detection and pitch tracking to midi output.
- `poly_note_detection.py`: Provides functions turning batches of samples (frames) to fourier transforms, computing the
likelihood of what fundamental pitches are present in the frame.
- `scale_detection.py`: Provides a class and functions for determining what the scale is for a set of detected pitches.
- `pitch_tracking.py`: Provides functionality for tracking detected notes across time, provides notes with start and 
stop times based on when they first were detected and when they stopped being detected.
- `generating_midi_file.py`: Functionality for taking a set of notes with start and stop points and writing it to a MIDI
file.
- `freq_note_conversions.py`: Functions for converting frequency to musical notes and vice versa.
- `audio_stream_test.py`: Provides examples of working with real time audio (default computer input)
- `audio_wave_buffer_test.py`: Provides additional examples of working with real time audio (default computer input)
