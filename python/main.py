import glob
import MIDI_Pedal


midiFiles = glob.glob('../download/**/*.*', recursive=True)
applyPath = '../midi/'

for midiFile in midiFiles:
    newName = applyPath + midiFile.replace("../download/", "").replace("/", "_")
    print(newName)
    MIDI_Pedal.apply(midiFile, newName)
