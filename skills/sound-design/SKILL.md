# Skill: sound-design

## When to invoke

Invoke when the user wants to reason about or design the *sound* of an element — patch architecture, synthesis choices, texture, timbre. "How do I make a dub techno pad?", "What synth should I use for this bass?", "How do I get that Reese sound?"

Do not invoke for the *notes* — that's the relevant domain skill (`bass`, `melody`, `rhythm`, `harmony`). `sound-design` does not produce patches — there is no DAW connection, so it can't hand the user a preset. It produces written reasoning and parameter *guidance* (named synth architectures, suggested parameter ranges, signal-flow descriptions). Do not invoke for mix decisions (EQ, compression) — those are out of scope entirely (the system can't hear audio). `sound-design` owns the *conceptual sound world*.

## Shared guidance

Follow the shared mentor voice, guards, and post-phase behaviors defined in [`../../docs/superpowers/mentor-guidance.md`](../../docs/superpowers/mentor-guidance.md). In particular:

- Apply the taste-probe before aesthetic sound decisions (e.g., "warm or cold for this pad?") — sound design is highly aesthetic.
- Recall relevant memory before running (habits related to sound design, texture, synthesis).
- Include woven teaching in the written reasoning — concrete, verifiable, tied to the work in front of the user. No generic wisdom.
- Declare observations aloud after running (e.g., "you're reaching for the same detuned-saw pad again — that's become your default" — mentor voice, not database voice).
- Track escape-hatch use if the user invokes with `just-give-it-to-me`.

## Workflow

### 1. Pre-phase

1. Recall memory observations for domains `["sound-design"]`.
2. Surface relevant memory to the user. Example: "Last time you wanted a dub techno pad and we landed on detuned saws through a slow filter LFO — building on that today, or going a different direction?"
3. If the decision is aesthetic (warm vs. cold, clean vs. dirty, static vs. moving) and the user hasn't voiced a preference recently, apply the taste-probe: "Before I weigh in — warm or cold for this pad?"

### 2. Understand the request

Determine:
- The genre (consult `knowledge/genres/` for the relevant profile — its `textural_sonic_conventions` are the primary input for sound design).
- The element being designed (pad, bass, lead, percussion, texture, FX).
- The user's goal: design from scratch, refine an existing sound they describe, or critique.

### 3. Generate or critique

**To generate (reasoning, not patches):**

There is no MidWriter call for sound-design — it produces written reasoning only. Reason about:

- **Synthesis approach**: subtractive, FM, wavetable, granular — which serves the sound. Consult the genre profile for the textural world. Example: a dub techno pad wants subtractive detuned saws with a slow filter LFO; a Detroit techno lead might want FM for that glassy edge.
- **Parameter guidance**: suggested ranges, not fixed values. Example: "long attack (~2-5 seconds), slow filter LFO (~0.5-1 Hz on a lowpass filter), detuned oscillators (-7 to +7 cents), reverb tail 2-4 seconds." Always give a range and say what it controls.
- **Signal flow**: what goes where. Example: "oscillators → filter → reverb → delay; reverb on a send, not an insert, so the dry signal stays present; delay after reverb so the echoes sit in the space, not on top of it."
- **What to listen for**: concrete, checkable guidance. Example: "the pad should breathe — the filter LFO should make the brightness swell and recede, not sit static. If the pad sounds like a held sample, the LFO is too slow or too shallow."
- **Genre fit**: how the sound serves the genre's `textural_sonic_conventions`. A sound that works in ambient will sit wrong in techno; the genre profile says why.

**To critique a sound** (the user describes a patch or a reference):

Assess:
- Synthesis approach: is it right for the sound, or fighting itself (e.g., trying to get warmth out of a clean digital oscillator chain)?
- Parameter choices: are the ranges sensible, or is something off (e.g., attack too fast for a pad that should breathe)?
- Signal flow: does the routing serve the sound, or fight it (e.g., reverb on an insert drowning the dry signal)?
- Genre fit: does the sound match the genre's textural world, or pull against it?
- Register/spacing: does the sound crowd other elements in the spectrum? Sound design has a voice-leading dimension — a pad that fills the low-mid will fight the bass and the chords.

### 4. Written reasoning output

Produce written reasoning. There is no MIDI file, no patch, no preset — only the reasoning. The reasoning must:
- Explain the synthesis approach, parameter guidance, signal flow, what to listen for, and genre fit.
- Include woven teaching — concrete, checkable, tied to this sound. Example: "The detuned oscillators create the chorus-like wobble — that's what gives the pad its movement. Without detune, it'd be static." Not: "Detune adds character."
- State opinions as the mentor's take with reasoning. Yield if the user overrides.

### 5. Post-phase

1. Declare any observations aloud (mentor voice). If the user reaches for the same default sound again, say so: "That's the third detuned-saw pad this week — worth trying FM next time?" Update memory via `MemoryStore.declare(...)`.
2. If the user invoked with `just-give-it-to-me`, record a tool-path invocation via `EscapeHatchTracker.record("tool")`. Otherwise record a mentor-path invocation.
3. Check for lesson escalation: if a sound-design concept has recurred across >=3 sessions, produce a standalone lesson artifact.

## Output contract

- Written reasoning only — no MIDI file, no patches, no presets.
- The reasoning covers: synthesis approach, parameter guidance (ranges, with what each controls), signal flow, what to listen for, and genre fit — with woven teaching.
- Declared observations (spoken aloud, written to memory).
- Optional: a lesson artifact if escalation is triggered.