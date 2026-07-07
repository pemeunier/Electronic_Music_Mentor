# Electronic Music Mentor — Knowledge Base: Theory Substrate Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the `theory` substrate — 8 music-theory documents covering voice-leading, diatonic harmony, chromatic harmony, bass-as-harmony, static harmony, rhythmic subdivision, phrase and form, and tension/release, each written in the project's own words with electronic-music-specific notes and source attributions, plus a loader that parses the markdown files into dicts for validation.

**Architecture:** Each theory document is a markdown file with YAML front-matter (the structured fields the validator checks) and a prose body (the elaboration skills read). A `loader` module parses the front-matter into a dict, runs the validator, and returns the parsed content. Documents are researched from authoritative music-theory references and rewritten in original prose.

**Tech Stack:** Python 3.12, PyYAML (front-matter parsing), pytest (testing), Markdown (content format).

---

## File Structure

```
Electronic_Music_Mentor/
├── pyproject.toml                                    # (modify) add pyyaml dependency
├── src/electronic_music_mentor/substrates/
│   ├── validator.py                                  # (exists) validates dicts
│   └── loader.py                                     # (new) parses markdown front-matter → dict + validates
├── tests/substrates/
│   ├── test_validator.py                             # (exists)
│   └── test_loader.py                                # (new) loader tests
├── knowledge/theory/
│   ├── README.md                                     # (modify) update topic list to link to files
│   ├── voice-leading.md                              # (new) Task 2
│   ├── diatonic-harmony.md                           # (new) Task 3
│   ├── chromatic-harmony.md                          # (new) Task 4
│   ├── bass-as-harmony.md                            # (new) Task 5
│   ├── static-harmony.md                             # (new) Task 6
│   ├── rhythmic-subdivision.md                       # (new) Task 7
│   ├── phrase-and-form.md                            # (new) Task 8
│   └── tension-and-release.md                        # (new) Task 9
```

Responsibilities:
- `src/electronic_music_mentor/substrates/loader.py` — parses markdown files with YAML front-matter into dicts, runs the appropriate validator, returns the parsed content. Used by skills to load substrates and by the content-building process to validate documents.
- `knowledge/theory/*.md` — one file per theory topic. Each has YAML front-matter (topic, summary, principles list, electronic_music_notes, examples list) validated by `validate_theory_document`, a prose body elaborating the topic with electronic-music focus, and a `## Sources` section with attributions.

---

## Document Format

Every theory document follows this format:

```markdown
---
topic: Voice-leading
summary: <one-sentence summary of the topic>
principles:
  - <principle 1>
  - <principle 2>
  - <principle 3>
electronic_music_notes: <how this topic plays differently in electronic music>
examples:
  - <example 1 — a progression, technique, or listening reference>
  - <example 2>
---

# <Topic Name>

<Prose elaboration — 200-400 words. This is the main content a skill reads. Must be original writing informed by authoritative sources, not reproduced text. Focus on electronic music application where relevant.>

## Sources

- <Author, Title, Publisher/URL> — <what was drawn from this source>
- <Author, Title, Publisher/URL> — <what was drawn from this source>
```

---

### Task 1: Add PyYAML dependency and build the loader

**Files:**
- Modify: `pyproject.toml` (add pyyaml to dependencies)
- Create: `src/electronic_music_mentor/substrates/loader.py`
- Create: `tests/substrates/test_loader.py`

- [ ] **Step 1: Add pyyaml to pyproject.toml**

In `pyproject.toml`, change the dependencies section from:
```toml
dependencies = [
    "mido>=1.3.0",
]
```
to:
```toml
dependencies = [
    "mido>=1.3.0",
    "pyyaml>=6.0",
]
```

- [ ] **Step 2: Install pyyaml**

Run: `.venv/bin/pip install pyyaml`
Expected: pyyaml installed.

- [ ] **Step 3: Write the failing test for the loader**

`tests/substrates/test_loader.py`:
```python
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
```

- [ ] **Step 4: Run test to verify it fails**

