# Skill: develop-track

## When to invoke

Invoke when the user wants to construct a whole track — "help me build this track", "I want to make a dub techno track from scratch", "let's develop this project". `develop-track` is the orchestrator that coordinates across domains to build a complete track.

Do not invoke for single-element work — that's the relevant domain skill. `develop-track` does not own domain expertise — it delegates to `arrangement` for shape, then to `bass`/`melody`/`rhythm`/`harmony`/`sound-design` for content, then to `critique` for cross-domain coherence. `develop-track` owns the *process* of construction and the *coherence* of the result. This is a skill that calls other skills — it is distinct from the Mentor Orchestrator (the relationship layer), which wraps all skill invocations including this one.

## Shared guidance

Follow the shared mentor voice, guards, and post-phase behaviors defined in [`../../docs/superpowers/mentor-guidance.md`](../../docs/superpowers/mentor-guidance.md). In particular:

- Apply the taste-probe before aesthetic decisions — develop-track is highly aesthetic, so the taste-probe is essential.
- Recall relevant memory before running (develop-track is cross-domain, so recall everything relevant).
- Include woven teaching in the written reasoning — concrete, verifiable, tied to the work in front of the user. No generic wisdom.
- Declare observations aloud after running (e.g., "you're overcrowding the low-mid again" — mentor voice, not database voice).
- Track escape-hatch use if the user invokes with `just-give-it-to-me`.

## Workflow

### 1. Pre-phase

1. Recall memory observations for domains `["arrangement", "bass", "melody", "rhythm", "harmony", "sound-design"]` — develop-track is cross-domain, so recall everything relevant.
2. Surface relevant memory to the user. Example: "Last time we built a track together you overcrowded the low-mid — bringing something on that today, or starting fresh?"
3. Apply the taste-probe: "Before we start building — what's the vision for this track? What genre? What mood?" Develop-track is highly aesthetic, so the taste-probe is essential.

### 2. Understand the request

Determine:
- The genre (consult `knowledge/genres/` — the genre profile is the primary input for the whole track).
- The user's vision (mood, energy, length, purpose).
- What the user already has (nothing? a sketch? some elements?).

### 3. Develop-track

Follow a construction process:

1. **Call `arrangement`** for the track shape. Get an arrangement plan (section list, energy arc, transitions). Consult the genre profile's `arrangement_conventions`.
2. **For each section, call the relevant domain skills for content:**
   - `rhythm` for the percussion pattern (consult the genre's `rhythmic_conventions`)
   - `bass` for the bassline (consult the genre's `harmonic_conventions` and `knowledge/theory/bass-as-harmony.md`)
   - `harmony` for chords if the genre uses them (consult the genre's `harmonic_conventions`)
   - `melody` for leads if the genre uses them
   - `sound-design` for the textural world (consult the genre's `textural_sonic_conventions`)
3. **Coordinate across domains** — ensure the parts work together:
   - Bass and kick share the low end (bass register vs. kick frequency)
   - Chord stabs and bass don't crowd the low-mid (consult `knowledge/theory/voice-leading.md`)
   - Melody sits in a register that doesn't clash with chords
   - Rhythmic placement of all elements is coherent
4. **Call `critique`** for cross-domain coherence once the parts are in place. Fix any issues the critique identifies (by handing back to the relevant domain skill).
5. **Iterate** — the user may want to revise sections, swap elements, or adjust the arrangement. Each revision goes through the relevant domain skill.

### 4. Written reasoning output

Produce written reasoning alongside the construction. The reasoning must:
- Explain the construction process: the arrangement plan, why each part was chosen, how the parts relate, what the genre conventions are doing.
- Include woven teaching — concrete, checkable, tied to this track. Example: "The bass is on C while the chord stab is Cm above it — that's bass-as-harmony, the dub techno approach. The stab adds the minor third color; the bass carries the root identity." Not: "The bass and chords work together."
- State opinions as the mentor's take with reasoning. Yield if the user overrides.

### 5. Post-phase

1. Declare any observations aloud (mentor voice). Develop-track is likely to surface multiple observations across domains. Update memory via `MemoryStore.declare(...)`.
2. If the user invoked with `just-give-it-to-me`, record a tool-path invocation via `EscapeHatchTracker.record("tool")`. Otherwise record a mentor-path invocation.
3. Check for lesson escalation: if a concept recurred during the construction, produce a standalone lesson artifact.

## Output contract

- A track construction plan + coordinated artifacts (MIDI files per part, arrangement plan, written reasoning linking them).
- Written reasoning: the construction process, why each part was chosen, how the parts relate, with woven teaching.
- Declared observations (spoken aloud, written to memory).
- Optional: a lesson artifact if escalation is triggered.