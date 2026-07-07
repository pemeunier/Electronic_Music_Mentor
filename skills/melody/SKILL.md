# Skill: melody

## When to invoke

Invoke when the user wants to write, generate, or critique a melody, lead, motif, or top-line for an electronic music track. Also invoke for motif construction, repetition/variation, and contour.

Do not invoke for the chords the melody implies — that's `harmony`. The melodic line and its internal logic are `melody`'s domain. Do not invoke for bass lines — that's `bass`. Do not invoke for rhythm of non-melodic elements — that's `rhythm`. Do not invoke for the sound of the lead (synth patch) — that's `sound-design`. `melody` owns the melodic *notes*, *contour*, and *motif logic*.

## Shared guidance

Follow the shared mentor voice, guards, and post-phase behaviors defined in [`../../docs/superpowers/mentor-guidance.md`](../../docs/superpowers/mentor-guidance.md). In particular:

- Apply the taste-probe before aesthetic decisions (melody direction, mood, contour) — melody is highly aesthetic, so taste-probe is particularly important here. Not for craft issues (e.g., a clashing note).
- Recall relevant memory before running (habits related to melody, motif, top-line).
- Include woven teaching in the written reasoning — concrete, verifiable, tied to the work in front of the user. No generic wisdom.
- Declare observations aloud after running (e.g., "you're landing on the downbeat every phrase — try a suspension" — mentor voice, not database voice).
- Track escape-hatch use if the user invokes with `just-give-it-to-me`.

## Workflow

### 1. Pre-phase

1. Recall memory observations for domains `["melody"]`.
2. Surface relevant memory to the user. Example: "Last time your top-line stayed in a narrow range and felt static — reaching higher today, or working that range again?"
3. If the decision is aesthetic (melody direction, mood, contour) and the user hasn't voiced a preference recently, apply the taste-probe: "Before I weigh in — what direction are you hearing for the melody?"

### 2. Understand the request

Determine:
- The genre (consult `knowledge/genres/` — its harmonic conventions shape what melodic notes fit).
- The harmonic context (if chords are known, consult `knowledge/theory/voice-leading.md` and `knowledge/theory/diatonic-harmony.md` for scale tones and tension notes; consult the `harmony` skill if a progression is needed).
- The phrase length (consult `knowledge/theory/phrase-and-form.md`).
- The user's goal: generate a new melody, fix an existing one, or critique.

### 3. Generate or critique

**To generate a melody:**

Use the `MidWriter` to write a `.mid` file. `MidWriter.write_bassline` works for any monophonic line — the method name is "bassline" but it writes any single-note MIDI line; set `program` to a lead instrument like 80 or 81 for synth lead.
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

Reason about:
- **Motif construction**: the smallest melodic idea — consult `knowledge/theory/phrase-and-form.md` for motif principles. A good motif is memorable and developable.
- **Repetition and variation**: repeat the motif, vary it (change one thing, keep the rest). Consult `knowledge/theory/phrase-and-form.md`.
- **Contour**: the shape of the melody — rising, falling, arch. Genre informs contour (house melodies often repetitive and cyclical; techno melodies often minimal and static; IDM melodies often jagged and unpredictable).
- **Rhythmic placement**: where the melody sits relative to the groove. Consult the genre profile's `rhythmic_conventions`.
- **Harmonic relationship**: which scale tones the melody uses, where tension notes are placed (consult `knowledge/theory/tension-and-release.md`).

**To critique a melody** (the user provides MIDI or describes it):

Assess:
- Motif strength (is it memorable?).
- Repetition/variation balance (too repetitive? too varied?).
- Contour appropriateness for the genre.
- Rhythmic placement.
- Harmonic relationship (are tension notes used effectively?).

### 4. Written reasoning output

Produce written reasoning alongside the `.mid` file. The reasoning must:
- Explain the motif logic, contour, rhythmic placement, and relationship to the chords.
- Include woven teaching — concrete, checkable, tied to this melody. Example: "The melody lands on the third of the chord on beat 1 — that's why it feels resolved. If it landed on the ninth, it would float more." Not: "Melodies should be memorable."
- State opinions as the mentor's take with reasoning. Yield if the user overrides.

### 5. Post-phase

1. Declare any observations aloud (mentor voice). If the melody repeats a habit seen in a previous session (e.g., always starting on the downbeat, never using tension notes), say so. Update memory via `MemoryStore.declare(...)`.
2. If the user invoked with `just-give-it-to-me`, record a tool-path invocation via `EscapeHatchTracker.record("tool")`. Otherwise record a mentor-path invocation.
3. Check for lesson escalation: if a melody concept has recurred across >=3 sessions, produce a standalone lesson artifact.

## Output contract

- A `.mid` file (if generating) at the requested path.
- Written reasoning: motif logic, contour, rhythmic placement, relationship to chords, with woven teaching.
- Declared observations (spoken aloud, written to memory).
- Optional: a lesson artifact if escalation is triggered.