Run: `.venv/bin/pytest tests/substrates/test_loader.py -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'electronic_music_mentor.substrates.loader'"

- [ ] **Step 5: Write the implementation**

`src/electronic_music_mentor/substrates/loader.py`:
```python
"""Loader for knowledge-base substrate files.

Parses markdown files with YAML front-matter into dicts, runs the
appropriate validator, and returns the parsed content (front-matter
fields plus the prose body).
"""

import re
from pathlib import Path

import yaml

from .validator import validate_theory_document, ValidationError


class LoadError(Exception):
    """Raised when a substrate file cannot be loaded or is invalid."""


FRONT_MATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)$", re.DOTALL)


def load_theory_document(path: Path) -> dict:
    """Load a theory document from a markdown file with YAML front-matter.

    Returns a dict with the front-matter fields plus a 'body' key containing
    the prose content (everything after the front-matter).

    Raises LoadError if the file has no front-matter, fails to parse, or
    fails validation.
    """
    path = Path(path)
    text = path.read_text()

    match = FRONT_MATTER_RE.match(text)
    if not match:
        raise LoadError(
            f"Could not find YAML front-matter in {path}. "
            "Theory documents must start with '---' delimiters."
        )

    yaml_text, body = match.groups()
    try:
        front_matter = yaml.safe_load(yaml_text)
    except yaml.YAMLError as e:
        raise LoadError(f"Failed to parse YAML front-matter in {path}: {e}") from e

    if not isinstance(front_matter, dict):
        raise LoadError(f"Front-matter in {path} is not a dict (got {type(front_matter).__name__})")

    try:
        validate_theory_document(front_matter)
    except ValidationError as e:
        raise LoadError(f"Validation failed for {path}: {e}") from e

    front_matter["body"] = body
    return front_matter
