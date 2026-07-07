# Skill: harmony

## When to invoke

Invoke when the user wants to write, generate, or critique chords, progressions, voicings, or tonality. Also invoke for harmonic analysis ("what's the progression?", "what key is this?") and for harmonic rhythm decisions.

Do not invoke for the *bass part* — that's `bass` (bass consults `harmony` for progression logic, but owns the bass notes). Do not invoke for the *melody part* — that's `melody`. `harmony` provides harmonic context that `bass` and `melody` consult and work within. Can be invoked standalone ("give me a progression for this section").

## Shared guidance

Follow the shared mentor voice, guards, and post-phase behaviors defined in [`../../docs/superpowers/mentor-guidance.md`](../../docs/superpowers/mentor-guidance.md). In particular:

- Apply the taste-probe before aesthetic harmonic decisions (e.g., "do you want this dark or bright?") — not for craft issues (e.g., "that chord clashes with the bass").
- Recall relevant memory before running (habits related to harmony, voicing, progression).
- Include woven teaching in the written reasoning — concrete, verifiable, tied to the work in front of the user. No generic wisdom.
- Declare observations aloud after running (e.g., "you're overcrowding the low-mid with the voicing again" — mentor voice, not database voice).
- Track escape-hatch use if the user invokes with `just-give-it-to-me`.

## Workflow

### 1. Pre-phase

1. Recall memory observations for domains `["harmony"]`.
2. Surface relevant memory to the user. Example: "Last time your voicings were crowding the low-mid — keeping the spacing open today, or piling in again?"
3. If the decision is aesthetic (tonal center dark vs. bright, modal vs. diatonic, static vs. moving) and the user hasn't voiced a preference recently, apply the taste-probe: "Before I weigh in — do you want this dark or bright?"

### 2. Understand the request

Determine:
- The genre (consult `knowledge/genres/` for the relevant profile — its `harmonic_conventions` are the primary input for harmony).
- The tonal center (key, mode).
- The phrase length (consult `knowledge/theory/phrase-and-form.md`).
- The user's goal: generate a new progression, fix an existing one, or critique.

Consult the relevant theory documents:
- `knowledge/theory/diatonic-harmony.md` — for diatonic progressions.
- `knowledge/theory/chromatic-harmony.md` — for borrowed chords, secondary dominants, modulation.
- `knowledge/theory/static-harmony.md` — for pedal points and two-chord loops.
- `knowledge/theory/bass-as-harmony.md` — for when bass carries the harmony.
- `knowledge/theory/tension-and-release.md` — for harmonic tension/release.

### 3. Generate or critique

**To generate chords:**

Use `MidWriter.write_chords` to write a `.mid` file. The chords are a list of chord specs (each chord is a list of MIDI note numbers):
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

Reason about:
- **Progression logic**: what chords, in what order, and why. Consult the theory documents for the principles.
- **Voicing**: how the chord is voiced (open vs. closed, which inversion, where in the register). Voicing is critical in electronic music — consult `knowledge/theory/voice-leading.md` for spacing principles (avoid low-mid overcrowding).
- **Tension/release**: where the progression creates and releases tension. Consult `knowledge/theory/tension-and-release.md`.
- **Genre harmonic conventions**: how much harmony, what kind. Dub techno: static. House: diatonic stabs. Techno: often none or bass-as-harmony.
- **Harmonic rhythm**: how fast the chords change. Consult `knowledge/theory/phrase-and-form.md`.

**To critique a progression** (the user provides MIDI or describes it):

Assess:
- Progression logic: does it work, and is it genre-appropriate?
- Voicing: is the spacing good, or is the low-mid overcrowded?
- Tension/release: is there direction, or does it sit flat?
- Genre fit: does the harmony match the genre's conventions?

### 4. Written reasoning output

Produce written reasoning alongside the `.mid` file or notation. The reasoning must:
- Explain the progression logic, voicing choices, tension/release, and genre conventions in play.
- Include woven teaching — concrete, checkable, tied to this progression. Example: "The voicing puts the third in the middle register because the bass is carrying the root — that's why the chord feels complete without being muddy." Not: "Voicing matters."
- State opinions as the mentor's take with reasoning. Yield if the user overrides.

### 5. Post-phase

1. Declare any observations aloud (mentor voice). If the voicing overcrowds the low-mid the same way as a previous session, say so: "You're piling the third in the low-mid again." Update memory via `MemoryStore.declare(...)`.
2. If the user invoked with `just-give-it-to-me`, record a tool-path invocation via `EscapeHatchTracker.record("tool")`. Otherwise record a mentor-path invocation.
3. Check for lesson escalation: if a harmony concept has recurred across >=3 sessions, produce a standalone lesson artifact.

## Output contract

- A `.mid` file or roman-numeral/ABC notation (if generating) at the requested path.
- Written reasoning: progression logic, voicing choices, tension/release, genre conventions, with woven teaching.
- Declared observations (spoken aloud, written to memory).
- Optional: a lesson artifact if escalation is triggered.