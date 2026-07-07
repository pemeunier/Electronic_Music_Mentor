import mido
from mido import Message, MidiFile, MidiTrack

from electronic_music_mentor.midi.writer import MidWriter


def test_write_bassline_creates_valid_midi_file(tmp_path):
    writer = MidWriter()
    # A simple 4-note bassline: C2, C2, G2, F2 — one note per beat, 4 beats
    notes = [
        {"note": 36, "length_beats": 1.0, "velocity": 100},  # C2
        {"note": 36, "length_beats": 1.0, "velocity": 100},  # C2
        {"note": 43, "length_beats": 1.0, "velocity": 100},  # G2
        {"note": 41, "length_beats": 1.0, "velocity": 100},  # F2
    ]
    out_path = tmp_path / "bassline.mid"
    writer.write_bassline(notes, out_path, bpm=124)
    assert out_path.exists()
    mid = mido.MidiFile(out_path)
    assert mid.ticks_per_beat > 0
    # Count note_on events
    note_ons = [
        msg for track in mid.tracks
        for msg in track
        if msg.type == "note_on" and msg.velocity > 0
    ]
    assert len(note_ons) == 4


def test_write_bassline_respects_velocity(tmp_path):
    writer = MidWriter()
    notes = [
        {"note": 36, "length_beats": 1.0, "velocity": 80},
        {"note": 38, "length_beats": 1.0, "velocity": 110},
    ]
    out_path = tmp_path / "bassline.mid"
    writer.write_bassline(notes, out_path, bpm=124)
    mid = mido.MidiFile(out_path)
    note_ons = [
        msg for track in mid.tracks
        for msg in track
        if msg.type == "note_on" and msg.velocity > 0
    ]
    assert note_ons[0].velocity == 80
    assert note_ons[1].velocity == 110


def test_write_chords_creates_overlapping_notes(tmp_path):
    writer = MidWriter()
    # Two chords: Cmaj7 (C3 E3 G3 B3) and Fmaj7 (F3 A3 C4 E4), each 2 beats
    chords = [
        {"notes": [60, 64, 67, 71], "length_beats": 2.0, "velocity": 90},
        {"notes": [65, 69, 72, 76], "length_beats": 2.0, "velocity": 90},
    ]
    out_path = tmp_path / "chords.mid"
    writer.write_chords(chords, out_path, bpm=124)
    mid = mido.MidiFile(out_path)
    note_ons = [
        msg for track in mid.tracks
        for msg in track
        if msg.type == "note_on" and msg.velocity > 0
    ]
    assert len(note_ons) == 8  # 4 notes per chord * 2 chords


def test_write_percussion_uses_channel_9(tmp_path):
    writer = MidWriter()
    # A simple 4-on-the-floor kick: kick on every beat, hat on offbeats
    hits = [
        {"note": 36, "position_beats": 0.0, "length_beats": 0.5, "velocity": 110},  # kick
        {"note": 42, "position_beats": 0.5, "length_beats": 0.25, "velocity": 80},  # hat
        {"note": 36, "position_beats": 1.0, "length_beats": 0.5, "velocity": 110},  # kick
        {"note": 42, "position_beats": 1.5, "length_beats": 0.25, "velocity": 80},  # hat
        {"note": 36, "position_beats": 2.0, "length_beats": 0.5, "velocity": 110},  # kick
        {"note": 42, "position_beats": 2.5, "length_beats": 0.25, "velocity": 80},  # hat
        {"note": 36, "position_beats": 3.0, "length_beats": 0.5, "velocity": 110},  # kick
        {"note": 42, "position_beats": 3.5, "length_beats": 0.25, "velocity": 80},  # hat
    ]
    out_path = tmp_path / "percussion.mid"
    writer.write_percussion(hits, out_path, bpm=124)
    mid = mido.MidiFile(out_path)
    drum_notes = [
        msg for track in mid.tracks
        for msg in track
        if msg.type == "note_on" and msg.velocity > 0
    ]
    assert len(drum_notes) == 8
    # All drum notes should be on channel 9 (GM drum channel)
    for msg in drum_notes:
        assert msg.channel == 9