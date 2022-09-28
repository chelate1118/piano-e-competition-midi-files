import pretty_midi


def apply(input_path: str, output_path: str):
    midiObject = _midiObj(input_path)
    midiObject.write(output_path)


class _pedal:
    def __init__(self, on, off):
        self.on = on
        self.off = off

    def __str__(self):
        return f"({self.on}, {self.off})"

    def __is_in(self, note: pretty_midi.Note):
        return self.on < note.end <= self.off

    def __apply(self, note: pretty_midi.Note):
        if self.__is_in(note):
            note.end = self.off

    def apply(self, notes):
        for note in notes:
            self.__apply(note)


class _midiObj:
    pedalRange = []

    def __init__(self, path: str):
        self.midi = pretty_midi.PrettyMIDI(path)
        self.midi.remove_invalid_notes()
        self.__concatenate()
        self.__apply_and_remove_pedal()

    def __concatenate(self):
        self.__concatenate_notes()
        self.__concatenate_control()
        self.midi.instruments = self.midi.instruments[0:1]

    def __apply_and_remove_pedal(self):
        self.__set_pedal_range()
        self.__apply_pedal()
        self.__remove_all_pedal()

    def __concatenate_notes(self):
        for instrument in self.midi.instruments[1:]:
            self.midi.instruments[0].notes += instrument.notes
        self.midi.instruments[0].notes.sort(key=lambda x: x.start)

    def __concatenate_control(self):
        for instrument in self.midi.instruments[1:]:
            self.midi.instruments[0].control_changes += instrument.control_changes
        self.midi.instruments[0].control_changes.sort(key=lambda x: (x.time, x.value))

    def __set_pedal_range(self):
        current = False
        first = False
        before = 0.0
        for control in self.midi.instruments[0].control_changes.copy():
            if control.number == 64:
                if not first:
                    current = (control.value >= 64)
                    if current:
                        before = control.time
                else:
                    if (control.value >= 64) == current:
                        self.midi.instruments[0].control_changes.remove(control)
                    else:
                        if current:
                            self.pedalRange.append(_pedal(before, control.time))
                        else:
                            before = control.time
                        current = (control.value >= 64)
                first = True

    def __apply_pedal(self):
        for pedal in self.pedalRange:
            pedal.apply(self.midi.instruments[0].notes)

    def __remove_all_pedal(self):
        for control in self.midi.instruments[0].control_changes.copy():
            if control.number == 64:
                self.midi.instruments[0].control_changes.remove(control)

    def write(self, path: str):
        self.midi.write(path)