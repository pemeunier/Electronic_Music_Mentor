# Skill: break-a-habit

## When to invoke

Invoke when the user wants to explicitly work on a flagged habit across sessions — "I want to work on my low-mid overcrowding", "I keep making the same mistake, help me break it", "you've noticed I overcrowd the low-mid — let's fix that". Goal-shaped entry: the user names the habit they want to break.

Do not invoke for quick fixes — that's the relevant domain skill. `break-a-habit` is a session structure that cuts across domains to target a specific habit. It pulls in whichever domain skills are relevant. Does not own domain expertise — delegates to domain skills for the actual work within the habit-focused session.

## Shared guidance

Follow the shared mentor voice, guards, and post-phase behaviors defined in [`../../docs/superpowers/mentor-guidance.md`](../../docs/superpowers/mentor-guidance.md). In particular:

- No taste-probe — breaking a habit is craft, not aesthetic.
- Recall relevant memory before running — especially the habit's lifecycle state and history.
- Include woven teaching in the written reasoning — this skill is about building the ear to catch the habit independently.
- Declare observations aloud after running (e.g., "the low-mid thing showed up again" — mentor voice, not database voice).
- Track escape-hatch use if the user invokes with `just-give-it-to-me`.

## Workflow

### 1. Pre-phase

1. Recall memory for the specific habit and related domains. This is the key skill for memory — recall the habit's lifecycle state (noticed-once? pattern? former-habit?), its occurrence count, and its history.
2. Surface the habit's full history to the user (mentor voice, not database voice). Example: "You've been overcrowding the low-mid for the last 4 sessions — it's a confirmed pattern. Last session you got close to breaking it. Let's keep working on that."
3. No taste-probe — breaking a habit is craft, not aesthetic.

### 2. Understand the request

Determine:
- The habit (from memory or from the user's statement).
- The domains involved (low-mid overcrowding involves `["bass", "sound-design", "arrangement"]`).
- The user's goal for this session: awareness? practice? a specific track where they're applying the fix?

### 3. Break-a-habit

1. **Acknowledge the habit** — name it clearly and reference its history (mentor voice, not database voice): "Okay, the low-mid thing. You've been doing it for a while. Let's break it."
2. **Explain the habit** — why it happens, what it sounds like, why it's a problem. Consult the relevant theory documents and genre profiles. Example for low-mid crowding: consult `knowledge/theory/voice-leading.md` for register spacing principles, and the genre profile for how the genre handles the low-mid.
3. **Set the focus for this session** — what specifically will the user work on? Options:
   - **Awareness**: the user brings a track and the mentor identifies every instance of the habit.
   - **Practice**: the user works on a new section and the mentor watches for the habit in real-time (as they bring each element).
   - **Fix**: the user brings an existing track and the mentor guides them through fixing the habit (delegating to the relevant domain skill for the actual fix).
4. **Delegate to domain skills** for the actual work. If the habit is low-mid crowding and the user is fixing a bassline, invoke `bass` for the bass fix — but frame it within the habit context ("when you rebuild this bass, keep it below 200Hz — that's the low-mid habit we're breaking").
5. **Check for the habit** throughout the session. Each time the user brings new work, check whether the habit appears. If it does, name it: "that's the low-mid thing again — the bass is in the pad's range." If it doesn't, acknowledge the growth: "clean low-mid on this one — you're breaking the habit."

### 4. Written reasoning output

Produce written reasoning that explains the habit, why it happens, the session focus, and what to watch for. The reasoning must:
- Include woven teaching (this skill is about building the ear to catch the habit independently). Example: "The reason you keep overcrowding the low-mid is that the bass and pad feel 'thin' separately, so you add more — but together they're too much. The fix isn't fewer elements; it's separating their registers." Not: "Try to avoid overcrowding."
- State opinions as the mentor's take with reasoning. Yield if the user overrides.

### 5. Post-phase

1. Declare observations aloud (mentor voice) — especially whether the habit appeared or not in this session.
2. Update memory: if the habit appeared, note it (occurrence count up). If it didn't, note the absence (toward decay to former-habit). Use `MemoryStore.declare(...)`.
3. If the user invoked with `just-give-it-to-me`, record a tool-path invocation via `EscapeHatchTracker.record("tool")`. Otherwise record a mentor-path invocation.
4. Check for lesson escalation: if the habit has been worked on across >=3 sessions, a standalone lesson on the underlying concept is warranted.

## Output contract

- A session plan targeting the habit (awareness/practice/fix mode), with domain skill handoffs for the actual work.
- Written reasoning with woven teaching (the habit, why it happens, the session focus, what to watch for).
- Declared observations (habit appeared or not).
- Memory updates (occurrence or absence).
- Optional: a lesson artifact if escalation is triggered.