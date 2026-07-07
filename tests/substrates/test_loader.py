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