```

- [ ] **Step 6: Run test to verify it passes**

Run: `.venv/bin/pytest tests/substrates/test_loader.py -v`
Expected: PASS (4 tests)

- [ ] **Step 7: Run the full test suite to confirm no regressions**

Run: `.venv/bin/pytest tests/ -v`
Expected: PASS (31 tests — 27 existing + 4 new)

- [ ] **Step 8: Commit**

```bash
git add pyproject.toml src/electronic_music_mentor/substrates/loader.py tests/substrates/test_loader.py
git commit -m "feat: theory document loader with YAML front-matter parsing"
```

---

### Task 2: Theory document — Voice-leading

**Files:**
- Create: `knowledge/theory/voice-leading.md`

- [ ] **Step 1: Research and write the voice-leading document**

Write `knowledge/theory/voice-leading.md` following the document format specified above. The document must cover:

**Content requirements:**
- **topic**: Voice-leading
- **summary**: One sentence on smooth voice-leading between chords
- **principles** (at least 4): minimize movement between voices; avoid parallel fifths and octaves in classical voice-leading; lead the outer voices (soprano and bass) with care; resolve tendency tones (leading tone up to tonic, seventh down); in electronic music, voice-leading rules relax when bass carries the harmony
- **electronic_music_notes**: How voice-leading works differently in electronic music — bass often carries the harmony (bass-as-harmony), chord stabs are often sparse and don't need smooth voice-leading, static loops mean voice-leading is less about movement and more about register spacing, parallel fifths are often idiomatic (not a problem) in electronic genres
- **examples** (at least 3): i-VI-III-VII in minor with common tones; static-bass voice-leading where bass stays on root while chords change above; pad voice-leading where inner voices move minimally
- **Body** (200-400 words): Explain the general principles of voice-leading (smooth connection between chords, minimizing leap, handling tendency tones), then how electronic music changes the picture: bass-as-harmony means wide bass leaps are fine, chord stabs often arrive simultaneously without smooth connection, the concern shifts to register spacing (avoiding low-mid overcrowding) rather than melodic voice-leading, parallelism is often a feature not a bug. Write in original prose informed by standard theory references; do not reproduce copyrighted text.
- **Sources**: Cite at least 2 authoritative sources (e.g., Aldwell & Schachter's "Harmony & Voice Leading", Schoenberg's "Theory of Harmony", or equivalent standard texts; for electronic music notes, general production knowledge with attribution to production literature).

- [ ] **Step 2: Validate the document**

Run: `.venv/bin/python -c "from electronic_music_mentor.substrates.loader import load_theory_document; from pathlib import Path; doc = load_theory_document(Path('knowledge/theory/voice-leading.md')); print(f'Loaded: {doc[\"topic\"]}, {len(doc[\"principles\"])} principles, {len(doc[\"examples\"])} examples')"`
Expected: prints a confirmation with the topic name, number of principles, and number of examples (no error).

- [ ] **Step 3: Commit**

```bash
git add knowledge/theory/voice-leading.md
git commit -m "docs: theory document — voice-leading"
```

---

### Task 3: Theory document — Diatonic harmony

**Files:**
- Create: `knowledge/theory/diatonic-harmony.md`

- [ ] **Step 1: Research and write the diatonic harmony document**

Write `knowledge/theory/diatonic-harmony.md` following the document format. Content requirements:

- **topic**: Diatonic harmony
- **summary**: One sentence on harmony built from the seven diatonic chords of a major or minor scale
- **principles** (at least 4): the seven diatonic triads (I-ii-iii-IV-V-vi-vii° in major; i-ii°-III-iv-V-VI-VII in minor); roman numeral analysis; primary functions (tonic, subdominant/pre-dominant, dominant); common progressions (I-V-vi-IV, ii-V-I, I-IV-V); the dominant-tonic relationship (V-I) as the strongest pull
- **electronic_music_notes**: How diatonic harmony plays in electronic music — many genres use only 2-4 chords (not full progressions); house often uses diatonic stabs (ii-V-I or I-vi-IV-V); techno often avoids functional harmony entirely; the "four chords" (I-V-vi-IV) is ubiquitous in pop-electronic; minor keys dominate (darker genres)
- **examples** (at least 3): ii-V-I in a house track; I-V-vi-IV (the "four chords"); a minor-key i-VI-III-VII loop common in deep house
- **Body** (200-400 words): Explain the diatonic system (scales → triads → functions), common progressions and why they work (tension/release, dominant to tonic), then electronic music specifics: genres that use diatonic harmony vs those that avoid it, how loops change harmonic thinking (a 2-chord loop isn't a "progression" in the classical sense), why minor keys dominate. Original prose, cite sources.
- **Sources**: At least 2 (e.g., a standard harmony text like Aldwell & Schachter or Kostka & Payne; a production-oriented harmony reference).

- [ ] **Step 2: Validate the document**

Run: `.venv/bin/python -c "from electronic_music_mentor.substrates.loader import load_theory_document; from pathlib import Path; doc = load_theory_document(Path('knowledge/theory/diatonic-harmony.md')); print(f'Loaded: {doc[\"topic\"]}')"`
Expected: confirmation, no error.

- [ ] **Step 3: Commit**

```bash
git add knowledge/theory/diatonic-harmony.md
git commit -m "docs: theory document — diatonic harmony"
```

---

### Task 4: Theory document — Chromatic harmony

**Files:**
- Create: `knowledge/theory/chromatic-harmony.md`

- [ ] **Step 1: Research and write the chromatic harmony document**

Content requirements:
- **topic**: Chromatic harmony
- **summary**: One sentence on chords and techniques that go beyond the diatonic scale — borrowed chords, secondary dominants, modulation
- **principles** (at least 4): borrowed chords (modal interchange — iv from minor in major, bVI, bVII); secondary dominants (V/V, V/ii — applying dominant function to a non-tonic chord); modulation (pivot chord, direct modulation, common-tone modulation); augmented sixth chords; chromatic mediants (III relationship)
- **electronic_music_notes**: Chromatic harmony is rarer in electronic music than in jazz or classical — but borrowed chords (especially bVI, iv) are common for color in house and techno; secondary dominants appear in more harmonically active genres (disco, french house); modulation is less common because loops tend to stay in one key; the bVI chord is a signature move in euphoric house
- **examples** (at least 3): bVI-bVII-I in a house track (euphoric lift); iv minor in a major-key house track (color); a secondary dominant (V/vi) leading to vi
- **Body** (200-400 words): Explain chromatic techniques (borrowing, secondary dominants, modulation), why each adds color or direction, then electronic music specifics: which techniques are common (borrowing for color, not function), which are rare (complex modulation), the bVI as a house signature. Original prose, cite sources.
- **Sources**: At least 2 (standard harmony text for chromatic harmony; production reference for electronic application).

- [ ] **Step 2: Validate the document**

Run: `.venv/bin/python -c "from electronic_music_mentor.substrates.loader import load_theory_document; from pathlib import Path; doc = load_theory_document(Path('knowledge/theory/chromatic-harmony.md')); print(f'Loaded: {doc[\"topic\"]}')"`
Expected: confirmation, no error.

- [ ] **Step 3: Commit**

```bash
git add knowledge/theory/chromatic-harmony.md
git commit -m "docs: theory document — chromatic harmony"
```

---

### Task 5: Theory document — Bass-as-harmony

**Files:**
- Create: `knowledge/theory/bass-as-harmony.md`

- [ ] **Step 1: Research and write the bass-as-harmony document**

This is the most electronic-music-specific topic in the set. Content requirements:
- **topic**: Bass-as-harmony
- **summary**: One sentence on when the bass line carries the harmonic identity, with chord stabs or pads providing color rather than functional progression
- **principles** (at least 4): the bass defines the root and therefore the chord identity; in bass-as-harmony, the bass often plays roots or roots+fifths while chords above add color (thirds, sevenths, extensions); bass movement IS the harmonic movement (bass changes = chord changes); the bass can play wide leaps that would be wrong in classical voice-leading because it's carrying the harmony, not a voice in a chord; register separation between bass and chord stabs is critical (bass low, stabs higher to avoid low-mid crowding)
- **electronic_music_notes**: This is THE defining harmonic approach in many electronic genres — techno, house, dub techno, drum & bass all use bass-as-harmony extensively; the bass plays the root (or root-fifth-octave pattern) and a chord stab or pad provides the harmonic color above; this means "chord progressions" in electronic music are often just bass note changes; the skill of bass-as-harmony is register management (keeping bass and stabs out of each other's way) and choosing which color notes the stab adds above each bass note
- **examples** (at least 3): a dub techno track where bass plays C while a minor chord stab plays above, then bass moves to Ab (the "chord change" is just the bass); a house track where bass plays root-fifth-octave while a major chord stab provides color; a techno track where the bass moves C-Eb-G-Ab (the harmonic identity follows the bass, no chord stabs at all)
- **Body** (200-400 words): Explain the concept (bass carries harmony vs. chord-led harmony where the progression is in the chords), why it's so common in electronic music (bass is the foundation, loops are bass-driven, chord stabs are textural), the practical implications (register management, what the stab adds above each bass note, when to use stabs vs. pads vs. nothing). Original prose, cite sources.
- **Sources**: At least 2 (a production-oriented reference for electronic music bass/harmony; a general harmony text for the contrast with chord-led harmony).

- [ ] **Step 2: Validate the document**

Run: `.venv/bin/python -c "from electronic_music_mentor.substrates.loader import load_theory_document; from pathlib import Path; doc = load_theory_document(Path('knowledge/theory/bass-as-harmony.md')); print(f'Loaded: {doc[\"topic\"]}')"`
Expected: confirmation, no error.

- [ ] **Step 3: Commit**

```bash
git add knowledge/theory/bass-as-harmony.md
git commit -m "docs: theory document — bass-as-harmony"
```

---

### Task 6: Theory document — Static harmony

**Files:**
- Create: `knowledge/theory/static-harmony.md`

- [ ] **Step 1: Research and write the static harmony document**

Content requirements:
- **topic**: Static harmony
- **summary**: One sentence on harmony that stays on one chord or oscillates between two, driving through rhythm and texture rather than progression
- **principles** (at least 4): static harmony stays on one chord (pedal point) or oscillates between two (i-VII, i-VI); the harmonic interest comes from rhythm, texture, and filter movement, not chord changes; the bass often anchors a pedal while textures evolve above; tension is created through density, register, and rhythm rather than harmonic direction; static harmony is not "harmony without progress" — the progress is textural and rhythmic
- **electronic_music_notes**: Static harmony is a defining feature of techno, dub techno, and minimal electronic — a single chord or two-chord loop sustains for minutes while the track evolves through texture, filter, and density; this is the opposite of pop harmonic thinking (where progressions drive); the skill is sustaining interest without harmonic change — using filter sweeps, adding/removing layers, evolving percussion, textural shifts
- **examples** (at least 3): a dub techno track on one minor chord for 8 minutes, evolving through filter movement; a techno track oscillating i-VII with percussion driving the energy; a minimal track on a pedal point where the bass holds the root and textures shift above
- **Body** (200-400 words): Explain static harmony (pedal, two-chord oscillation), why it's powerful (sustains a mood, lets rhythm and texture drive), how it differs from progression-based harmony, the skill of maintaining interest without harmonic change. Original prose, cite sources.
- **Sources**: At least 2 (a production reference on minimal/techno approaches; a harmony text on pedal point and static harmony).

- [ ] **Step 2: Validate the document**

Run: `.venv/bin/python -c "from electronic_music_mentor.substrates.loader import load_theory_document; from pathlib import Path; doc = load_theory_document(Path('knowledge/theory/static-harmony.md')); print(f'Loaded: {doc[\"topic\"]}')"`
Expected: confirmation, no error.

- [ ] **Step 3: Commit**

```bash
git add knowledge/theory/static-harmony.md
git commit -m "docs: theory document — static harmony"
```

---

### Task 7: Theory document — Rhythmic subdivision and groove

**Files:**
- Create: `knowledge/theory/rhythmic-subdivision.md`

- [ ] **Step 1: Research and write the rhythmic subdivision document**

Content requirements:
- **topic**: Rhythmic subdivision and groove
- **summary**: One sentence on how rhythmic grids (sixteenth-note, triplet) and micro-timing (swing, pocket) create groove in electronic music
- **principles** (at least 4): the sixteenth-note grid is the default rhythmic framework in most electronic music; swing (delaying off-beats) creates groove — house swing delays the second sixteenth, garage/shuffle uses triplet feel; the pocket is where the kick sits relative to the grid — slightly ahead (pushing) or behind (pulling) changes the feel; velocity and accent patterns create groove as much as timing — where you hit hard vs. soft; polyrhythm (3 against 4, etc.) adds complexity within the grid
- **electronic_music_notes**: Groove is central to electronic music — house swing, garage shuffle, techno's rigid grid, jungle's breakbeat polyrhythm are all groove signatures; micro-timing (swing percentages, groove templates) is a production craft; the grid can be rigid (techno) or loose (garage, jungle); velocity patterns (especially on hats) are as important as timing for groove
- **examples** (at least 3): house swing (second sixteenth delayed) on a hat pattern; a garage shuffle (triplet feel on hats); a jungle breakbeat with syncopated kick/snare against a straight hi-hat
- **Body** (200-400 words): Explain rhythmic subdivision (the grid, swing, triplets vs. straight), the pocket (micro-timing of kick and bass), velocity as groove, polyrhythm, then electronic music specifics: how different genres use the grid, swing, and velocity to create their signature grooves. Original prose, cite sources.
- **Sources**: At least 2 (a rhythm/groove reference like Mark London's "The Producing Drum Grooves" or general production literature on groove; a music theory text on rhythm and meter).

- [ ] **Step 2: Validate the document**

Run: `.venv/bin/python -c "from electronic_music_mentor.substrates.loader import load_theory_document; from pathlib import Path; doc = load_theory_document(Path('knowledge/theory/rhythmic-subdivision.md')); print(f'Loaded: {doc[\"topic\"]}')"`
Expected: confirmation, no error.

- [ ] **Step 3: Commit**

```bash
git add knowledge/theory/rhythmic-subdivision.md
git commit -m "docs: theory document — rhythmic subdivision and groove"
```

---

### Task 8: Theory document — Phrase and form

**Files:**
- Create: `knowledge/theory/phrase-and-form.md`

- [ ] **Step 1: Research and write the phrase and form document**

Content requirements:
- **topic**: Phrase and form
- **summary**: One sentence on how motifs, repetition, variation, and section structure create form in electronic music
- **principles** (at least 4): the motif is the smallest melodic/rhythmic idea — a track grows by developing it; repetition establishes identity, variation sustains interest (change something, keep the rest); phrase length (4, 8, 16 bars) creates formal expectation; electronic music form is often additive/subtractive (layers in, layers out) rather than verse-chorus; the energy arc (build → peak → release) structures the track regardless of harmonic form
- **electronic_music_notes**: Electronic music form differs from song form — it's additive (start sparse, add layers, peak, remove layers) rather than verse-chorus-bridge; the 16-bar phrase is common (4 groups of 4); builds and drops are the structural pillars; motif development is often subtle (a filter opens on the same motif rather than a new motif); arrangement is about managing energy and density, not chord progression
- **examples** (at least 3): a house track with a 16-bar phrase structure, building percussion then dropping into a chord stab; a techno track that adds layers over a static loop to build to a peak; a motif that repeats through a track with filter evolution as the variation
- **Body** (200-400 words): Explain motif, repetition/variation, phrase length, form types, then electronic music specifics: additive/subtractive form, builds and drops, the 16-bar phrase, arrangement as energy management. Original prose, cite sources.
- **Sources**: At least 2 (a form/analysis text for classical form concepts; a production reference for electronic arrangement).

- [ ] **Step 2: Validate the document**

Run: `.venv/bin/python -c "from electronic_music_mentor.substrates.loader import load_theory_document; from pathlib import Path; doc = load_theory_document(Path('knowledge/theory/phrase-and-form.md')); print(f'Loaded: {doc[\"topic\"]}')"`
Expected: confirmation, no error.

- [ ] **Step 3: Commit**

```bash
git add knowledge/theory/phrase-and-form.md
git commit -m "docs: theory document — phrase and form"
```

---

### Task 9: Theory document — Tension and release

**Files:**
- Create: `knowledge/theory/tension-and-release.md`

- [ ] **Step 1: Research and write the tension and release document**

Content requirements:
- **topic**: Tension and release
- **summary**: One sentence on how tension is created and released across harmonic, rhythmic, and textural dimensions in electronic music
- **principles** (at least 4): harmonic tension (dissonance, dominant function, chromaticism) resolves to consonance; rhythmic tension (syncopation, density, build-up) releases to simplicity or drop; textural tension (filter opening, layer addition) releases to clarity or subtraction; the build-drop is the dominant tension-release structure in electronic music (long build of tension → sudden release at the drop); tension can be sustained (static harmony holding dissonance) or directed (progression toward resolution)
- **electronic_music_notes**: In electronic music, tension and release is often non-harmonic — the build-drop uses density, filter, and rhythm rather than chord progressions to create and release tension; a snare roll build-up creates rhythmic tension that releases at the drop; a filter sweep on a pad creates textural tension that releases when the filter closes; the skill is managing multiple tension dimensions (harmonic, rhythmic, textural) simultaneously, and knowing when to release vs. sustain
- **examples** (at least 3): a snare roll build-up that releases at a drop; a filter sweep that opens (tension) then closes (release); a harmonic tension (sustained dominant chord) that resolves to tonic at a section change
- **Body** (200-400 words): Explain tension and release across three dimensions (harmonic, rhythmic, textural), the build-drop as the signature electronic tension-release structure, how different genres use tension (techno sustains, house builds and releases, jungle uses rhythmic tension), the skill of managing multiple dimensions. Original prose, cite sources.
- **Sources**: At least 2 (a harmony text for harmonic tension/release; a production reference for build-drop and textural tension).

- [ ] **Step 2: Validate the document**

Run: `.venv/bin/python -c "from electronic_music_mentor.substrates.loader import load_theory_document; from pathlib import Path; doc = load_theory_document(Path('knowledge/theory/tension-and-release.md')); print(f'Loaded: {doc[\"topic\"]}')"`
Expected: confirmation, no error.

- [ ] **Step 3: Commit**

```bash
git add knowledge/theory/tension-and-release.md
git commit -m "docs: theory document — tension and release"
```

---

### Task 10: Update theory README and final validation

**Files:**
- Modify: `knowledge/theory/README.md`

- [ ] **Step 1: Update the theory README**

Replace the "Planned topics" section with a list of the completed documents, linking to each file. Update the format section to reference the loader. The new content:

```markdown
# Theory Substrate

