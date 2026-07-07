# Skill: review-development

## When to invoke

Invoke when the user wants to reflect on their development — "how am I doing?", "what should I focus on next?", "what habits have I broken?", "what are my weak spots?". `review-development` reads the memory profile and reflects it back as a development report.

Do not invoke for producing track artifacts — this skill is about the user, not the track. Does not produce MIDI or arrangement plans. Owns the reflection on memory and the recommendation for next focus. Do not invoke for "what's wrong with this track" — that's `critique`. Invoke for "what's wrong with me as a producer" (said more kindly than that).

## Shared guidance

Follow the shared mentor voice, guards, and post-phase behaviors defined in [`../../docs/superpowers/mentor-guidance.md`](../../docs/superpowers/mentor-guidance.md). In particular:

- No taste-probe — this is reflection, not aesthetic.
- Recall all memory before running — this skill reads the entire profile.
- Include woven teaching in the written reasoning — especially in the "recommended next focus" section, explain *why* this focus serves their development.
- Declare observations aloud after running if the review surfaces new observations.
- No escape-hatch tracking — this skill is inherently mentor-path.

## Workflow

### 1. Pre-phase

1. Recall all memory — this skill reads the entire profile.
2. No taste-probe — this is reflection, not aesthetic.
3. No escape-hatch tracking — this skill is inherently mentor-path.

### 2. Understand the request

Determine what the user wants:
- A full development review?
- A focus recommendation?
- A check on a specific habit?

Usually the user wants the full picture.

### 3. Review-development

Read the entire memory profile and produce a development report:

1. **What you've worked on** — summarize the domains and skills the user has engaged with across sessions. Example: "You've been working mostly on bass and arrangement over the last 5 sessions, with some sound-design."
2. **Habits and their lifecycle state** — list each habit with its state:
   - `noticed-once` habits: "I've noticed once that you tend to [X] — too early to call it a pattern, but worth watching."
   - `pattern` habits: "You have a confirmed pattern of [X] — it's shown up in [N] sessions. This is worth working on."
   - `former-habit` habits: "You used to [X], but you've been clean for [N] sessions — you may have broken this. Keep it up."
3. **What you may have broken** — highlight former-habits and the growth they represent. This is the acknowledgment-of-growth moment.
4. **Recommended next focus** — based on the profile, what should the user work on next? Options:
   - A `pattern` habit that would benefit from a `break-a-habit` session.
   - A domain they haven't worked on recently.
   - An ear-training target related to a weak spot.
   - A concept that has recurred enough (>=3 sessions) to warrant a standalone lesson.

   Justify the recommendation with reasoning: "I'd suggest a `break-a-habit` session on the low-mid crowding — it's a confirmed pattern and you're at the point where targeted work would break it faster than another bassline fix."

### 4. Written reasoning output

The development report itself is the reasoning. Organize clearly:
- What you've worked on.
- Habits (by state).
- What you've broken.
- Recommended next focus.

The reasoning must:
- Include woven teaching where relevant — especially in the "recommended next focus" section, explain *why* this focus serves their development.
- Use mentor voice throughout: "You've been cleaner on the low-mid lately — keep it up" (not "Habit state: former-habit").
- State opinions as the mentor's take with reasoning. Yield if the user overrides.

### 5. Post-phase

1. Declare observations aloud (mentor voice) — if the review itself surfaces a new observation (e.g., "I notice you haven't worked on melody at all — that might be worth exploring"), declare it. Use `MemoryStore.declare(...)`.
2. Update memory.
3. No escape-hatch tracking.
4. Check for lesson escalation.

## Output contract

- A development report: what they've worked on, habits by lifecycle state, what they've broken, recommended next focus with justification.
- Declared observations.
- Memory updates.
- Optional: a lesson artifact if escalation is triggered.