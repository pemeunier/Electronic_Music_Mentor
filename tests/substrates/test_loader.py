from pathlib import Path

import pytest

from electronic_music_mentor.substrates.loader import load_theory_document, LoadError


def test_load_valid_theory_document(tmp_path):
    content = """---
topic: Voice-leading
summary: Principles of smooth voice-leading between chords.
principles:
  - minimize movement between voices
  - avoid parallel fifths in classical contexts
  - in electronic music, bass movement can be wide if it carries the harmony
electronic_music_notes: When bass is the harmony, voice-leading rules relax.
examples:
  - i-VI-III-VII progression in minor with static-bass voice-leading
---

# Voice-leading

Some prose body here.

## Sources

- Aldwell & Schachter, Harmony & Voice Leading
"""
    path = tmp_path / "voice-leading.md"
    path.write_text(content)
    doc = load_theory_document(path)
    assert doc["topic"] == "Voice-leading"
    assert doc["summary"] == "Principles of smooth voice-leading between chords."
    assert len(doc["principles"]) == 3
    assert "minimize movement between voices" in doc["principles"][0]
    assert isinstance(doc["examples"], list)
    assert "i-VI-III-VII" in doc["examples"][0]
    assert doc["body"].startswith("# Voice-leading")
    assert "## Sources" in doc["body"]


def test_load_theory_document_missing_fields_raises(tmp_path):
    content = """---
topic: Voice-leading
summary: Some summary.
---

# Voice-leading

Body.
"""
    path = tmp_path / "voice-leading.md"
    path.write_text(content)
    with pytest.raises(LoadError) as exc_info:
        load_theory_document(path)
    assert "missing" in str(exc_info.value).lower() or "principles" in str(exc_info.value).lower()


def test_load_theory_document_no_front_matter_raises(tmp_path):
    content = "# Voice-leading\n\nNo front-matter here.\n"
    path = tmp_path / "voice-leading.md"
    path.write_text(content)
    with pytest.raises(LoadError) as exc_info:
        load_theory_document(path)
    assert "front-matter" in str(exc_info.value).lower() or "yaml" in str(exc_info.value).lower()


def test_load_theory_document_includes_sources_section(tmp_path):
    content = """---
topic: Test
summary: A test document.
principles:
  - principle one
electronic_music_notes: Notes here.
examples:
  - example one
---

# Test

Body.

## Sources

- Some Book by Some Author
"""
    path = tmp_path / "test.md"
    path.write_text(content)
    doc = load_theory_document(path)
    assert "## Sources" in doc["body"]
    assert "Some Book by Some Author" in doc["body"]


from electronic_music_mentor.substrates.loader import load_genre_profile


def test_load_valid_genre_profile(tmp_path):
    content = """---
name: Dub Techno
tempo_range:
  min: 120
  max: 130
  feel: "hypnotic, patient"
rhythmic_conventions:
  - four-on-the-floor kick
  - offbeat hats
  - sparse percussion
harmonic_conventions:
  - static harmony
  - minor tonality
  - chord stabs with long reverb
textural_sonic_conventions:
  - haze
  - reverb-drenched
  - filter movement
arrangement_conventions:
  - long builds
  - atmospheric breakdowns
  - minimal section changes
spirit: >
  Hypnotic immersion through repetition and slow change. Good examples sustain a single
  idea with patience; lazy examples just repeat a loop without evolution.
common_failure_modes:
  - no evolution
  - static loop without filter movement
  - overcrowded mid
---

# Dub Techno

Some prose body here.

## Sources

- Mark Jamieson, electronic music production literature
"""
    path = tmp_path / "dub-techno.md"
    path.write_text(content)
    profile = load_genre_profile(path)
    assert profile["name"] == "Dub Techno"
    assert profile["tempo_range"]["min"] == 120
    assert profile["tempo_range"]["max"] == 130
    assert len(profile["rhythmic_conventions"]) == 3
    assert isinstance(profile["harmonic_conventions"], list)
    assert len(profile["spirit"]) >= 80
    assert profile["body"].startswith("# Dub Techno")
    assert "## Sources" in profile["body"]


def test_load_genre_profile_missing_fields_raises(tmp_path):
    content = """---
name: Dub Techno
tempo_range:
  min: 120
  max: 130
  feel: "hypnotic"
---

# Dub Techno

Body.
"""
    path = tmp_path / "dub-techno.md"
    path.write_text(content)
    with pytest.raises(LoadError) as exc_info:
        load_genre_profile(path)
    assert "missing" in str(exc_info.value).lower() or "rhythmic" in str(exc_info.value).lower()


def test_load_genre_profile_spirit_too_short_raises(tmp_path):
    content = """---
name: Test Genre
tempo_range:
  min: 120
  max: 130
  feel: "test"
rhythmic_conventions:
  - kick
harmonic_conventions:
  - minor
textural_sonic_conventions:
  - haze
arrangement_conventions:
  - builds
spirit: "Too short."
common_failure_modes:
  - boring
---

# Test Genre

Body.

## Sources

- Some Source
"""
    path = tmp_path / "test.md"
    path.write_text(content)
    with pytest.raises(LoadError) as exc_info:
        load_genre_profile(path)
    assert "spirit" in str(exc_info.value).lower()