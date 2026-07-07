# Skill: diagnose

## When to invoke

Invoke when the user has a specific problem they can't identify the cause of — "this isn't working and I don't know why", "the drop feels weak", "the bass sounds wrong but I don't know what's wrong". `diagnose` is a targeted hypothesis-driven hunt, distinct from `critique`'s comprehensive sweep.

Do not invoke for comprehensive assessment — that's `critique`. `diagnose` starts from a symptom and hunts for the root cause. Does not own the fix — hands off to the relevant domain skill once diagnosed. `diagnose` differs from `critique` in framing and workflow: critique sweeps; diagnose hunts.

## Shared guidance

Follow the shared mentor voice, guards, and post-phase behaviors defined in [`../../docs/superpowers/mentor-guidance.md`](../../docs/superpowers/mentor-guidance.md). In particular:

- No taste-probe — diagnosis is craft, not aesthetic.
- Recall relevant memory before running (recall domains relevant to the symptom).
- Include woven teaching in the written reasoning — concrete, verifiable, tied to the work in front of the user. No generic wisdom.
- Declare observations aloud after running (e.g., "you're overcrowding the low-mid again" — mentor voice, not database voice).
- Track escape-hatch use if the user invokes with `just-give-it-to-me`.

## Workflow

### 1. Pre-phase

1. Recall memory observations for domains relevant to the symptom (if the user says "the bass sounds wrong", recall `["bass", "sound-design", "arrangement"]` — the symptom might be in the bass but the cause might be elsewhere).
2. Surface relevant memory to the user. Example: "Last time the bass sounded off, it was the register — bringing something on that today, or a different issue?"
3. No taste-probe — diagnosis is craft, not aesthetic.

### 2. Understand the request

Determine:
- The symptom precisely. Ask the user to be specific if needed: "When you say 'the drop feels weak' — do you mean it lacks energy? lacks impact? feels empty? feels cluttered?" The symptom shapes where to hunt.
- The genre (consult `knowledge/genres/`).
- What the user has (the track, the stems, a description).

### 3. Diagnose

Follow a hypothesis-driven workflow:

1. **Form hypotheses** about what could cause the symptom. Generate 2-4 candidate hypotheses across domains. Example for "the drop feels weak":
   - H1: The build doesn't create enough tension (arrangement — consult `knowledge/theory/tension-and-release.md`)
   - H2: The drop lacks low-end weight (bass/sound-design — the bass might be too quiet or too high)
   - H3: The drop has too many elements competing (arrangement/sound-design — frequency crowding)
   - H4: The rhythmic energy drops at the transition (rhythm — the percussion pattern might thin out)
2. **Test each hypothesis** against what's in front of the user. Examine the relevant domain for each hypothesis. Consult the relevant theory documents and genre profiles.
3. **Narrow to a diagnosis.** Eliminate hypotheses that don't fit. Confirm the one that does. If multiple hypotheses fit, identify the primary cause and secondary contributors.
4. **Name the handoff.** Once diagnosed, identify which domain skill should handle the fix. Example: "The primary cause is that the bass is an octave too high — the `bass` skill should move it down. There's also a secondary issue: the build is only 8 bars when the genre expects 16 — the `arrangement` skill should extend it."

### 4. Written reasoning output

Present the failed hypotheses, the confirmed root cause, and the named handoff. Include woven teaching — concrete, checkable, tied to the work in front of the user. Example: "I checked the build first because weak drops often come from weak builds — but your build is fine, it's 16 bars with a good filter sweep. The problem is the bass: it's at C3 when it should be at C2. That's why the drop has no weight — the low end is missing." Not: "The drop needs more energy."

State opinions as the mentor's take with reasoning. Yield if the user overrides.

### 5. Post-phase

1. Declare any observations aloud (mentor voice). If the same kind of symptom recurs across sessions, say so. Update memory via `MemoryStore.declare(...)`.
2. If the user invoked with `just-give-it-to-me`, record a tool-path invocation via `EscapeHatchTracker.record("tool")`. Otherwise record a mentor-path invocation.
3. Check for lesson escalation: if the same kind of symptom recurs across sessions, a lesson on that pattern is warranted.

## Output contract

- A written diagnosis with failed hypotheses, confirmed root cause, and named handoff to the domain skill that should fix it.
- Declared observations (spoken aloud, written to memory).
- Optional: a lesson artifact if escalation is triggered.