# Electronic Music Mentor — Domain Skills Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the remaining 5 domain skills — `melody`, `rhythm`, `harmony`, `sound-design`, `arrangement` — each as an opencode skill (SKILL.md) following the pattern established by the `bass` skill. Each skill defines when to invoke, its boundaries with other skills, the workflow (pre-phase, understand, generate/critique, written reasoning, post-phase), and its output contract.

**Architecture:** Each skill is a directory under `skills/` with a `SKILL.md`. Skills reference the shared mentor guidance, consult the knowledge substrates (`knowledge/theory/` and `knowledge/genres/`), use the Python infrastructure (`MemoryStore`, `EscapeHatchTracker`, `MidWriter`), and follow the distributed orchestrator pattern (pre/post-phase behaviors documented in each skill's workflow, pointing at the shared guidance).

**Tech Stack:** Markdown (SKILL.md files), Python infrastructure (from Plan 1), knowledge substrates (from Plans 2-3).

---

## File Structure

```
Electronic_Music_Mentor/
├── skills/
│   ├── README.md                                     # (exists) update to remove "(planned)" from completed skills
│   ├── bass/                                         # (exists) completed in Plan 1
│   │   └── SKILL.md
│   ├── melody/                                       # (new) Task 1
│   │   └── SKILL.md
│   ├── rhythm/                                       # (new) Task 2
│   │   └── SKILL.md
│   ├── harmony/                                      # (new) Task 3
│   │   └── SKILL.md
│   ├── sound-design/                                 # (new) Task 4
│   │   └── SKILL.md
│   └── arrangement/                                  # (new) Task 5
│       └── SKILL.md
```

---

## SKILL.md Pattern (followed by all 5 skills)

Each SKILL.md follows this structure (established by `bass/SKILL.md`):

```markdown
# Skill: <name>

## When to invoke
<When to invoke this skill. What it owns. Explicit "do not invoke for X" boundaries with other skills.>

## Shared guidance
Follow the shared mentor voice, guards, and post-phase behaviors defined in [`../../docs/superpowers/mentor-guidance.md`](../../docs/superpowers/mentor-guidance.md). In particular:
- Apply the taste-probe before aesthetic decisions (not for craft issues).
- Recall relevant memory before running.
- Include woven teaching — concrete, verifiable, tied to the work. No generic wisdom.
- Declare observations aloud after running (mentor voice).
- Track escape-hatch use if the user invokes with `just-give-it-to-me`.

## Workflow
### 1. Pre-phase
1. Recall memory observations for domains [...].
2. Surface relevant memory to the user.
3. If aesthetic, apply taste-probe.

### 2. Understand the request
Determine: genre (consult knowledge/genres/), relevant theory (consult knowledge/theory/), user's goal.

### 3. Generate or critique
**To generate:** <How to generate, including MidWriter code if MIDI-producing. What to reason about.>
**To critique:** <What to assess.>

### 4. Written reasoning output
Produce written reasoning. Explain choices. Include woven teaching (concrete, checkable). State opinions as mentor's take. Yield if overridden.

### 5. Post-phase
1. Declare observations (mentor voice). Update memory via MemoryStore.declare(...).
2. Track escape-hatch via EscapeHatchTracker.record("tool"/"mentor").
3. Check for lesson escalation (>=3 sessions).

## Output contract
- <What the skill produces>
- Written reasoning with woven teaching.
- Declared observations.
- Optional: lesson artifact.
```

---

### Task 1: Skill — `melody`

**Files:**
- Create: `skills/melody/SKILL.md`

- [ ] **Step 1: Write the melody skill SKILL.md**

Write `skills/melody/SKILL.md` following the SKILL.md pattern. Specific content for melody:

**When to invoke:** Invoke when the user wants to write, generate, or critique a melody, lead, motif, or top-line for an electronic music track. Also invoke for motif construction, repetition/variation, and contour.

Boundaries (do not invoke for): the chords the melody implies — that's `harmony`. The melodic line and its internal logic are `melody`'s domain. Do not invoke for bass lines — that's `bass`. Do not invoke for rhythm of non-melodic elements — that's `rhythm`. Do not invoke for the sound of the lead (synth patch) — that's `sound-design`.

**Pre-phase:** Recall memory for domains `["melody"]`. Surface relevant memory. Apply taste-probe for aesthetic decisions (melody direction, mood, contour) — melody is highly aesthetic, so taste-probe is particularly important here.

**Understand the request:** Determine the genre (consult `knowledge/genres/` — its harmonic conventions shape what melodic notes fit), the harmonic context (if chords are known, consult `knowledge/theory/voice-leading.md` and `knowledge/theory/diatonic-harmony.md` for scale tones and tension notes; consult the `harmony` skill if a progression is needed), the phrase length (consult `knowledge/theory/phrase-and-form.md`), and the user's goal (generate, fix, critique).

**Generate:** Use `MidWriter.write_bassline` (works for any monophonic line — the method name is "bassline" but it writes any single-note MIDI line; set `program` to a lead instrument like 80 or 81 for synth lead). Reason about:
- **Motif construction**: the smallest melodic idea — consult `knowledge/theory/phrase-and-form.md` for motif principles. A good motif is memorable and developable.
- **Repetition and variation**: repeat the motif, vary it (change one thing, keep the rest). Consult `knowledge/theory/phrase-and-form.md`.
- **Contour**: the shape of the melody — rising, falling, arch. Genre informs contour (house melodies often repetitive and cyclical; techno melodies often minimal and static; IDM melodies often jagged and unpredictable).
- **Rhythmic placement**: where the melody sits relative to the groove. Consult the genre profile's `rhythmic_conventions`.
- **Harmonic relationship**: which scale tones the melody uses, where tension notes are placed (consult `knowledge/theory/tension-and-release.md`).

Example MidWriter code:
```python
from electronic_music_mentor.midi.writer import MidWriter

notes = [
    {"note": 72, "length_beats": 0.5, "velocity": 90},  # C5
    {"note": 74, "length_beats": 0.5, "velocity": 90},  # D5
    {"note": 72, "length_beats": 0.5, "velocity": 90},  # C5
    {"note": 77, "length_beats": 1.0, "velocity": 100},  # F5
]
writer = MidWriter()
writer.write_bassline(notes, "output/melody.mid", bpm=124, program=81)  # 81 = Lead 2 (sawtooth)
```

**Critique:** Assess motif strength (is it memorable?), repetition/variation balance (too repetitive? too varied?), contour appropriateness for genre, rhythmic placement, harmonic relationship (are tension notes used effectively?).

**Written reasoning:** Explain motif logic, contour, rhythmic placement, relationship to chords. Woven teaching must be concrete: "The melody lands on the third of the chord on beat 1 — that's why it feels resolved. If it landed on the ninth, it would float more." Not: "Melodies should be memorable."

**Output contract:** A `.mid` file (if generating), written reasoning with woven teaching, declared observations, optional lesson artifact.

- [ ] **Step 2: Commit**

```bash
git add skills/melody/SKILL.md
git commit -m "feat: melody skill SKILL.md"
```

---

### Task 2: Skill — `rhythm`

**Files:**
- Create: `skills/rhythm/SKILL.md`

- [ ] **Step 1: Write the rhythm skill SKILL.md**

**When to invoke:** Invoke when the user wants to write, generate, or critique a rhythmic pattern, groove, or percussion content (kick patterns, hat patterns, percussion arrangement). Also invoke for groove feel (swing, pocket, velocity patterns).

Boundaries (do not invoke for): the *sound* of percussion (synth patch, timbre) — that's `sound-design`. The *notes* of non-percussion elements — that's the relevant domain skill. *Harmonic rhythm* (the rate of chord changes) — that's `harmony`/`arrangement`. `rhythm` owns rhythmic content only (note placement, velocity, role).

**Pre-phase:** Recall memory for domains `["rhythm"]`. Apply taste-probe for aesthetic groove decisions (e.g., "how loose do you want the groove?") — but not for craft issues (e.g., "the kick is off-grid and it sounds like a mistake").

**Understand the request:** Determine the genre (consult `knowledge/genres/` — its `rhythmic_conventions` are the primary input for rhythm), the groove feel (swing, pocket — consult `knowledge/theory/rhythmic-subdivision.md`), the phrase length, and the user's goal.

**Generate:** Use `MidWriter.write_percussion` for percussion patterns. Reason about:
- **Groove feel**: swing amount, pocket (where the kick sits). Consult `knowledge/theory/rhythmic-subdivision.md` and the genre profile.
- **Velocity patterns**: where hits are loud vs. soft. Velocity is as important as timing for groove.
- **Layer roles**: kick (foundation), snare/clap (backbeat), hats (subdivision), percussion (color). Each layer has a role.
- **Density**: how many elements, how busy. Genre informs density (minimal techno is sparse; jungle is dense).

Example MidWriter code:
```python
from electronic_music_mentor.midi.writer import MidWriter

hits = [
    {"note": 36, "position_beats": 0.0, "length_beats": 0.5, "velocity": 120},  # kick
    {"note": 38, "position_beats": 1.0, "length_beats": 0.25, "velocity": 100},  # snare
    {"note": 36, "position_beats": 2.0, "length_beats": 0.5, "velocity": 120},  # kick
    {"note": 38, "position_beats": 3.0, "length_beats": 0.25, "velocity": 100},  # snare
    {"note": 42, "position_beats": 0.5, "length_beats": 0.25, "velocity": 80},   # hat
    {"note": 42, "position_beats": 1.5, "length_beats": 0.25, "velocity": 80},   # hat
    {"note": 42, "position_beats": 2.5, "length_beats": 0.25, "velocity": 80},   # hat
    {"note": 42, "position_beats": 3.5, "length_beats": 0.25, "velocity": 80},   # hat
]
writer = MidWriter()
writer.write_percussion(hits, "output/rhythm.mid", bpm=124)
```

**Critique:** Assess groove feel (is the swing right for the genre?), velocity patterns (is there dynamic life?), layer roles (is each element doing its job?), density (too busy? too sparse?), and the relationship to the bass (bass and kick share the low end — consult `knowledge/theory/rhythmic-subdivision.md`).

**Written reasoning:** Explain groove feel, velocity choices, layer roles, density. Woven teaching: "The kick is on every beat but the hats are swung — that's what creates the forward lean. Straight hats would feel rigid." Not: "Groove is important."

**Output contract:** A `.mid` file (if generating), written reasoning, declared observations, optional lesson artifact.

- [ ] **Step 2: Commit**

```bash
git add skills/rhythm/SKILL.md
git commit -m "feat: rhythm skill SKILL.md"
```

---

### Task 3: Skill — `harmony`

**Files:**
- Create: `skills/harmony/SKILL.md`

- [ ] **Step 1: Write the harmony skill SKILL.md**

**When to invoke:** Invoke when the user wants to write, generate, or critique chords, progressions, voicings, or tonality. Also invoke for harmonic analysis ("what's the progression?", "what key is this?") and for harmonic rhythm decisions.

Boundaries (do not invoke for): the *bass part* — that's `bass` (bass consults `harmony` for progression logic, but owns the bass notes). The *melody part* — that's `melody`. `harmony` provides harmonic context that `bass` and `melody` consult and work within. Can be invoked standalone ("give me a progression for this section").

**Pre-phase:** Recall memory for domains `["harmony"]`. Apply taste-probe for aesthetic harmonic decisions (e.g., "do you want this dark or bright?") — but not for craft issues (e.g., "that chord clashes with the bass").

**Understand the request:** Determine the genre (consult `knowledge/genres/` — its `harmonic_conventions` are the primary input), the tonal center, the phrase length, and the user's goal. Consult the relevant theory documents:
- `knowledge/theory/diatonic-harmony.md` — for diatonic progressions
- `knowledge/theory/chromatic-harmony.md` — for borrowed chords, secondary dominants, modulation
- `knowledge/theory/static-harmony.md` — for pedal points and two-chord loops
- `knowledge/theory/bass-as-harmony.md` — for when bass carries the harmony
- `knowledge/theory/tension-and-release.md` — for harmonic tension/release

**Generate:** Use `MidWriter.write_chords` for chord stabs/pads. Reason about:
- **Progression logic**: what chords, in what order, and why. Consult the theory documents for the principles.
- **Voicing**: how the chord is voiced (open vs. closed, which inversion, where in the register). Voicing is critical in electronic music — consult `knowledge/theory/voice-leading.md` for spacing principles (avoid low-mid overcrowding).
- **Tension/release**: where the progression creates and releases tension. Consult `knowledge/theory/tension-and-release.md`.
- **Genre harmonic conventions**: how much harmony, what kind. Dub techno: static. House: diatonic stabs. Techno: often none or bass-as-harmony.
- **Harmonic rhythm**: how fast the chords change. Consult `knowledge/theory/phrase-and-form.md`.

Example MidWriter code:
```python
from electronic_music_mentor.midi.writer import MidWriter

chords = [
    {"notes": [48, 55, 60, 64], "length_beats": 2.0, "velocity": 90},  # Cm (C3 G3 C4 Eb4)
    {"notes": [44, 51, 56, 60], "length_beats": 2.0, "velocity": 90},  # Abmaj7 (Ab2 Eb3 Ab3 C4)
]
writer = MidWriter()
writer.write_chords(chords, "output/chords.mid", bpm=124, program=4)  # 4 = Electric Piano 1
```

Or roman-numeral/ABC notation for non-MIDI output:
```
|: i - - - | bVI - - - | bVII - - - | i - - - :|
```

**Critique:** Assess progression logic (does it work? is it genre-appropriate?), voicing (is the spacing good? is the low-mid overcrowded?), tension/release (is there direction?), genre fit (does the harmony match the genre's conventions?).

**Written reasoning:** Explain progression logic, voicing choices, tension/release, genre conventions in play. Woven teaching: "The voicing puts the third in the middle register because the bass is carrying the root — that's why the chord feels complete without being muddy." Not: "Voicing matters."

**Output contract:** A `.mid` file or roman-numeral/ABC notation (if generating), written reasoning, declared observations, optional lesson artifact.

- [ ] **Step 2: Commit**

```bash
git add skills/harmony/SKILL.md
git commit -m "feat: harmony skill SKILL.md"
```

---

### Task 4: Skill — `sound-design`

**Files:**
- Create: `skills/sound-design/SKILL.md`

- [ ] **Step 1: Write the sound-design skill SKILL.md**

**When to invoke:** Invoke when the user wants to reason about or design the *sound* of an element — patch architecture, synthesis choices, texture, timbre. "How do I make a dub techno pad?", "What synth should I use for this bass?", "How do I get that Reese sound?"

Boundaries (do not invoke for): the *notes* — that's the relevant domain skill. `sound-design` does not produce patches (no DAW connection — can't hand the user a preset). Produces written reasoning + parameter *guidance* (named synth architectures, suggested parameter ranges, signal-flow descriptions). Does not invoke for mix decisions (EQ, compression) — those are out of scope entirely (the system can't hear audio).

**Pre-phase:** Recall memory for domains `["sound-design"]`. Apply taste-probe for aesthetic sound decisions (e.g., "warm or cold for this pad?") — sound design is highly aesthetic.

**Understand the request:** Determine the genre (consult `knowledge/genres/` — its `textural_sonic_conventions` are the primary input for sound design), the element being designed (pad, bass, lead, percussion, texture), and the user's goal.

**Generate (reasoning, not patches):** Produce written reasoning about:
- **Synthesis approach**: subtractive, FM, wavetable, granular — which serves the sound. Consult the genre profile for the textural world.
- **Parameter guidance**: suggested ranges (e.g., "long attack (~2-5 seconds), slow filter LFO (~0.5-1 Hz on a lowpass filter), detuned oscillators (-7 to +7 cents)").
- **Signal flow**: what goes where (e.g., "oscillators → filter → reverb → delay; reverb on a send, not insert, for space").
- **What to listen for**: concrete, checkable guidance (e.g., "the pad should breathe — the filter LFO should make the brightness swell and recede, not sit static").
- **Genre fit**: how the sound serves the genre's textural conventions.

No MidWriter code — sound-design produces written reasoning only.

**Critique:** Assess synthesis approach (is it right for the sound?), parameter choices (are the ranges sensible?), signal flow (does the routing serve the sound?), genre fit (does the sound match the genre's textural world?), and register/spacing (does the sound crowd other elements?).

**Written reasoning:** Explain synthesis approach, parameter guidance, signal flow, what to listen for, genre fit. Woven teaching: "The detuned oscillators create the chorus-like wobble — that's what gives the pad its movement. Without detune, it'd be static." Not: "Detune adds character."

**Output contract:** Written reasoning only (no MIDI, no patches). Synthesis approach, parameter guidance, signal flow, what to listen for, with woven teaching. Declared observations. Optional lesson artifact.

- [ ] **Step 2: Commit**

```bash
git add skills/sound-design/SKILL.md
git commit -m "feat: sound-design skill SKILL.md"
```

---

### Task 5: Skill — `arrangement`

**Files:**
- Create: `skills/arrangement/SKILL.md`

- [ ] **Step 1: Write the arrangement skill SKILL.md**

**When to invoke:** Invoke when the user wants to plan, critique, or restructure the section structure, energy arc, or transitions of a track. "Help me structure this track", "the arrangement feels flat", "how do I transition from the build to the drop?"

Boundaries (do not invoke for): generating parts — calls other domain skills for content. `arrangement` owns the *shape* of the track and the *role* of each section. `critique` and `diagnose` consult arrangement knowledge independently. Does not own domain expertise — delegates to domain skills.

**Pre-phase:** Recall memory for domains `["arrangement"]`. Apply taste-probe for aesthetic arrangement decisions (e.g., "do you want this to build slowly or hit hard early?") — arrangement is highly aesthetic.

**Understand the request:** Determine the genre (consult `knowledge/genres/` — its `arrangement_conventions` are the primary input), the current state of the track (if the user has one), and the user's goal (plan from scratch, critique existing, fix a specific transition).

**Generate (arrangement plan, not MIDI):** Produce a written arrangement plan. Reason about:
- **Section list**: what sections (intro, build, drop, breakdown, outro) and in what order. Consult the genre profile.
- **Energy arc**: how energy builds and releases across the track. Consult `knowledge/theory/tension-and-release.md`.
- **Section roles**: what each section does (intro sets the mood, build creates tension, drop releases it, breakdown provides contrast).
- **Transitions**: how to move between sections (filter sweeps, layer addition/removal, rhythmic shifts). Consult `knowledge/theory/phrase-and-form.md` for phrase length.
- **Layer management**: what enters/exits when. Arrangement in electronic music is often additive/subtractive.
- **Phrase length**: 4, 8, or 16-bar phrases. Consult `knowledge/theory/phrase-and-form.md`.

Example arrangement plan output:
```
Section 1: Intro (16 bars) — sparse, just kick and bass
Section 2: Build (16 bars) — add percussion, then stabs, filter opens
Section 3: Drop (32 bars) — full energy, all elements
Section 4: Breakdown (16 bars) — remove percussion, pads only
Section 5: Build 2 (16 bars) — re-add elements
Section 6: Drop 2 (32 bars) — full energy
Section 7: Outro (8 bars) — strip back to kick and bass, fade
```

**Critique:** Assess section structure (does it flow? are sections in the right order?), energy arc (does it build and release effectively?), transitions (are they smooth or jarring?), section roles (is each section doing its job?), phrase length (are phrases consistent?), and genre fit (does the arrangement match the genre's conventions?).

**Written reasoning:** Explain section structure, energy arc, transitions, layer management. Woven teaching: "The build is 16 bars because that's four 4-bar phrases — the listener expects a change at 16, so the drop lands on the expected bar. Cutting the build to 8 bars would feel rushed." Not: "Builds should be the right length."

**Output contract:** A written arrangement plan (section list with roles, energy curve, transition notes, layer management). No MIDI directly (but references artifacts from other skills). Declared observations. Optional lesson artifact.

- [ ] **Step 2: Commit**

```bash
git add skills/arrangement/SKILL.md
git commit -m "feat: arrangement skill SKILL.md"
```

---

### Task 6: Update skills README

**Files:**
- Modify: `skills/README.md`

- [ ] **Step 1: Update the skills README**

In `skills/README.md`, update the skill inventory to remove "(planned)" from the now-completed domain skills. The Domain skills section should become:

```markdown
### Domain skills (generate + critique within one domain)

- `bass` — basslines, sub, low-end voice-leading
- `melody` — leads, motifs, top-line development
- `rhythm` — patterns, grooves, percussion content
- `harmony` — chords, progressions, voicings, tonality
- `sound-design` — conceptual sound-design mentoring, synthesis reasoning
- `arrangement` — section structure, energy arc, transitions
```

Leave the other sections (Track-construction skill, Cross-domain act skills, Development skills) with "(planned)" as they are — those are built in Plan 5.

- [ ] **Step 2: Run the full test suite**

Run: `.venv/bin/pytest tests/ -v`
Expected: PASS (34 tests — no regressions; this is a documentation-only change)

- [ ] **Step 3: Commit**

```bash
git add skills/README.md
git commit -m "docs: update skills README — domain skills complete"
```

---

## Self-Review

**1. Spec coverage:**
- melody skill — ✓ (Task 1)
- rhythm skill — ✓ (Task 2)
- harmony skill — ✓ (Task 3)
- sound-design skill — ✓ (Task 4)
- arrangement skill — ✓ (Task 5)
- skills README updated — ✓ (Task 6)

All 5 skills follow the SKILL.md pattern established by `bass` (When to invoke, Shared guidance, Workflow with pre/post-phase, Output contract). Each skill's boundaries are explicitly defined (do not invoke for X — that's Y). Each skill references the shared mentor guidance, the knowledge substrates, and the Python infrastructure.

**2. Placeholder scan:** No TBD or TODO. Each task specifies the exact content requirements for its SKILL.md.

**3. Consistency:** All skills reference the same shared guidance path (`../../docs/superpowers/mentor-guidance.md`), use the same MidWriter API (`write_bassline`, `write_chords`, `write_percussion`), and follow the same pre/post-phase pattern. The domain lists in pre-phase recall match each skill's domain.