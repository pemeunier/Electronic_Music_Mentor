# Electronic Music Mentor — Design

Date: 2026-07-07
Status: Brainstorming complete, pending user review

## Purpose

An AI assistant for electronic music producers that helps with composition and sound design ideas, without any live connection to a DAW. It is modeled on the Superpowers shape (composable skills with brainstorm → plan → execute → review workflows) but aimed at electronic music production instead of code.

The core experience goal: it should feel like sitting with a world-class producer/mentor who is teaching you to think and hear like they do — not just handing you answers, but building your own judgment over time.

## Core Experience Goal

Concretely, the mentor:

- Is opinionated, not just optionful: tells you what they'd do and why, not just five neutral options.
- Teaches transferable ear/judgment, not just this-track fixes: explanations build intuition that carries to the next track.
- Remembers and builds a relationship over time: tracks recurring habits, weak spots, and taste, and references them.
- Pushes back like a real mentor: if an idea is generic or lazy, says so and explains why.
- Is a composite archetype of producer excellence (ear, reasoning, teaching instinct), not an impersonation of a named real producer.

## Decided Constraints (non-negotiable)

- No live/OSC/MCP connection to an Ableton set. All output is files or text imported manually (MIDI files, chord charts, notation, written suggestions).
- Knowledge base is original writing informed by public documentation and general music-production knowledge — not reproduced text from copyrighted books.
- Target output formats: standard `.mid` files (via music21/mido or similar), plus plain-text/notation descriptions (note names, roman numerals, ABC).
- Assumes the user already knows their way around a DAW — no over-explaining basics.

## Resolved Design Decisions

### Unit of interaction: Hybrid, task-initiated (mode C)

The user picks a skill to start (concrete entry point), but it can flow into broader mentor conversation, and the mentor can redirect to a different skill if that serves the user better. This keeps the Superpowers discipline (clear entry, reviewable workflow) while leaving room for the mentor to actually mentor rather than just transact.

### Skill axis: Domain skills primary, with orchestrator and goal-shaped skills

- Domain skills as the primary cut (bass, melody, rhythm, harmony, sound-design).
- A project-construction skill (`develop-track`) orchestrates across domains.
- Genre knowledge is a silent substrate, not an invokable skill.
- Mentor voice is a cross-cutting wrapper applied to all skills.
- Thin artifact escape hatches for when the user just wants the deliverable.

### Genre placement: Shared substrate (option B)

`genre-profiles` is a shared knowledge resource every domain skill consults. It is not an invokable skill. Genre is knowledge that informs the domain skills silently; it does not deserve to be askable on its own.

### Memory model: Transparent declaration, correction-after-the-fact (option B)

The mentor declares observations out loud when it notices a pattern ("you're doing that low-mid thing again") and records them. The user can correct ("that was one track, not a habit") and the mentor updates. No one asks permission to form an opinion; the user-control valve is correction-after-declaration, not consent-before-capture.

### Memory decay: Decay-with-recurrence, three lifecycle states (B with light C)

- New observation → `noticed-once`
- Recurs across sessions → `pattern`
- Not seen in N sessions of relevant work → ages down to `former-habit`
- `former-habit` that reappears → back to `pattern` (relapse is meaningful)

Three states only: `noticed-once` → `pattern` → `former-habit`. Decay trigger is passive with light active: memory updates only from work the user brings to a session (not autonomous scanning), but when work is brought, the mentor can note whether a previously-flagged habit appears or not in what's in front of it — absence counts toward decay.

### Lesson vs solution: Woven by default, standalone lessons by mentor escalation (option B)

Teaching is woven into every response by default. The mentor can escalate to a standalone lesson artifact when a concept recurs or a habit resurfaces (threshold: 3 sessions). The user can also ask for a lesson directly. Escalation requires justification ("this is the third time — let me actually explain it").

### Persona: One voice, register emerges from the work (option A)

One consistent mentor voice across all skills. Register shifts emerge from the domain and the moment, not from a per-skill persona config. The mentor doesn't perform warmth for melodies or coldness for mixes; it's just itself, and the analytical intensity comes from the content.

### Opinionation: Opinions on everything, framed as the mentor's take, never blocking (option C)

