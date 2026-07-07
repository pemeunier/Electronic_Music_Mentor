# Skill: critique

## When to invoke

Invoke when the user wants a comprehensive cross-domain assessment — "tell me what's wrong", "what's working", "review this track". `critique` sweeps across all domains (bass, melody, rhythm, harmony, sound-design, arrangement) and identifies issues and strengths.

Do not invoke for domain-specific deep fixes — when `critique` identifies a bass problem, it can hand off to `bass` for the fix. `critique` owns the *cross-domain assessment*, not the deep fixes. Do not invoke for targeted troubleshooting ("this specific thing isn't working") — that's `diagnose`. `critique` is a sweep; `diagnose` is a hunt.

## Shared guidance

Follow the shared mentor voice, guards, and post-phase behaviors defined in [`../../docs/superpowers/mentor-guidance.md`](../../docs/superpowers/mentor-guidance.md). In particular:

- Apply the taste-probe before aesthetic direction (e.g., "before I tell you what I'd change — what are you going for with this track?").
- Recall relevant memory before running (critique is cross-domain, so recall everything relevant).
- Include woven teaching in the written reasoning — concrete, verifiable, tied to the work in front of the user. No generic wisdom.
- Declare observations aloud after running (e.g., "you're overcrowding the low-mid the same way you did last time" — mentor voice, not database voice).
- Track escape-hatch use if the user invokes with `just-give-it-to-me`.

## Workflow

### 1. Pre-phase

1. Recall memory observations for domains `["bass", "melody", "rhythm", "harmony", "sound-design", "arrangement"]` — critique is cross-domain, so recall everything relevant.
2. Surface relevant memory to the user. Example: "Last time you were overcrowding the low-mid — bringing something on that today, or starting fresh?"
3. If the critique will involve aesthetic direction and the user hasn't voiced a preference recently, apply the taste-probe: "Before I weigh in — what are you going for with this track?"

### 2. Understand the request

Determine:
- The genre (consult `knowledge/genres/` — the genre's `common_failure_modes` are a key input for critique).
- What the user has (a full track? a sketch? a stem?).
- What they want (full critique? focus on a specific area?).

### 3. Critique

Assess across all domains:

- **Bass**: register, rhythmic relationship to kick, harmonic role clarity, voice-leading. Consult the `bass` skill's critique criteria.
- **Melody**: motif strength, repetition/variation, contour, rhythmic placement, harmonic relationship. Consult the `melody` skill's critique criteria.
- **Rhythm**: groove feel, velocity patterns, layer roles, density. Consult the `rhythm` skill's critique criteria.
- **Harmony**: progression logic, voicing, tension/release, genre fit. Consult the `harmony` skill's critique criteria.
- **Sound-design**: synthesis approach, parameter choices, signal flow, genre fit, register/spacing. Consult the `sound-design` skill's critique criteria.
- **Arrangement**: section structure, energy arc, transitions, section roles, phrase length. Consult the `arrangement` skill's critique criteria.
- **Cross-domain issues**: frequency-space reasoning ("the low-mid is crowded — bass and pad are fighting"), coherence across domains (does the bass serve the harmony? does the rhythm serve the groove?).

Consult the genre profile's `common_failure_modes` — these are the lazy-execution patterns to check for.

Produce a written critique organized by domain, with severity/priority for each issue, and named handoffs where a domain skill should take over for the fix.

### 4. Written reasoning output

The critique itself is the reasoning. Organize by domain, lead with the most important issues. Include woven teaching — concrete, checkable, tied to the work in front of the user. Example: "The bass and kick are both hitting at 80Hz on every beat — that's why the low end is muddy. The fix is either to move the bass up an octave or sidechain the bass to the kick." Not: "The low end needs work."

State opinions as the mentor's take with reasoning. Yield if the user overrides.

### 5. Post-phase

1. Declare any observations aloud (mentor voice). If a cross-domain issue recurs the same way as a previous session, say so: "You're overcrowding the low-mid the same way you did last time." Update memory via `MemoryStore.declare(...)`.
2. If the user invoked with `just-give-it-to-me`, record a tool-path invocation via `EscapeHatchTracker.record("tool")`. Otherwise record a mentor-path invocation. (Critique is rarely tool-path — it's inherently mentor-path.)
3. Check for lesson escalation: if a concept has recurred across >=3 sessions, produce a standalone lesson artifact.

## Output contract

- A written critique organized by domain, with severity/priority and named handoffs to domain skills.
- Declared observations (spoken aloud, written to memory).
- Optional: a lesson artifact if escalation is triggered.