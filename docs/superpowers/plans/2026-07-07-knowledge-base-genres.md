# Electronic Music Mentor — Knowledge Base: Genre Profiles Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the `genre-profiles` substrate — 9 genre profile documents covering dub techno, deep house, Detroit techno, jungle/drum & bass, UK garage, ambient, minimal techno, electro, and IDM/braindance, each encoding the spirit of the genre with rhythmic/harmonic/textural/arrangement conventions and common failure modes, plus a loader extension for genre profiles.

**Architecture:** Each genre profile is a markdown file with YAML front-matter (the structured fields the validator checks) and a prose body (the elaboration skills read). The existing `loader.py` is extended with a `load_genre_profile` function (paralleling `load_theory_document`). Documents are researched from authoritative references and rewritten in original prose.

**Tech Stack:** Python 3.12, PyYAML (already installed), pytest (testing), Markdown (content format).

---

## File Structure

```
Electronic_Music_Mentor/
├── src/electronic_music_mentor/substrates/
│   ├── validator.py                                  # (exists) validates dicts
│   ├── loader.py                                     # (modify) add load_genre_profile
├── tests/substrates/
│   ├── test_loader.py                                # (modify) add genre profile loader tests
├── knowledge/genres/
│   ├── README.md                                     # (modify) update with completed document index
│   ├── dub-techno.md                                 # (new) Task 2
│   ├── deep-house.md                                 # (new) Task 3
│   ├── detroit-techno.md                             # (new) Task 4
│   ├── jungle-drum-and-bass.md                       # (new) Task 5
│   ├── uk-garage.md                                  # (new) Task 6
│   ├── ambient.md                                    # (new) Task 7
│   ├── minimal-techno.md                             # (new) Task 8
│   ├── electro.md                                    # (new) Task 9
│   └── idm-braindance.md                             # (new) Task 10
```

---

## Document Format

Every genre profile follows this format:

```markdown
---
name: <Genre Name>
tempo_range:
  min: <BPM>
  max: <BPM>
  feel: "<one-phrase description of the tempo feel>"
rhythmic_conventions:
  - <convention 1>
  - <convention 2>
  - <convention 3>
harmonic_conventions:
  - <convention 1>
  - <convention 2>
  - <convention 3>
textural_sonic_conventions:
  - <convention 1>
  - <convention 2>
  - <convention 3>
arrangement_conventions:
  - <convention 1>
  - <convention 2>
  - <convention 3>
spirit: >
  <Substantial prose — at least 80 characters, ideally 100-200 words. What the genre is
  trying to do, what good examples do, what lazy examples miss. This is the anti-stereotype
  field that lets the mentor distinguish "executes the genre well" from "copies the surface.">
common_failure_modes:
  - <failure mode 1>
  - <failure mode 2>
  - <failure mode 3>
---

# <Genre Name>

<Prose body — 200-400 words. The main content a skill reads. Original writing informed by
authoritative sources, not reproduced text. Covers the genre's history/context briefly,
then the spirit, what good execution sounds like, what lazy execution sounds like.>

## Sources

- <Author, Title, Publisher/URL> — <what was drawn from this source>
- <Author, Title, Publisher/URL> — <what was drawn from this source>
```

---

### Task 1: Extend loader with `load_genre_profile`

**Files:**
- Modify: `src/electronic_music_mentor/substrates/loader.py`
- Modify: `tests/substrates/test_loader.py` (append tests)

- [ ] **Step 1: Append failing tests for genre profile loading**