Music-theory foundations as they apply to electronic music. Consumed by the `harmony`, `bass`, `melody`, `rhythm`, and `arrangement` skills.

## Documents

- [Voice-leading](voice-leading.md) — smooth chord connection, with electronic-music specifics on bass-as-harmony and register spacing
- [Diatonic harmony](diatonic-harmony.md) — the seven diatonic chords, common progressions, and how electronic genres use them
- [Chromatic harmony](chromatic-harmony.md) — borrowed chords, secondary dominants, modulation, and their use in electronic music
- [Bass-as-harmony](bass-as-harmony.md) — when the bass carries the harmonic identity, the defining approach in many electronic genres
- [Static harmony](static-harmony.md) — pedal points and two-chord loops, driving through rhythm and texture
- [Rhythmic subdivision and groove](rhythmic-subdivision.md) — grids, swing, pocket, velocity, and groove signatures
- [Phrase and form](phrase-and-form.md) — motifs, repetition, variation, additive form, and energy arcs
- [Tension and release](tension-and-release.md) — harmonic, rhythmic, and textural tension; the build-drop

## Format

Each theory document is a markdown file with YAML front-matter validated by `electronic_music_mentor.substrates.validator.validate_theory_document`, loaded by `electronic_music_mentor.substrates.loader.load_theory_document`:
- `topic`
- `summary`
- `principles` (list)
- `electronic_music_notes`
- `examples` (list)
- `## Sources` section at the bottom with attributions
```

- [ ] **Step 2: Validate all theory documents load cleanly**

Run: `.venv/bin/python -c "
from electronic_music_mentor.substrates.loader import load_theory_document
from pathlib import Path
topics = ['voice-leading', 'diatonic-harmony', 'chromatic-harmony', 'bass-as-harmony', 'static-harmony', 'rhythmic-subdivision', 'phrase-and-form', 'tension-and-release']
for t in topics:
    doc = load_theory_document(Path(f'knowledge/theory/{t}.md'))
    print(f'{doc[\"topic\"]}: {len(doc[\"principles\"])} principles, {len(doc[\"examples\"])} examples')
