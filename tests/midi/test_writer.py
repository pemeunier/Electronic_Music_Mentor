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