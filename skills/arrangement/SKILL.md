# Skill: arrangement

## When to invoke

Invoke when the user wants to plan, critique, or restructure the section structure, energy arc, or transitions of a track. Also invoke for "Help me structure this track", "the arrangement feels flat", "how do I transition from the build to the drop?".

Do not invoke for generating parts — `arrangement` calls other domain skills for content. `arrangement` owns the *shape* of the track and the *role* of each section. `critique` and `diagnose` consult arrangement knowledge independently. `arrangement` does not own domain expertise — it delegates to domain skills (`bass`, `melody`, `rhythm`, `harmony`, `sound-design`).

## Shared guidance

Follow the shared mentor voice, guards, and post-phase behaviors defined in [`../../docs/superpowers/mentor-guidance.md`](../../docs/superpowers/mentor-guidance.md). In particular:

- Apply the taste-probe before aesthetic decisions about arrangement direction (e.g., "do you want this to build slowly or hit hard early?") — arrangement is highly aesthetic.
- Recall relevant memory before running (habits related to arrangement, energy arc, transitions).
- Include woven teaching in the written reasoning — concrete, verifiable, tied to the work in front of the user. No generic wisdom.
- Declare observations aloud after running (e.g., "you're cutting your builds short again" — mentor voice, not database voice).
- Track escape-hatch use if the user invokes with `just-give-it-to-me`.

## Workflow

### 1. Pre-phase

1. Recall memory observations for domains `["arrangement"]`.
2. Surface relevant memory to the user. Example: "Last time your tracks were front-loaded — all energy in the first drop. Bringing that today, or building a longer arc this time?"
3. If the decision is aesthetic (overall arc shape, pacing, build/release choices) and the user hasn't voiced a preference recently, apply the taste-probe: "Before I weigh in — do you want this to build slowly or hit hard early?"

### 2. Understand the request

Determine:
- The genre (consult `knowledge/genres/` for the relevant profile — its `arrangement_conventions` are the primary input for arrangement).
- The current state of the track (if the user has one — sections that exist, energy so far, where it stalls).
- The user's goal: plan an arrangement from scratch, critique an existing one, or fix a specific transition.

### 3. Generate or critique

**To generate an arrangement plan:**

`arrangement` does not produce MIDI directly. It produces a written arrangement plan, then references artifacts from other skills (`bass`, `melody`, `rhythm`, `harmony`, `sound-design`) for the actual content. Reason about:

- **Section list**: what sections (intro, build, drop, breakdown, outro) and in what order. Consult the genre profile's `arrangement_conventions`.
- **Energy arc**: how energy builds and releases across the track. Consult `knowledge/theory/tension-and-release.md`.
- **Section roles**: what each section does (intro sets the mood, build creates tension, drop releases it, breakdown provides contrast). State each role explicitly.
- **Transitions**: how to move between sections (filter sweeps, layer addition/removal, rhythmic shifts). Consult `knowledge/theory/phrase-and-form.md` for phrase length.
- **Layer management**: what enters/exits when. Arrangement in electronic music is often additive/subtractive — which elements come in and leave at each section boundary matters as much as the sections themselves.
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

For each section, note which domain skill produces its content (e.g., "Drop calls `bass` for the sub, `rhythm` for the percussion, `harmony` for the stabs, `sound-design` for the pad texture").

**To critique an arrangement** (the user describes it or provides a section list):

Assess:
- Section structure (does it flow? are sections in the right order?).
- Energy arc (does it build and release effectively, or sit flat?).
- Transitions (are they smooth or jarring? do they serve the genre?).
- Section roles (is each section doing its job — does the intro set the mood, does the build actually build?).
- Phrase length (are phrases consistent — 4/8/16 — or ragged?).
- Genre fit (does the arrangement match the genre's `arrangement_conventions`?).

### 4. Written reasoning output

Produce written reasoning alongside the arrangement plan. The reasoning must:
- Explain the section structure, energy arc, transitions, and layer management choices.
- Include woven teaching — concrete, checkable, tied to this arrangement. Example: "The build is 16 bars because that's four 4-bar phrases — the listener expects a change at 16, so the drop lands on the expected bar. Cutting the build to 8 bars would feel rushed." Not: "Builds should be the right length."
- State opinions as the mentor's take with reasoning. Yield if the user overrides.

### 5. Post-phase

1. Declare any observations aloud (mentor voice). If the arrangement falls into a recurring pattern from previous sessions, say so: "You're front-loading the energy again." Update memory via `MemoryStore.declare(...)`.
2. If the user invoked with `just-give-it-to-me`, record a tool-path invocation via `EscapeHatchTracker.record("tool")`. Otherwise record a mentor-path invocation.
3. Check for lesson escalation: if an arrangement concept has recurred across >=3 sessions, produce a standalone lesson artifact.

## Output contract

- A written arrangement plan: section list with roles, energy curve, transition notes, layer management.
- No MIDI directly (but references artifacts from other skills for content).
- Written reasoning with woven teaching.
- Declared observations (spoken aloud, written to memory).
- Optional: a lesson artifact if escalation is triggered.