print('All theory documents loaded successfully')
"`
Expected: prints a line per topic (8 total) and "All theory documents loaded successfully" with no errors.

- [ ] **Step 3: Run the full test suite**

Run: `.venv/bin/pytest tests/ -v`
Expected: PASS (31 tests — no regressions)

- [ ] **Step 4: Commit**

```bash
git add knowledge/theory/README.md
git commit -m "docs: update theory README with completed document index"
```

---

## Self-Review

**1. Spec coverage:**
- Loader for markdown front-matter → dict → validation — ✓ (Task 1)
- 8 theory topics from the planned list — ✓ (Tasks 2-9, one per topic)
- Voice-leading — ✓ (Task 2)
- Diatonic harmony — ✓ (Task 3)
- Chromatic harmony — ✓ (Task 4)
- Bass-as-harmony — ✓ (Task 5)
- Static harmony — ✓ (Task 6)
- Rhythmic subdivision and groove — ✓ (Task 7)
- Phrase and form — ✓ (Task 8)
- Tension and release — ✓ (Task 9)
- Theory README updated with completed index — ✓ (Task 10)
- Sourcing rules (original writing, citations, no verbatim copying) — ✓ (in each task's content requirements)

**2. Placeholder scan:** No TBD or TODO. Each content task specifies exact requirements (topic, minimum principles count, minimum examples count, body length, source count).

**3. Type consistency:** `load_theory_document(path)` returns a dict with front-matter fields plus `body` key. Consistent across Task 1 (definition) and Tasks 2-9 (validation calls). The validator's `THEORY_DOCUMENT_REQUIRED_FIELDS` matches the front-matter fields specified in each content task.