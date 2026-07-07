"""MidWriter: writes .mid files for basslines, chord stabs, and percussion.

All methods take a list of note specs and an output path, and write a
standard MIDI file the user can import into their DAW.
"""

from mido import MidiFile, MidiTrack, Message, MetaMessage, bpm2tempo


class MidWriter:
    """Writes MIDI files for Electronic Music Mentor skills."""

    def __init__(self, ticks_per_beat: int = 480):
        self.ticks_per_beat = ticks_per_beat

    def write_bassline(
        self,
        notes: list[dict],
        out_path,
        bpm: int = 124,
        channel: int = 0,
        program: int = 33,  # 33 = Electric Bass (finger)
    ) -> None:
        """Write a bassline to a .mid file.

        Each note is a dict with keys:
        - note: MIDI note number (e.g., 36 = C2)
        - length_beats: duration in beats (e.g., 1.0 = quarter note)
        - velocity: 0-127
        """
        mid = MidiFile(ticks_per_beat=self.ticks_per_beat)
        track = MidiTrack()
        mid.tracks.append(track)

        tempo = bpm2tempo(bpm)
        track.append(MetaMessage("set_tempo", tempo=tempo))
        track.append(Message("program_change", program=program, channel=channel))

        for note_spec in notes:
            note = note_spec["note"]
            length = int(note_spec["length_beats"] * self.ticks_per_beat)
            velocity = note_spec.get("velocity", 100)
            track.append(Message("note_on", note=note, velocity=velocity, channel=channel, time=0))
            track.append(Message("note_off", note=note, velocity=0, channel=channel, time=length))

        mid.save(out_path)