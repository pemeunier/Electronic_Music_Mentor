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

    def write_chords(
        self,
        chords: list[dict],
        out_path,
        bpm: int = 124,
        channel: int = 0,
        program: int = 4,  # 4 = Electric Piano 1
    ) -> None:
        """Write chord stabs/pads to a .mid file.

        Each chord is a dict with keys:
        - notes: list of MIDI note numbers
        - length_beats: duration in beats
        - velocity: 0-127
        """
        mid = MidiFile(ticks_per_beat=self.ticks_per_beat)
        track = MidiTrack()
        mid.tracks.append(track)

        tempo = bpm2tempo(bpm)
        track.append(MetaMessage("set_tempo", tempo=tempo))
        track.append(Message("program_change", program=program, channel=channel))

        for chord_spec in chords:
            chord_notes = chord_spec["notes"]
            length = int(chord_spec["length_beats"] * self.ticks_per_beat)
            velocity = chord_spec.get("velocity", 90)
            # All notes on simultaneously
            for note in chord_notes:
                track.append(Message("note_on", note=note, velocity=velocity, channel=channel, time=0))
            # All notes off after the length
            for i, note in enumerate(chord_notes):
                track.append(Message("note_off", note=note, velocity=0, channel=channel, time=length if i == 0 else 0))

        mid.save(out_path)

    def write_percussion(
        self,
        hits: list[dict],
        out_path,
        bpm: int = 124,
    ) -> None:
        """Write a percussion pattern to a .mid file on GM channel 9 (drums).

        Each hit is a dict with keys:
        - note: GM percussion note number (36 = kick, 42 = closed hat, etc.)
        - position_beats: when in the bar the hit occurs (0.0 = beat 1)
        - length_beats: duration
        - velocity: 0-127

        Hits must be sorted by position_beats before calling.
        """
        mid = MidiFile(ticks_per_beat=self.ticks_per_beat)
        track = MidiTrack()
        mid.tracks.append(track)

        tempo = bpm2tempo(bpm)
        track.append(MetaMessage("set_tempo", tempo=tempo))
        track.append(Message("program_change", program=0, channel=9))

        sorted_hits = sorted(hits, key=lambda h: h["position_beats"])
        cumulative_beats = 0.0

        for hit in sorted_hits:
            position = hit["position_beats"]
            length = int(hit["length_beats"] * self.ticks_per_beat)
            velocity = hit.get("velocity", 100)
            note = hit["note"]
            delta = int((position - cumulative_beats) * self.ticks_per_beat)
            track.append(Message("note_on", note=note, velocity=velocity, channel=9, time=max(0, delta)))
            track.append(Message("note_off", note=note, velocity=0, channel=9, time=length))
            cumulative_beats = position + hit["length_beats"]

        mid.save(out_path)