Append to `tests/substrates/test_loader.py`:
```python
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `.venv/bin/pytest tests/substrates/test_loader.py -v`
Expected: FAIL — the new tests fail (load_genre_profile doesn't exist yet); the 4 existing theory tests still pass.

- [ ] **Step 3: Add `load_genre_profile` to the loader**

In `src/electronic_music_mentor/substrates/loader.py`, add the import and function. Read the existing file first, then:

1. Change the import line:
```python
from .validator import validate_theory_document, ValidationError
```
to:
```python
from .validator import validate_theory_document, validate_genre_profile, ValidationError
```

2. Add this function after `load_theory_document`:
```python
def load_genre_profile(path: Path) -> dict:
    """Load a genre profile from a markdown file with YAML front-matter.

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
            "Genre profiles must start with '---' delimiters."
        )

    yaml_text, body = match.groups()
    try:
        front_matter = yaml.safe_load(yaml_text)
    except yaml.YAMLError as e:
        raise LoadError(f"Failed to parse YAML front-matter in {path}: {e}") from e

    if not isinstance(front_matter, dict):
        raise LoadError(f"Front-matter in {path} is not a dict (got {type(front_matter).__name__})")

    try:
        validate_genre_profile(front_matter)
    except ValidationError as e:
        raise LoadError(f"Validation failed for {path}: {e}") from e

    front_matter["body"] = body
    return front_matter
```

- [ ] **Step 4: Run test to verify it passes**

Run: `.venv/bin/pytest tests/substrates/test_loader.py -v`
Expected: PASS (7 tests — 4 existing theory + 3 new genre profile)

- [ ] **Step 5: Run the full test suite**

Run: `.venv/bin/pytest tests/ -v`
Expected: PASS (34 tests — 31 existing + 3 new)

- [ ] **Step 6: Commit**

```bash
git add src/electronic_music_mentor/substrates/loader.py tests/substrates/test_loader.py
git commit -m "feat: genre profile loader (extends substrate loader)"
```

---

### Task 2: Genre profile — Dub Techno

**Files:**
- Create: `knowledge/genres/dub-techno.md`

- [ ] **Step 1: Research and write the Dub Techno profile**

Write `knowledge/genres/dub-techno.md` following the document format. Content requirements:

- **name**: Dub Techno
- **tempo_range**: min 120, max 130, feel "hypnotic, patient"
- **rhythmic_conventions** (at least 3): four-on-the-floor kick; offbeat/open hats; sparse percussion; emphasis on groove through filter movement not pattern complexity
- **harmonic_conventions** (at least 3): static harmony (one or two chords for minutes); minor tonality; chord stabs with long reverb; bass-as-harmony (bass carries the root, stab adds color)
- **textural_sonic_conventions** (at least 3): haze and atmosphere; reverb-drenched; slow filter movement (the defining textural motion); detuned oscillators; tape/tape-saturation character
- **arrangement_conventions** (at least 3): long builds; atmospheric breakdowns; minimal section changes; evolution through texture not structure
- **spirit**: Substantial prose (100-200 words) — Dub techno pursues hypnotic immersion through repetition and slow change. Good examples sustain a single idea with patience — the track evolves through filter movement, layer addition, and textural density, not through chord changes or section shifts. The groove is patient; the atmosphere is deep and reverberant. Lazy examples just repeat a loop without evolution — they mistake "static" for "stuck." The genre's depth comes from *controlled* change, not from no change. A dub techno track that doesn't evolve isn't minimal, it's boring.
- **common_failure_modes** (at least 3): no evolution (static loop without filter/texture movement); overcrowded mid (too many elements in the low-mid range); harsh digital high end (missing the warm, hazy character); chord stabs too loud (overpowering the atmosphere)
- **Body** (200-400 words): Brief history (Berlin, Basic Channel/Chain Reaction, the dub reggae influence), the spirit, what good execution sounds like (patient evolution, deep atmosphere, bass-as-harmony), what lazy execution sounds like (static loops, no filter movement, overcrowded). Original prose, cite sources.
- **Sources**: At least 2 (e.g., production literature on dub techno; general electronic music history references).

- [ ] **Step 2: Validate the document**

Run: `.venv/bin/python -c "from electronic_music_mentor.substrates.loader import load_genre_profile; from pathlib import Path; p = load_genre_profile(Path('knowledge/genres/dub-techno.md')); print(f'Loaded: {p[\"name\"]}, tempo {p[\"tempo_range\"][\"min\"]}-{p[\"tempo_range\"][\"max\"]}, {len(p[\"rhythmic_conventions\"])} rhythmic, {len(p[\"common_failure_modes\"])} failure modes')"`
Expected: confirmation, no error.

- [ ] **Step 3: Commit**

```bash
git add knowledge/genres/dub-techno.md
git commit -m "docs: genre profile — dub techno"
```

---

### Task 3: Genre profile — Deep House

**Files:**
- Create: `knowledge/genres/deep-house.md`

- [ ] **Step 1: Research and write the Deep House profile**

Content requirements:
- **name**: Deep House
- **tempo_range**: min 118, max 125, feel "warm, soulful, steady"
- **rhythmic_conventions** (at least 3): four-on-the-floor kick; swung hats (subtle swing, not rigid); shaker/percussion layers; the groove is warm and steady, not driving
- **harmonic_conventions** (at least 3): diatonic progressions (often ii-V-I or I-vi-IV-V); minor keys with major VII borrow; chord stabs (rhodes, pads); bass-as-harmony with walking bass movement
- **textural_sonic_conventions** (at least 3): warm (rhodes, analog pads); vinyl crackle; soft saturation; reverb on stabs but not overwhelming; organic feel
- **arrangement_conventions** (at least 3): 16-bar phrases; builds through layer addition (percussion, then stabs, then vocals); drops into chord stab sections; vocal hooks as structural pillars
- **spirit** (100-200 words): Deep house pursues warmth and soul through groove and harmony. Good examples feel organic — the swing is subtle, the chords are voiced with care, the bass walks, and the atmosphere is warm without being muddy. The groove is steady and inviting, not aggressive. Lazy examples use a generic house loop with a minor chord stab and call it deep — but deep house's depth comes from harmonic care and textural warmth, not just "minor key + swing." A deep house track without harmonic intention is just house with a mood.
- **common_failure_modes** (at least 3): generic chord stabs (no harmonic care); rigid groove (no swing, feels mechanical); harsh digital sound (missing warmth); overcrowded arrangement (too many layers, losing the space)
- **Body** (200-400 words): Brief context (Chicago roots, the "deep" designation, the soul/jazz influence), the spirit, good vs lazy execution. Original prose, cite sources.
- **Sources**: At least 2.

- [ ] **Step 2: Validate**

Run: `.venv/bin/python -c "from electronic_music_mentor.substrates.loader import load_genre_profile; from pathlib import Path; p = load_genre_profile(Path('knowledge/genres/deep-house.md')); print(f'Loaded: {p[\"name\"]}')"`

- [ ] **Step 3: Commit**

```bash
git add knowledge/genres/deep-house.md
git commit -m "docs: genre profile — deep house"
```

---

### Task 4: Genre profile — Detroit Techno

**Files:**
- Create: `knowledge/genres/detroit-techno.md`

- [ ] **Step 1: Research and write the Detroit Techno profile**

Content requirements:
- **name**: Detroit Techno
- **tempo_range**: min 125, max 132, feel "mechanical, emotive, driving"
- **rhythmic_conventions** (at least 3): four-on-the-floor kick; robotic/precise hats; percussion often syncopated but tight; the groove is mechanical but not lifeless — the emotion is in the harmony and texture
- **harmonic_conventions** (at least 3): minor keys; chromatic bass movement; string-pad chords; bass-as-harmony with melodic bass lines; harmonic tension through suspended or unresolved chords
- **textural_sonic_conventions** (at least 3): cold/clinical synths; string pads for emotion; metallic percussion; the contrast between cold textures and emotive harmony is the signature
- **arrangement_conventions** (at least 3): long-form builds; layer addition; breakdowns with string pads; the arrangement emphasizes the cold/emotive contrast
- **spirit** (100-200 words): Detroit techno pursues the tension between mechanical precision and emotive depth. Good examples are cold on the surface — robotic percussion, clinical synths — but emotive underneath — minor harmony, string pads, melancholic bass. The genre's signature is this contrast, not just "fast and mechanical." Lazy examples are all surface — fast mechanical patterns with no harmonic or emotional content. Detroit techno without the emotive undercurrent is just techno; the depth is in the feeling inside the machine.
- **common_failure_modes** (at least 3): all surface (mechanical without emotive content); no harmonic intention; harsh high end; lack of dynamic range (everything loud)
- **Body** (200-400 words): Brief context (Detroit, Belleville Three, the industrial/emotive duality), the spirit, good vs lazy execution. Original prose, cite sources.
- **Sources**: At least 2.

- [ ] **Step 2: Validate**

Run: `.venv/bin/python -c "from electronic_music_mentor.substrates.loader import load_genre_profile; from pathlib import Path; p = load_genre_profile(Path('knowledge/genres/detroit-techno.md')); print(f'Loaded: {p[\"name\"]}')"`

- [ ] **Step 3: Commit**

```bash
git add knowledge/genres/detroit-techno.md
git commit -m "docs: genre profile — detroit techno"
```

---

### Task 5: Genre profile — Jungle / Drum & Bass

**Files:**
- Create: `knowledge/genres/jungle-drum-and-bass.md`

- [ ] **Step 1: Research and write the Jungle / Drum & Bass profile**

Content requirements:
- **name**: Jungle / Drum & Bass
- **tempo_range**: min 160, max 180, feel "fast, breakbeat-driven, energetic"
- **rhythmic_conventions** (at least 3): breakbeat drums (Amen break and variations); syncopated snare placement; fast hi-hats; the groove is in the breakbeat complexity, not a four-on-the-floor pattern; Reese bass often doubles the rhythmic energy
- **harmonic_conventions** (at least 3): minor keys; chromatic Reese bass; sparse harmony (often just bass and atmosphere); bass-as-harmony is dominant; harmonic stabs for tension at builds
- **textural_sonic_conventions** (at least 3): Reese bass (detuned, moving); atmospheric pads; gritty/grainy textures; sub-bass weight; the contrast between dark bass and atmospheric pads
- **arrangement_conventions** (at least 3): build-drop structure; long builds with snare rolls; drops into full breakbeat energy; breakdowns with atmospheric pads; the drop is the structural pillar
- **spirit** (100-200 words): Jungle/drum & bass pursues energy through breakbeat complexity and sub-bass weight. Good examples drive through the breakbeat's rhythmic intricacy while the Reese bass provides harmonic and textural weight. The energy is in the drums; the depth is in the bass and atmosphere. Lazy examples use a static breakbeat loop with no variation and a generic Reese — they have the tempo but not the groove. The genre's skill is making a fast, complex rhythm feel coherent and driving, not chaotic.
- **common_failure_modes** (at least 3): static breakbeat (no variation); weak sub-bass; chaotic arrangement (no build/drop structure); thin mix (missing the weight)
- **Body** (200-400 words): Brief context (UK, jungle's roots in rave and reggae sound system culture, the jungle→DnB evolution), the spirit, good vs lazy execution. Original prose, cite sources.
- **Sources**: At least 2.

- [ ] **Step 2: Validate**

Run: `.venv/bin/python -c "from electronic_music_mentor.substrates.loader import load_genre_profile; from pathlib import Path; p = load_genre_profile(Path('knowledge/genres/jungle-drum-and-bass.md')); print(f'Loaded: {p[\"name\"]}')"`

- [ ] **Step 3: Commit**

```bash
git add knowledge/genres/jungle-drum-and-bass.md
git commit -m "docs: genre profile — jungle / drum & bass"
```

---

### Task 6: Genre profile — UK Garage

**Files:**
- Create: `knowledge/genres/uk-garage.md`

- [ ] **Step 1: Research and write the UK Garage profile**

Content requirements:
- **name**: UK Garage
- **tempo_range**: min 130, max 138, feel "swung, bouncy, skip-beat"
- **rhythmic_conventions** (at least 3): broken kick pattern (not four-on-the-floor); swung/shuffled hats (triplet feel); skip-beat snare; the groove is in the swing and the broken pattern — the signature is the "forward-leaning" feel
- **harmonic_conventions** (at least 3): minor keys; R&B-influenced chord voicings (ninths, elevenths); bass-as-harmony with melodic bass; vocal samples as harmonic color
- **textural_sonic_conventions** (at least 3): smooth/polished; vocal chops; warm bass; crisp hats; the texture is smooth and vocal-influenced, not gritty
- **arrangement_conventions** (at least 3): 16-bar phrases; vocal-led sections; builds through vocal and bass addition; drops into the swung groove
- **spirit** (100-200 words): UK garage pursues a bouncy, forward-leaning groove through swing and broken patterns. Good examples feel like they're skipping forward — the swing creates momentum, the broken kick creates tension against the hats, and the bass is melodic and warm. The groove is the whole point. Lazy examples just use a shuffled hat over a four-on-the-floor kick and call it garage — but garage's signature is the *broken* pattern and the *skip*, not just swing. A garage track that doesn't skip isn't garage.
- **common_failure_modes** (at least 3): four-on-the-floor with swing (missing the broken pattern); no skip feel; generic bass (not melodic); stiff groove (swing too subtle)
- **Body** (200-400 words): Brief context (UK, the US garage influence, the speed garage→2-step evolution), the spirit, good vs lazy execution. Original prose, cite sources.
- **Sources**: At least 2.

- [ ] **Step 2: Validate**

Run: `.venv/bin/python -c "from electronic_music_mentor.substrates.loader import load_genre_profile; from pathlib import Path; p = load_genre_profile(Path('knowledge/genres/uk-garage.md')); print(f'Loaded: {p[\"name\"]}')"`

- [ ] **Step 3: Commit**

```bash
git add knowledge/genres/uk-garage.md
git commit -m "docs: genre profile — uk garage"
```

---

### Task 7: Genre profile — Ambient

**Files:**
- Create: `knowledge/genres/ambient.md`

- [ ] **Step 1: Research and write the Ambient profile**

Content requirements:
- **name**: Ambient
- **tempo_range**: min 60, max 100, feel "slow, atmospheric, drifting" (note: ambient can have no explicit beat, tempo is loose)
- **rhythmic_conventions** (at least 3): often no explicit percussion; if percussion, sparse and slow; textural rhythm (slow filter, evolving pads); the groove is absent or minimal — the energy is in texture and harmony
- **harmonic_conventions** (at least 3): static or slowly evolving harmony; modal (often Dorian or Aeolian); drone-based; bass-as-harmony with sustained bass notes; harmonic change is slow and textural
- **textural_sonic_conventions** (at least 3): evolving pads; reverb and space; granular or processed textures; field recordings; the texture IS the content — the track is about evolving atmosphere
- **arrangement_conventions** (at least 3): no traditional build-drop; slow evolution; layer drift in and out; the arrangement is about sustained atmosphere, not structural events
- **spirit** (100-200 words): Ambient pursues atmosphere and sustained mood over rhythm and progression. Good examples create a world you inhabit — the texture evolves slowly, the harmony is static or drifting, the space is deep. The track isn't going anywhere; it's being somewhere. Lazy examples are a pad with reverb and nothing else — they have the surface of ambient but not the depth, because the texture isn't evolving. Ambient requires *controlled* evolution of texture, not just "pad + reverb."
- **common_failure_modes** (at least 3): static pad (no evolution); no space (too dry); no harmonic identity (random pad with no tonal center); overcrowded (ambient needs space, not density)
- **Body** (200-400 words): Brief context (Eno, the "music as atmosphere" concept, the ambient→ambient techno→dub techno lineage), the spirit, good vs lazy execution. Original prose, cite sources.
- **Sources**: At least 2.

- [ ] **Step 2: Validate**

Run: `.venv/bin/python -c "from electronic_music_mentor.substrates.loader import load_genre_profile; from pathlib import Path; p = load_genre_profile(Path('knowledge/genres/ambient.md')); print(f'Loaded: {p[\"name\"]}')"`

- [ ] **Step 3: Commit**

```bash
git add knowledge/genres/ambient.md
git commit -m "docs: genre profile — ambient"
```

---

### Task 8: Genre profile — Minimal Techno

**Files:**
- Create: `knowledge/genres/minimal-techno.md`

- [ ] **Step 1: Research and write the Minimal Techno profile**

Content requirements:
- **name**: Minimal Techno
- **tempo_range**: min 125, max 130, feel "reduced, hypnotic, precise"
- **rhythmic_conventions** (at least 3): four-on-the-floor kick; precise, stripped percussion; subtle swing or completely rigid; the groove comes from *what's removed*, not what's added — the interest is in the negative space
- **harmonic_conventions** (at least 3): often no explicit harmony; if present, single notes or two-note stabs; bass-as-harmony with single bass notes; harmonic content is minimal by design
- **textural_sonic_conventions** (at least 3): clean/digital; precise sound design; every element audible and distinct; the texture is about clarity, not atmosphere — each sound is sculpted
- **arrangement_conventions** (at least 3): very long builds; single elements added/removed over long phrases; the arrangement is about *what changes*, not *how much changes* — one element added is a major event
- **spirit** (100-200 words): Minimal techno pursues depth through reduction. Good examples achieve hypnotic intensity by removing everything non-essential — the track drives through a kick, a bass note, and one or two percussive elements, and the interest is in the precise interplay of those few elements. The skill is making less feel like more. Lazy examples are just "empty" — they remove elements but don't sculpt the remaining ones, so the track feels thin rather than hypnotic. Minimal isn't "less stuff"; it's "each thing matters more."
- **common_failure_modes** (at least 3): empty (removed elements without sculpting the rest); no evolution (truly static); thin mix (missing weight); no groove (the kick and bass don't lock)
- **Body** (200-400 words): Brief context (the minimal techno tradition, the reduction principle), the spirit, good vs lazy execution. Original prose, cite sources.
- **Sources**: At least 2.

- [ ] **Step 2: Validate**

Run: `.venv/bin/python -c "from electronic_music_mentor.substrates.loader import load_genre_profile; from pathlib import Path; p = load_genre_profile(Path('knowledge/genres/minimal-techno.md')); print(f'Loaded: {p[\"name\"]}')"`

- [ ] **Step 3: Commit**

```bash
git add knowledge/genres/minimal-techno.md
git commit -m "docs: genre profile — minimal techno"
```

---

### Task 9: Genre profile — Electro

**Files:**
- Create: `knowledge/genres/electro.md`

- [ ] **Step 1: Research and write the Electro profile**

Content requirements:
- **name**: Electro
- **tempo_range**: min 110, max 130, feel "robotic, funky, syncopated"
- **rhythmic_conventions** (at least 3): broken kick pattern (not four-on-the-floor); syncopated 808 programming; electronic handclaps; the groove is robotic-but-funky — the signature is 808 patterns that feel mechanical and groovy at once
- **harmonic_conventions** (at least 3): minor keys; bass-as-harmony with 808 bass lines (melodic 808 patterns); sparse stabs; the 808 bass often carries both rhythm and harmony
- **textural_sonic_conventions** (at least 3): 808 drum sound; vocoder vocals; cold synths; the texture is retro-futuristic — 808 drums, vocoder, cold pads
- **arrangement_conventions** (at least 3): 16-bar phrases; vocoder/vocal sections; bass-led drops; the arrangement emphasizes the 808 bass and vocoder
- **spirit** (100-200 words): Electro pursues a robotic funk through 808 programming and vocoder identity. Good examples feel like a machine grooving — the 808 patterns are syncopated and funky, the bass is melodic and heavy, the vocoder adds a futuristic vocal element. The genre's signature is the robotic-funky duality. Lazy examples use a generic 808 pattern with no syncopation and a flat bass — they have the 808 sound but not the funk. Electro without funk is just "808 track"; the skill is making the machine move.
- **common_failure_modes** (at least 3): no syncopation (rigid 808); flat 808 bass (not melodic); no vocoder/identity element; missing the funk
- **Body** (200-400 words): Brief context (the electro tradition, 808, the hip-hop/funk/electronic intersection), the spirit, good vs lazy execution. Original prose, cite sources.
- **Sources**: At least 2.

- [ ] **Step 2: Validate**

Run: `.venv/bin/python -c "from electronic_music_mentor.substrates.loader import load_genre_profile; from pathlib import Path; p = load_genre_profile(Path('knowledge/genres/electro.md')); print(f'Loaded: {p[\"name\"]}')"`

- [ ] **Step 3: Commit**

```bash
git add knowledge/genres/electro.md
git commit -m "docs: genre profile — electro"
```

---

### Task 10: Genre profile — IDM / Braindance

**Files:**
- Create: `knowledge/genres/idm-braindance.md`

- [ ] **Step 1: Research and write the IDM / Braindance profile**

Content requirements:
- **name**: IDM / Braindance
- **tempo_range**: min 70, max 180, feel "unpredictable, intricate, exploratory" (IDM has no fixed tempo — it ranges from downtempo to fast)
- **rhythmic_conventions** (at least 3): complex/irregular rhythms; programmed drums with human feel; polyrhythm; the groove is unpredictable — IDM doesn't commit to one grid; the rhythm is part of the exploration
- **harmonic_conventions** (at least 3): often modal or atonal; chromatic harmony; unusual chord voicings; the harmony is exploratory, not genre-bound — IDM uses harmony as color, not as function
- **textural_sonic_conventions** (at least 3): intricate sound design; granular and processed textures; found sounds; the texture is the content — IDM is as much about *what the sounds are* as what they play
- **arrangement_conventions** (at least 3): unpredictable structure; no standard build-drop; sections often contrast sharply; the arrangement is part of the exploration — IDM doesn't follow genre structure
- **spirit** (100-200 words): IDM/braindance pursues exploration and intricacy over groove and genre convention. Good examples are unpredictable — the rhythm shifts, the harmony surprises, the texture is sculpted and strange, the structure doesn't follow a template. The genre's signature is the *intention to explore* — each track is an experiment in what electronic music can do. Lazy examples use complex rhythms and weird sounds without coherence — they have the surface of IDM (intricate) but not the depth (intentional exploration). IDM isn't "weird for weird's sake"; it's "each choice serves the exploration."
- **common_failure_modes** (at least 3): weird for weird's sake (no coherence); no groove at all (forgetting that even complex music needs to move); muddy mix (too many intricate elements competing); no emotional core (complex but cold)
- **Body** (200-400 words): Brief context (Rephlex, Aphex Twin, the "intelligent dance music" term and its controversy, the braindance alternative), the spirit, good vs lazy execution. Original prose, cite sources.
- **Sources**: At least 2.

- [ ] **Step 2: Validate**

Run: `.venv/bin/python -c "from electronic_music_mentor.substrates.loader import load_genre_profile; from pathlib import Path; p = load_genre_profile(Path('knowledge/genres/idm-braindance.md')); print(f'Loaded: {p[\"name\"]}')"`

- [ ] **Step 3: Commit**

```bash
git add knowledge/genres/idm-braindance.md
git commit -m "docs: genre profile — idm / braindance"
```

---

### Task 11: Update genres README and final validation

**Files:**
- Modify: `knowledge/genres/README.md`

- [ ] **Step 1: Update the genres README**

Replace the contents of `knowledge/genres/README.md` with:

```markdown
# Genre Profiles Substrate

One file per electronic music genre, encoding the spirit of each genre. Consumed by all domain skills.

## Documents

- [Dub Techno](dub-techno.md) — hypnotic immersion through repetition and slow change
- [Deep House](deep-house.md) — warmth and soul through groove and harmony
- [Detroit Techno](detroit-techno.md) — mechanical precision with emotive depth
- [Jungle / Drum & Bass](jungle-drum-and-bass.md) — breakbeat energy and sub-bass weight
- [UK Garage](uk-garage.md) — bouncy, forward-leaning swing and broken patterns
- [Ambient](ambient.md) — atmosphere and sustained mood over rhythm
- [Minimal Techno](minimal-techno.md) — depth through reduction; each element matters more
- [Electro](electro.md) — robotic funk through 808 programming and vocoder
- [IDM / Braindance](idm-braindance.md) — exploration and intricacy over groove and convention

## Format

Each genre profile is a markdown file with YAML front-matter validated by `electronic_music_mentor.substrates.validator.validate_genre_profile`, loaded by `electronic_music_mentor.substrates.loader.load_genre_profile`:
- `name`
- `tempo_range` (dict with `min`, `max`, `feel`)
- `rhythmic_conventions` (list)
- `harmonic_conventions` (list)
- `textural_sonic_conventions` (list)
- `arrangement_conventions` (list)
- `spirit` (substantial prose — what the genre is trying to do, what good examples do, what lazy examples miss)
- `common_failure_modes` (list)
- `## Sources` section at the bottom with attributions
```

- [ ] **Step 2: Validate all genre profiles load cleanly**

Run: `.venv/bin/python -c "
from electronic_music_mentor.substrates.loader import load_genre_profile
from pathlib import Path
genres = ['dub-techno', 'deep-house', 'detroit-techno', 'jungle-drum-and-bass', 'uk-garage', 'ambient', 'minimal-techno', 'electro', 'idm-braindance']
for g in genres:
    p = load_genre_profile(Path(f'knowledge/genres/{g}.md'))
    print(f'{p[\"name\"]}: tempo {p[\"tempo_range\"][\"min\"]}-{p[\"tempo_range\"][\"max\"]}, {len(p[\"rhythmic_conventions\"])} rhythmic, {len(p[\"common_failure_modes\"])} failure modes')
print('All genre profiles loaded successfully')
"`
Expected: prints a line per genre (9 total) and "All genre profiles loaded successfully" with no errors.

- [ ] **Step 3: Run the full test suite**

Run: `.venv/bin/pytest tests/ -v`
Expected: PASS (34 tests — no regressions)

- [ ] **Step 4: Commit**

```bash
git add knowledge/genres/README.md
git commit -m "docs: update genres README with completed profile index"
```

---

## Self-Review

**1. Spec coverage:**
- Loader extension for genre profiles — ✓ (Task 1)
- 9 genre profiles from the planned list — ✓ (Tasks 2-10)
- Dub Techno — ✓ (Task 2)
- Deep House — ✓ (Task 3)
- Detroit Techno — ✓ (Task 4)
- Jungle / Drum & Bass — ✓ (Task 5)
- UK Garage — ✓ (Task 6)
- Ambient — ✓ (Task 7)
- Minimal Techno — ✓ (Task 8)
- Electro — ✓ (Task 9)
- IDM / Braindance — ✓ (Task 10)
- Genres README updated — ✓ (Task 11)
- Sourcing rules — ✓ (each task requires original prose with attributions)

**2. Placeholder scan:** No TBD or TODO. Each content task specifies exact requirements (name, tempo range, minimum conventions per field, spirit length, body length, source count).

**3. Type consistency:** `load_genre_profile(path)` returns a dict with front-matter fields plus `body` key, paralleling `load_theory_document`. The validator's `GENRE_PROFILE_REQUIRED_FIELDS` matches the front-matter fields specified in each content task. The `tempo_range` is a dict with `min`, `max`, `feel` — consistent across validator, loader, and content tasks.