from math import log2, pow

A4 = 440
C0 = A4 * pow(2, -4.75)
key_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
octaves = list(range(11))
NOTES_IN_OCTAVE = len(key_names)

errors = {
    'program': 'Bad input, please refer this spec-\n',
}

def freq_to_note(freq):
    assert freq > 0, errors['program']
    h = round(12 * log2(freq / C0)) #can also use log(x)/log(2) to replace log2
    octave = h // 12
    n = h % 12
    return (key_names[n], octave)

def note_to_midi_pitch(note:str, octave:int):
    assert note in key_names, errors['program']
    assert octave in octaves, errors['program']

    midi_pitch_val = key_names.index(note)
    midi_pitch_val += (NOTES_IN_OCTAVE * octave)

    assert 0 <= midi_pitch_val <= 127, errors['program']

    return midi_pitch_val