# Skill: rhythm

## When to invoke

Invoke when the user wants to write, generate, or critique a rhythmic pattern, groove, or percussion content (kick patterns, hat patterns, percussion arrangement). Also invoke for groove feel — swing, pocket, velocity patterns.

Do not invoke for the *sound* of percussion (synth patch, timbre) — that's `sound-design`. Do not invoke for the *notes* of non-percussion elements — that's the relevant domain skill. Do not invoke for *harmonic rhythm* (the rate of chord changes) — that's `harmony`/`arrangement`. `rhythm` owns rhythmic content only (note placement, velocity, role).

## Shared guidance

Follow the shared mentor voice, guards, and post-phase behaviors defined in [`../../docs/superpowers/mentor-guidance.md`](../../docs/superpowers/mentor-guidance.md). In particular:

- Apply the taste-probe before aesthetic groove decisions (e.g., "how loose do you want the groove?") — not for craft issues (e.g., "the kick is off-grid and it sounds like a mistake").
- Recall relevant memory before running (habits related to rhythm, groove, percussion).
- Include woven teaching in the written reasoning — concrete, verifiable, tied to the work in front of the user. No generic wisdom.
- Declare observations aloud after running (e.g., "you're stacking hats again and it's cluttering the pocket" — mentor voice, not database voice).
- Track escape-hatch use if the user invokes with `just-give-it-to-me`.

## Workflow

### 1. Pre-phase

1. Recall memory observations for domains `["rhythm"]`.
2. Surface relevant memory to the user. Example: "Last time your hats were drowning the snare — keeping the pocket clean today?"
3. If the decision is aesthetic (groove feel, swing amount, pocket) and the user hasn't voiced a preference recently, apply the taste-probe: "Before I weigh in — how loose do you want the groove?"

### 2. Understand the request

Determine:
- The genre (consult `knowledge/genres/` for the relevant profile — its `rhythmic_conventions` are the primary input for rhythm).
- The groove feel (swing amount, pocket — where the kick sits). Consult `knowledge/theory/rhythmic-subdivision.md`.
- The phrase length (4, 8, or 16 bars). Consult `knowledge/theory/phrase-and-form.md`.
- The user's goal: generate a new pattern, fix an existing one, or critique.

### 3. Generate or critique

**To generate a percussion pattern:**

Use `MidWriter.write_percussion` to write a `.mid` file. The pattern is a list of hit specs (each hit has `position_beats`, not just sequential ordering):
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

Reason about:
- **Groove feel**: swing amount, pocket (where the kick sits). Consult `knowledge/theory/rhythmic-subdivision.md` and the genre profile.
- **Velocity patterns**: where hits are loud vs. soft. Velocity is as important as timing for groove — a flat-velocity loop feels mechanical.
- **Layer roles**: kick (foundation), snare/clap (backbeat), hats (subdivision), percussion (color). Each layer has a role; know which layer each hit belongs to.
- **Density**: how many elements, how busy. Genre informs density — minimal techno is sparse; jungle is dense.

**To critique a rhythm** (the user provides MIDI or describes it):

Assess:
- Groove feel: is the swing right for the genre?
- Velocity patterns: is there dynamic life, or is everything at one velocity?
- Layer roles: is each element doing its job, or are layers stepping on each other?
- Density: too busy, too sparse, or just right for the genre?
- Relationship to the bass: bass and kick share the low end. Consult `knowledge/theory/rhythmic-subdivision.md`.

### 4. Written reasoning output

Produce written reasoning alongside the `.mid` file. The reasoning must:
- Explain the choices (groove feel, velocity patterns, layer roles, density).
- Include woven teaching — concrete, checkable, tied to this pattern. Example: "The kick is on every beat but the hats are swung — that's what creates the forward lean. Straight hats would feel rigid." Not: "Groove is important."
- State opinions as the mentor's take with reasoning. Yield if the user overrides.

### 5. Post-phase

1. Declare any observations aloud (mentor voice). If the groove is cluttered the same way as a previous session, say so: "You're overstacking the hats again." Update memory via `MemoryStore.declare(...)`.
2. If the user invoked with `just-give-it-to-me`, record a tool-path invocation via `EscapeHatchTracker.record("tool")`. Otherwise record a mentor-path invocation.
3. Check for lesson escalation: if a rhythm concept has recurred across >=3 sessions, produce a standalone lesson artifact.

## Output contract

- A `.mid` file (if generating) at the requested path.
- Written reasoning: groove feel, velocity choices, layer roles, density, relationship to bass, with woven teaching.
- Declared observations (spoken aloud, written to memory).
- Optional: a lesson artifact if escalation is triggered.