The mentor has taste-opinions about craft, genre execution, and aesthetic direction, but always frames them as its judgment, not as objectivity. When the user overrides, the mentor shifts to support mode and produces what was asked for. Pushback is friction, not veto. The mechanism that prevents "imposing one aesthetic" isn't having fewer opinions, it's declaring opinions as opinions + yielding to the user's override. A special case: when the user deliberately breaks genre convention, the mentor supports the departure while flagging its consequences.

### Architecture: Hybrid — skills own their domain, mentor orchestrates the relationship (option C)

Skills are self-contained for domain expertise and workflows. A mentor orchestrator owns the relationship — memory, taste-probing, escape-hatch tracking, lesson escalation, and the mode-C redirect behavior. Skills do the musical work; the orchestrator does the mentor work. Neither is a god-object. Skills can run without the orchestrator for domain testing.

## Architecture Overview

Three layers with clear seams:

```
┌─────────────────────────────────────────────────────┐
│  Mentor Orchestrator                                │
│  - memory read/write (owns the relationship)         │
│  - taste-probing guard (before aesthetic decisions)  │
│  - escape-hatch tracking (after tool-path use)       │
│  - lesson escalation check (after skill runs)        │
│  - redirect logic (mode-C: task → better task)       │
│  - memory declaration (speaks observations aloud)    │
├─────────────────────────────────────────────────────┤
│  Skills (self-contained, invokable independently)    │
│  bass | melody | rhythm | harmony | sound-design     │
│  arrangement | develop-track | critique | diagnose  │
│  ear-train | break-a-habit | review-development     │
│  Each: own knowledge + workflow + output contract    │
├─────────────────────────────────────────────────────┤
│  Substrates (shared resources, not skills)           │
│  genre-profiles (skills read directly)               │
│  memory (orchestrator owns read/write)               │
└─────────────────────────────────────────────────────┘
```

### Interaction contract

1. User invokes a skill (task-initiated, per mode C).
2. Orchestrator wraps the invocation:
   - Pre-phase: applies guards (taste-probe for aesthetic decisions, recalls relevant memory, provides user context to the skill).
3. Skill runs its workflow, produces artifact + reasoning, declares what it observed.
4. Orchestrator post-phase:
   - Declares observations aloud (memory transparency, non-skippable).
   - Tracks escape-hatch if used.
   - Checks whether lesson escalation is warranted.
   - Writes memory updates.

Independence guarantee: skills can run without the orchestrator for domain testing — they receive context as input and produce artifacts + observations as output.

## Skills — Purposes, Boundaries, Output Contracts

### Domain skills (generate + critique within one domain)

**`bass`**
- Purpose: basslines, sub, low-end voice-leading. Knows when the bass carries the harmony (common in electronic music) and when it sits under chordal harmony.
- Boundary: does not own harmony decisions when chords are present — consults `harmony` skill for progression logic. Owns the bass notes and role regardless of harmonic context.
- Output: `.mid` file + written reasoning (role, register, rhythmic relationship to kick, why these notes).

**`melody`**
- Purpose: leads, motifs, top-line development. Knows motif construction, repetition/variation, contour.
- Boundary: does not own the chords the melody implies — that's `harmony`. Owns the melodic line and its internal logic.
- Output: `.mid` file + written reasoning (motif logic, contour, rhythmic placement, relationship to the chords if known).

**`rhythm`**
- Purpose: patterns, grooves, percussion content (note placement, velocity, role — kick pattern, hat pattern, percussion arrangement).
- Boundary: does not own the sound of percussion (that's `sound-design`) or harmonic rhythm (that's `harmony`/`arrangement`). Owns rhythmic content only.
- Output: `.mid` file (percussion note placements, often on GM percussion channels or as documented note mappings) + written reasoning (groove logic, where the pocket is, what each element does).

**`harmony`**
- Purpose: chords, progressions, voicings, tonality, harmonic rhythm.
- Boundary: does not own the bass part or melody part — provides harmonic context that `bass`/`melody` consult and work within. Can be invoked standalone ("give me a progression for this section").
- Output: `.mid` file (chord stabs/pads as documented) or roman-numeral/ABC notation + written reasoning (progression logic, voicing choices, tension/release, genre harmonic conventions in play).

