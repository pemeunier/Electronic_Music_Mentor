# Skill: ear-train

## When to invoke

Invoke when the user wants to deliberately train their ear — "teach me to hear X", "I can't tell what's wrong with my low end", "help me recognize when a chord progression is good". `ear-train` is the most direct expression of the core experience goal: building transferable ear/judgment.

Do not invoke for quick answers — that's the relevant domain skill. `ear-train` has a workflow: identify what to train, give exercises, check back next session. It's deliberate practice, not a one-off explanation. Do not invoke for "what's wrong with this bass" — that's `bass` or `critique`. Invoke for "I want to learn to hear when the bass is wrong".

## Shared guidance

Follow the shared mentor voice, guards, and post-phase behaviors defined in [`../../docs/superpowers/mentor-guidance.md`](../../docs/superpowers/mentor-guidance.md). In particular:

- Recall relevant memory before running — especially previous ear-training check-backs.
- Include woven teaching in the written reasoning — concrete, verifiable, tied to the work in front of the user. This is the skill where woven teaching is most at home.
- Declare observations aloud after running (e.g., "you're still missing the low-mid crowding when the bass is high" — mentor voice, not database voice).
- No taste-probe — ear-training is craft development, not aesthetic direction.

## Workflow

### 1. Pre-phase

1. Recall memory observations for domains relevant to what the user wants to train. If unsure, recall broadly.
2. Surface relevant memory — especially previous ear-training check-backs. Example: "Last time you were working on hearing low-mid crowding — did you practice?"
3. No taste-probe — ear-training is craft development, not aesthetic direction.

### 2. Understand the request

Determine what the user wants to train their ear for. Common ear-training targets:

- Low-end clarity (hearing when bass and kick clash)
- Low-mid crowding (hearing when too many elements occupy the low-mid)
- Harmonic recognition (hearing what chord is playing, what the progression is)
- Groove feel (hearing swing, pocket, velocity patterns)
- Tension and release (hearing when harmony creates tension, when it releases)
- Texture and filter movement (hearing when a filter opens/closes, when texture evolves)

Determine:

- The user's current level (ask if not clear).
- The genre context (consult `knowledge/genres/` — ear-training is more effective in a genre context the user knows).

### 3. Ear-train

1. **Identify what to train** — narrow the target to something specific and trainable. "Hearing low-mid crowding" is good; "hearing better" is not.

2. **Give exercises** — provide concrete listening exercises:

   - **Reference listening**: point the user to the genre profile and ask them to listen to tracks in that genre, focusing on the specific thing. Example: "Listen to three dub techno tracks and focus on the low-mid. Notice how in good examples, the bass and pad don't overlap — the bass is low, the pad is higher. In lazy examples, they crowd each other."
   - **Self-assessment**: ask the user to apply the listening to their own work. Example: "Now listen to your own track's low-mid. Is the bass and pad relationship more like the good examples or the lazy ones?"
   - **A/B comparison**: if the user has a reference and their own work, compare them.

3. **Set the check-back** — store a check-back note in memory for the next session. Example: "User is training low-mid crowding recognition. Check back next session: ask them to identify whether their current low-mid is crowded, without prompting."

   Store the check-back via `MemoryStore.declare(...)` with a special domain tag like `["ear-train"]` and content describing the exercise and what to check.

### 4. Written reasoning output

Produce written reasoning. The reasoning must:

- Explain what to train, why it matters, the exercises, and what to listen for.
- Include woven teaching — concrete, checkable, tied to this target. Example: "When you listen for low-mid crowding, focus on the 200-500Hz range. If the bass and a pad are both in that range, you'll hear a 'boxy' or 'muddy' quality. In good dub techno, the bass stays below 200Hz and the pad sits above 500Hz — there's a gap." Not: "Listen carefully to the low-mid."
- State opinions as the mentor's take with reasoning. Yield if the user overrides.

### 5. Post-phase

1. Declare any observations aloud (mentor voice). Update memory via `MemoryStore.declare(...)` — especially the check-back note.
2. If the user invoked with `just-give-it-to-me`, record a tool-path invocation via `EscapeHatchTracker.record("tool")`. Otherwise record a mentor-path invocation. Ear-training is inherently mentor-path — the user is choosing to build judgment, not grab a quick fix.
3. Check for lesson escalation: if the user has been training the same ear across multiple sessions, a standalone lesson on that ear-skill is warranted.

## Output contract

- An exercise set: what to listen for, references or the user's own work to apply it to.
- A check-back note stored in memory for the next session (via `MemoryStore.declare(...)` with domain tag `["ear-train"]`).
- Written reasoning with woven teaching: what to train, why it matters, the exercises, what to listen for.
- Declared observations (spoken aloud, written to memory).
- Optional: a lesson artifact if escalation is triggered.