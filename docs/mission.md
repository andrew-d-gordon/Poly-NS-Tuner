# Mission for the Poly Note Tuner
The reason for the existence of this library (and soon to be plugin) is to provide producers, musicians or any auditory 
inclined personnel with their own, digital version of perfect pitch. The ability to chop and work with multiple samples
or even stems from other artists most often involves the work of parsing scale and pitch information. Having the ability
to determine real-time, pitch and scale information is a large time save for the process of working with samples. 

While current plugins for scale detection and monophonic pitch detection are useful in their own right, I have yet to 
find a plugin which can replace my daily task of noodling around to get the melodies or chords out of samples. This is
why on top of polyphonic pitch detection in real-time, Poly NS Tuner can make scale-detection predictions and generate
MIDI files (utilizing pitch tracking) for audio passed through it.

As of today, 1/16/2022, the Poly NS Tuner requires work to tune its peak weighting algorithms within 
`poly_note_detection.py` as well as it's pitch tracking algorithm to throw away fundamental guesses with insufficient 
weighting. In specific to `poly_note_detection.py`, it's process of calculating harmonic weighting needs to be 
refactored to a function that returns scores ranging from 0->1 in relation to how many frequencies fall close to a 
candidate fundamental's harmonic series.

Over the coming months I hope to closer align the project's algorithms to the work done on `Fiddle` (link to 
that research in README.md), which should have positive downstream effects on the current pitch-tracking and scale 
detection algorithms.

Features to be implemented going forward are Machine Learning models to ratify scale-detection decisions (utilizing 
chroma graphs), and replacing the current DIY pitch-track algorithm with an industry standard pitch-track algorithm.
An offline version of Poly NS Tuner may also be implemented with the use of a phase vocoder (something which to my 
current understanding is not viable in real-time settings).