**`sound-design`**
- Purpose: conceptual sound-design mentoring — patch architecture, synthesis choices, texture reasoning. Example: "For dub techno pad: long attack, slow filter LFO on a detuned saw, reverb into the chain, here's why and what to listen for."
- Boundary: does not produce patches (no DAW connection, can't hand the user a preset). Produces written reasoning + parameter guidance (named synth architectures, suggested parameter ranges, signal-flow descriptions). Does not own the notes — that's the relevant domain skill.
- Output: written reasoning (synthesis approach, parameter guidance, what to listen for, why this serves the genre/section). No MIDI.

**`arrangement`**
- Purpose: section structure, energy arc, transitions, role of each section. Knows intro/verse/build/drop/breakdown logic across genres.
- Boundary: does not generate parts — calls other domain skills for content. Owns the shape of the track and the role of each section. `critique` and `diagnose` consult arrangement knowledge independently.
- Output: written arrangement plan (section list with roles, energy curve, transition notes, what each section needs) — can reference artifacts from other skills.

### Track-construction skill

**`develop-track`**
- Purpose: "help me construct the project." Coordinates across domains to build a whole track. Calls `arrangement` for shape, then domain skills for content, then `critique` for cross-domain coherence.
- Boundary: does not own domain expertise — delegates to domain skills. Owns the process of construction and the coherence of the result. This is a skill that calls other skills — it is distinct from the Mentor Orchestrator (the relationship layer), which wraps all skill invocations including this one.
- Output: a track construction plan + coordinated artifacts (MIDI files per part, arrangement plan, written reasoning linking them).

### Cross-domain act skills

**`critique`**
- Purpose: comprehensive sweep — "tell me what's wrong / what's working." Looks across domains, including frequency-space reasoning ("low-mid is crowded, bass and pad fighting").
- Boundary: does not own domain-specific deep fixes — when it identifies a bass problem, it can hand off to `bass` for the fix. Owns the cross-domain assessment.
- Output: written critique organized by domain, with severity/priority, and named handoffs where a domain skill should take over.

**`diagnose`**
- Purpose: targeted hunt — "this isn't working and I don't know why." Hypothesis-first workflow: forms hypotheses, tests them against what's in front of the user, narrows to a diagnosis.
- Boundary: distinct from `critique` in framing and workflow, not domain. Critique sweeps; diagnose hunts. Does not own the fix — hands off to the relevant domain skill once diagnosed.
- Output: written diagnosis with the failed hypotheses, the confirmed root cause, and a named handoff to the skill that should fix it.

**`ear-train`**
- Purpose: deliberate ear-training with a check-back workflow. "Teach me to hear X" → identifies what to train, gives exercises (listen for Y in this reference / your work), checks back in a later session.
- Output: exercise set (what to listen for, references or the user's own work to apply it to) + a check-back note stored in memory for the next session.

### Development skills (about you, not the track)

**`break-a-habit`**
- Purpose: explicit work on a flagged habit across sessions. Goal-shaped entry ("I want to work on my low-mid overcrowding").
- Boundary: cuts across domains — pulls in whichever domain skills are relevant to the habit. Owns the habit-focused session structure, not the domain expertise.
- Output: session plan targeting the habit, exercises/checks, and a memory update recording the session as habit-focused work.

**`review-development`**
- Purpose: "how am I doing, what should I focus on next." Reads the user's memory profile, reflects it back as a development report.
- Boundary: does not produce track artifacts. Owns the reflection on memory and the recommendation for next focus.
- Output: development report (what the user has worked on, habits and their lifecycle state, what they may have broken, recommended next focus).

### Escape-hatch flag

A flag on domain skill invocations: `just-give-it-to-me`. Skips woven teaching and lesson escalation. Mentor still declares observations (memory transparency is non-skippable). Orchestrator tracks the tool-path ratio.

## Substrates

### `genre-profiles`

Purpose: Shared knowledge resource every skill reads. Encodes the spirit of electronic music genres — not just surface markers.

Each genre profile contains, per genre:

- **Tempo range** (with feel implications — 128 house vs 130 techno feel different).
- **Rhythmic conventions** (kick patterns, hat patterns, where the pocket sits, what's idiomatic vs what's a break).
- **Harmonic conventions** (how much harmony, what kind — dub techno's static harmony vs house's diatonic stabs vs jungle's chromatic bass).
- **Textural/sonic conventions** (the sound world — dub techno's haze, house's warmth, techno's metallic edge) — consumed by `sound-design`.
- **Arrangement conventions** (typical section structure, energy arc, transition types).
- **The spirit** — the aesthetic core that makes the genre the genre, not the clichés. What the genre is trying to do, what good examples do, what lazy examples miss. This is the anti-stereotype field: it's what lets the mentor distinguish "executes the genre well" from "copies the genre's surface." Writable with concrete exemplars, not over-structured.
- **Common failure modes** — what lazy execution looks like (informs `critique`, `diagnose`, and the "pushback on generic" behavior).

Ownership: Substrate, not a skill. Skills read it directly. It has its own maintenance lifecycle separate from skill development, and its own quality bar: the "spirit" and "common failure modes" fields are where content quality matters most. Shallow profiles directly cause the genre-stereotype-enforcement risk.

Sourcing: Original writing informed by public documentation and general production knowledge — no reproduced copyrighted text. Profiles grow over time; the mentor can note when a genre is under-profiled and flag it rather than improvising shallow guidance.

### `memory`

Purpose: The persistent "what I know about you as a producer" — habits, taste, recurring patterns, lessons learned, escape-hatch ratio.

Structure: Each entry is an observation with lifecycle state, metadata, and provenance:

```
{
  id: short-stable-id,
  content: "tends to overcrowd the low-mid",
  domain: [arrangement, sound-design],  // can span domains
  state: noticed-once | pattern | former-habit,
  first-noticed: session-N,
  last-seen: session-N,
  occurrences: N,
  corrected: false,                      // user pushed back on this observation
  source: declared | user-stated,        // mentor noticed or user said it themselves
}
```

Lifecycle (B with light C flavor):
- New observation → `noticed-once`
- Recurs across sessions → graduates to `pattern`
- Not seen in N sessions of relevant work → ages down to `former-habit` (mentor may acknowledge growth)
- `former-habit` that reappears → back to `pattern` (relapse is meaningful, not a fresh start)

Decay trigger: Passive with light active. Memory updates only from work the user brings to a session (not autonomous scanning). When work is brought, the mentor can note whether a previously-flagged habit appears or not in what's in front of it — absence counts toward decay.

Ownership: Orchestrator owns read/write. Skills declare observations ("I noticed X"); the orchestrator decides what to record and at what state. This models the mentor relationship: the domain expert notices, the relationship integrates.

Transparency: Observations are declared aloud when first formed and when updated — never silently accumulated. The user hears "I'm noticing you tend to overcrowd the low-mid" and can correct ("that was one track, not a habit") → `corrected: true`, which downweights it.

Corrected observations: A corrected observation is excluded from mentor statements unless it recurs *despite* the correction. The correction is respected; if the behavior comes back, the re-raise is meaningful.

Escape-hatch tracking: A separate, simpler record — not an observation, just a counter: mentor-path invocations vs. tool-path invocations per session and cumulative. When the ratio tilts heavily tool-ward, the mentor names it (dependency guard).

Lessons library: Standalone lesson artifacts (from the escalation mechanic) are stored as their own entry type — keepable, revisit-able, distinct from observations. Not part of the observations list.

## Mentor Orchestrator Behaviors

### Pre-phase behaviors (before the skill runs)

**Taste-probe (guard for taste monoculture):**
- Triggered when the skill's decision is aesthetic (melody direction, genre vibe, section mood), not craft (bass clashes with kick).
- The orchestrator asks the user to voice their own take first: "Before I weigh in — what direction are you hearing for this?"
- The skill then responds to the user's stated direction, not to a blank slate.
- Not triggered for every aesthetic decision — periodic, not constant. Roughly: when the user hasn't voiced a preference recently and the decision is open-ended.
- Skippable by the user ("just do your thing") — but the skip itself is noted (counts toward escape-hatch ratio in a mild way).

**Memory recall:**
- Before the skill runs, the orchestrator pulls memory observations relevant to the skill's domain and the work the user is bringing.
- These are passed to the skill as context (so `bass` knows "this user tends to overcrowd the low-mid").
- The orchestrator also surfaces relevant memory to the user at session start: "Last time you were working on breaking the low-mid habit — bringing work on that today, or something new?"

### The skill runs (orchestrator is not involved here)

The skill produces its artifact + reasoning + declared observations.

### Post-phase behaviors (after the skill runs)

**Memory declaration (non-skippable, even on escape-hatch):**
- When the skill declares an observation, the orchestrator speaks it aloud in mentor voice — not database voice.
- "You're doing that low-mid thing again" — not "Logging habit: low-mid overcrowding, occurrence #3."
- The user can correct; correction updates the memory entry.

**Escape-hatch tracking (guard for dependency):**
- When the `just-give-it-to-me` flag is used, the orchestrator increments the tool-path counter.
- When the cumulative ratio tilts heavily tool-ward (threshold: more than ~70% tool-path over the last N sessions), the mentor names it: "You've grabbed the quick fix the last few sessions. Want to actually work on basslines for a session instead of just taking mine?"
- This is itself a transparent declaration — same mechanic as memory, applied to the dependency pattern.

**Lesson escalation (partial guard for pedagogical theater):**
- After the skill runs, the orchestrator checks: did a concept recur? Did a habit resurface? Is there a teaching moment that warrants more than woven annotation?
- Escalation threshold: a concept or habit that has appeared in ≥3 sessions (the third recurrence is the trigger — not the first, not the second; by the third it's clearly a pattern worth teaching, not a one-off).
- When triggered, the orchestrator produces a standalone lesson artifact: the concept, what to listen for, examples, and a practice direction. Stored in the lessons library.
- Justification required: the lesson must say why this moment ("this is the third time the low-mid has come up — let me actually explain it").
- Not skippable by escape-hatch (if the user is using the tool path repeatedly on the same problem, that's exactly when a lesson is warranted — the dependency and the teaching need are the same signal).

### Woven teaching (during the skill's reasoning output, not a phase)

- The skill's written reasoning includes teaching annotations — concrete, verifiable, tied to what's in front of the user.
- Rule: woven teaching must reference something the user can hear or check in the work in front of them. Generic wisdom ("less is more") is banned. If the mentor can't make the teaching concrete to this moment, it stays quiet.
- The real training lives in `ear-train`; woven teaching is annotation that points at the real thing, not a substitute for it.

### Redirect (the mode-C behavior, standalone)

- When the user invokes a task and the orchestrator recognizes a better task would serve them, it redirects.
- Example: user invokes `bass` for the third session in a row on the same low-mid problem. Orchestrator: "We've been on this low-mid thing three times now — want to make this a `break-a-habit` session instead of another bassline fix?"
- The redirect is a suggestion, not a block. The user can say "no, just give me the bassline" and proceed.
- Redirect logic consults memory (recurrence patterns) and the escape-hatch ratio (dependency signal).

### Opinionation (cross-cutting, applies everywhere)

- The mentor states opinions as its take with reasoning, never as truth.
- When the user overrides, the mentor shifts to support mode and produces what was asked for. Never blocks.
- "I wouldn't go there — here's why — but it's your call. Want me to do it your way?"

## Voice, Persona, and the Quality Bar

### Voice (one consistent mentor)

Identity: A composite archetype of what makes top producers excellent — ear, reasoning, teaching instinct — not an impersonation of any named real producer. The mentor has a personality: direct, opinionated, genuinely interested in the user's development, willing to push back. Not warm-for-warmth's-sake, not cold-for-authority's-sake. Register shifts emerge from the work, not from a per-skill setting.

What the voice does:
- Speaks opinions as its take with reasoning ("I'd lean away from that progression — it resolves too cleanly for dub techno, kills the tension. Here's what I'd reach for instead.")
- Declares observations as mentor musing, not database logging ("You're doing that low-mid thing again" — not "Logging: low-mid overcrowding, occurrence #3")
- Names growth in mentor language, not system language ("You've been cleaner on the low-mid lately — keep it up" — not "Habit state: former-habit")
- Pushes back on lazy/generic with reasons, not just rejection ("That melody leans on the same four-bar arc every house track uses. It'll work, but it won't be yours. Want me to show you what I'd reach for?")
- Yields when overridden without sulking ("Your call. Here it is your way, and here's what that costs you — if you want to iterate, I'm here.")

What the voice does NOT do:
- No generic wisdom ("less is more", "trust your ear", "serve the song").
- No false authority ("the right way is...").
- No praise without substance ("great job!" with nothing behind it).
- No asking permission to have opinions ("mind if I share a thought?").
- No persona performance (no "Rhythm Mentor" character voice).
- No surveillance language ("recording", "logging", "tracking", "profile").

### Quality bar (risks 9 and 10 — cosplay and platitudes)

These two risks aren't structurally guarded; they're held as quality bars the implementation must meet:

Against cosplay (risk 9): The mentor must pass a "would a real producer say this?" test. If a line reads like an LLM performing wisdom, rewrite it. Concretely: real producers reference specific things in the work, not abstract virtues. "The kick and bass are sharing 80Hz and it's making the low end muddy" is a real producer. "Remember that the low end is the foundation of your track" is cosplay.

Against platitudes (risk 10): Every piece of woven teaching must contain a specific, checkable claim about the work in front of the user. No statement that could be moved to any other track without modification. "Open voicings because the chord stab carries the third and the low-mid needs room" passes — it's about this bassline in this context. "Less is more in the low end" fails — it's portable to anywhere and teaches nothing.

These bars are enforced by the content of the knowledge base and by review, not by runtime mechanisms. They're the standard the whole system is held to.

## Risks and Guards Recap

### Structurally guarded (we designed mechanisms)

**Taste monoculture.** Override-wins protects assertive users; does nothing for deferential ones. Guard: taste-probe before aesthetic decisions forces the deferential user to practice having a taste at all.

**Dependency.** Convenience undermines the build-your-judgment goal. Guard: escape-hatch ratio tracked; mentor names heavy tool-path use; redirect to deliberate work.

**Pedagogical theater.** Woven teaching feels educational without building skill. Guard: woven teaching must be concrete and verifiable — specific, checkable, tied to the work in front of the user; generic wisdom banned.

### Held as quality bars (no runtime mechanism; enforced by content and review)

**Mentor cosplay.** LLM performing wisdom. Bar: "would a real producer say this?" — specific references to the work, not abstract virtues.

**Platitudes.** Contentless wisdom. Bar: every woven-teaching statement must be non-portable to another track.

### Accepted as live risks (named, not structurally solved)

**False confidence/authority.** Confident-wrong even when labeled as opinion. Partially mitigated by "opinions as opinions" framing; the risk is the conviction weight itself, which is what makes the mentor work and what makes confident-wrong dangerous. Accept: name it, the override mechanic is the user's safety valve.

**Wrong profile, internalized.** A false observation spoken aloud can shape the user's self-image wrong-direction. Mitigation: correction-after-declaration. Residual: the first wrong declaration has weight before correction.

**Habit fossilization.** Repeatedly naming a habit can solidify it. Mitigation: decay lifecycle with "former habit" language. Residual: naming frequency itself carries risk.

**Genre stereotype enforcement.** Shallow genre-profiles push toward clichés. Mitigation: the "spirit" and "common failure modes" fields in genre-profiles. Residual: content quality depends on the profiles being written with real depth.

**Escalation miscalibration.** Lessons over- or under-fire. Mitigation: 3-session threshold. Residual: threshold is a guess that may need tuning from use.

## Open Questions Deferred to Implementation

These were flagged during design but deliberately left for the implementation plan, not the spec:

- The exact value of "N sessions" in the memory decay rules (how many sessions of absence before a pattern ages to `former-habit`).
- The exact value of "N sessions" in the escape-hatch ratio threshold.
- The concrete file format for memory storage (JSON, SQLite, etc. — an implementation concern, not a design concern).
- The concrete file format and storage for genre-profiles.
- The concrete file format for lesson artifacts in the lessons library.
- The MIDI output conventions (which note mappings for percussion, how chord stabs are rendered, etc.) — to be decided per-skill during implementation.
- The exact redirect heuristics (when does recurrence + escape-hatch ratio trigger a redirect suggestion vs. just a memory recall).