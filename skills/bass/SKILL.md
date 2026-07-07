# Skill: bass

## When to invoke

Invoke when the user wants to write, generate, or critique a bassline or bass part for an electronic music track. Also invoke when the user asks about bass register, sub, low-end voice-leading, or the relationship between bass and kick.

Do not invoke for harmony decisions when chords are present — that's `harmony`. `bass` consults `harmony` when needed. Do not invoke for percussion — that's `rhythm`. Do not invoke for the sound of the bass (synth patch, timbre) — that's `sound-design`. `bass` owns the bass *notes* and *role*.

## Shared guidance

Follow the shared mentor voice, guards, and post-phase behaviors defined in [`../../docs/superpowers/mentor-guidance.md`](../../docs/superpowers/mentor-guidance.md). In particular:

- Apply the taste-probe before aesthetic decisions about bass direction (not for craft issues like bass-kick clashing).
- Recall relevant memory before running (habits related to bass, low-mid, low-end).
- Include woven teaching in the written reasoning — concrete, verifiable, tied to the work in front of the user. No generic wisdom.
- Declare observations aloud after running (e.g., "you're overcrowding the low-mid again" — mentor voice, not database voice).
- Track escape-hatch use if the user invokes with `just-give-it-to-me`.

## Workflow

### 1. Pre-phase

1. Recall memory observations for domains `["bass", "arrangement", "sound-design"]` (bass habits often surface as arrangement or sound-design issues).
2. Surface relevant memory to the user. Example: "Last time your bass was clashing with the kick at 80Hz — bringing something on that today, or starting fresh?"
3. If the decision is aesthetic (bass direction, vibe, register choice) and the user hasn't voiced a preference recently, apply the taste-probe: "Before I weigh in — what direction are you hearing for the bass?"

### 2. Understand the request

Determine:
- The genre (consult `knowledge/genres/` for the relevant profile — its `harmonic_conventions` and `rhythmic_conventions` shape what the bass should do).
- The harmonic context (if chords are present or known, consult `knowledge/theory/` for voice-leading principles; consult the `harmony` skill if a progression is needed).
- The rhythmic context (where the kick sits — bass and kick share the low end; consult the genre profile for typical kick patterns).
- The user's goal: generate a new bassline, fix an existing one, or critique.

### 3. Generate or critique

**To generate a bassline:**

Use the `MidWriter` to write a `.mid` file. The bassline is a list of note specs:
```python
from electronic_music_mentor.midi.writer import MidWriter

notes = [
    {"note": 36, "length_beats": 1.0, "velocity": 100},  # C2
    {"note": 36, "length_beats": 1.0, "velocity": 100},
    {"note": 43, "length_beats": 1.0, "velocity": 100},  # G2
    {"note": 41, "length_beats": 1.0, "velocity": 100},  # F2
]
writer = MidWriter()
writer.write_bassline(notes, "output/bassline.mid", bpm=124)
```

Reason about:
- **Register**: where in the bass range (C2-C3 for sub, higher for melodic bass). Genre profile informs this.
- **Rhythmic relationship to kick**: bass and kick share the low end. In four-on-the-floor genres, bass often sits around the kick or in the gaps. Consult the genre profile's `rhythmic_conventions`.
- **Harmonic role**: is the bass carrying the harmony (common in electronic music — bass on root, chord stab on top), or sitting under chordal harmony? Consult `knowledge/theory/` for bass-as-harmony principles.
- **Voice-leading**: smooth bass movement vs. idiomatic wide leaps. In electronic music, wide bass leaps are often fine when bass carries the harmony.

**To critique a bassline** (the user provides MIDI or describes it):

Assess:
- Register appropriateness for the genre.
- Rhythmic relationship to the kick (frequency clashes, doubling, counterpoint).
- Harmonic role clarity (is the bass carrying the harmony clearly, or muddying it?).
- Voice-leading (genre-appropriate or not).

### 4. Written reasoning output

Produce written reasoning alongside the `.mid` file. The reasoning must:
- Explain the choices (role, register, rhythmic relationship to kick, why these notes).
- Include woven teaching — concrete, checkable, tied to this bassline. Example: "The bass is on root and fifth because the chord stab carries the third — listen to how the low end stays clear when the stab hits." Not: "Less is more in the low end."
- State opinions as the mentor's take with reasoning. Yield if the user overrides.

### 5. Post-phase

1. Declare any observations aloud (mentor voice). If the bass overcrowds the low-mid the same way as a previous session, say so: "You're doing that low-mid thing again." Update memory via `MemoryStore.declare(...)`.
2. If the user invoked with `just-give-it-to-me`, record a tool-path invocation via `EscapeHatchTracker.record("tool")`. Otherwise record a mentor-path invocation.
3. Check for lesson escalation: if a bass concept has recurred across >=3 sessions, produce a standalone lesson artifact.

## Output contract

- A `.mid` file (if generating) at the requested path.
- Written reasoning: role, register, rhythmic relationship to kick, harmonic context, why these notes, with woven teaching.
- Declared observations (spoken aloud, written to memory).
- Optional: a lesson artifact if escalation is triggered.