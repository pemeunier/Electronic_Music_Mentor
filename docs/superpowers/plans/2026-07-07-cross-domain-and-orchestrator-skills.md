# Electronic Music Mentor — Cross-domain, Development & Orchestrator Skills Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the remaining 6 skills — `critique`, `diagnose`, `ear-train`, `break-a-habit`, `review-development`, and `develop-track` — completing the full skill inventory of 12 skills. These are the cross-domain act skills (critique, diagnose, ear-train), the development skills (break-a-habit, review-development), and the track-construction orchestrator skill (develop-track).

**Architecture:** Each skill is a directory under `skills/` with a `SKILL.md`, following the pattern established by the domain skills. The cross-domain and development skills reference the shared mentor guidance, consult the knowledge substrates, and use the Python infrastructure. The `develop-track` skill is the orchestrator that calls other domain skills to construct a whole track.

**Tech Stack:** Markdown (SKILL.md files), Python infrastructure (from Plan 1), knowledge substrates (from Plans 2-3), domain skills (from Plan 4).

---

## File Structure

```
Electronic_Music_Mentor/
├── skills/
│   ├── README.md                                     # (modify) remove all "(planned)" — all skills complete
│   ├── critique/                                     # (new) Task 1
│   │   └── SKILL.md
│   ├── diagnose/                                     # (new) Task 2
│   │   └── SKILL.md
│   ├── ear-train/                                    # (new) Task 3
│   │   └── SKILL.md
│   ├── break-a-habit/                                # (new) Task 4
│   │   └── SKILL.md
│   ├── review-development/                           # (new) Task 5
│   │   └── SKILL.md
│   └── develop-track/                                # (new) Task 6
│       └── SKILL.md
```

---

## SKILL.md Pattern

All skills follow the same structure as the domain skills (see `skills/bass/SKILL.md`):
- `# Skill: <name>`
- `## When to invoke` — when to use this skill, what it owns, explicit boundaries
- `## Shared guidance` — references `../../docs/superpowers/mentor-guidance.md`
- `## Workflow` — Pre-phase, Understand, [Main work], Written reasoning, Post-phase
- `## Output contract` — what the skill produces

---

### Task 1: Skill — `critique`

**Files:**
- Create: `skills/critique/SKILL.md`

- [ ] **Step 1: Write the critique skill SKILL.md**

**When to invoke:** Invoke when the user wants a comprehensive cross-domain assessment — "tell me what's wrong", "what's working", "review this track". `critique` sweeps across all domains (bass, melody, rhythm, harmony, sound-design, arrangement) and identifies issues and strengths.

Boundaries (do not invoke for): domain-specific deep fixes — when `critique` identifies a bass problem, it can hand off to `bass` for the fix. `critique` owns the *cross-domain assessment*, not the deep fixes. Do not invoke for targeted troubleshooting ("this specific thing isn't working") — that's `diagnose`. `critique` is a sweep; `diagnose` is a hunt.

**Pre-phase:** Recall memory for domains `["bass", "melody", "rhythm", "harmony", "sound-design", "arrangement"]` — critique is cross-domain, so recall everything relevant. Surface relevant memory. Apply taste-probe if the critique will involve aesthetic direction (e.g., "before I tell you what I'd change — what are you going for with this track?").

**Understand the request:** Determine the genre (consult `knowledge/genres/` — the genre's `common_failure_modes` are a key input for critique), what the user has (a full track? a sketch? a stem?), and what they want (full critique? focus on a specific area?).

**Critique (the main work):** Assess across all domains:
- **Bass**: register, rhythmic relationship to kick, harmonic role clarity, voice-leading. Consult the `bass` skill's critique criteria.
- **Melody**: motif strength, repetition/variation, contour, rhythmic placement, harmonic relationship. Consult the `melody` skill's critique criteria.
- **Rhythm**: groove feel, velocity patterns, layer roles, density. Consult the `rhythm` skill's critique criteria.
- **Harmony**: progression logic, voicing, tension/release, genre fit. Consult the `harmony` skill's critique criteria.
- **Sound-design**: synthesis approach, parameter choices, signal flow, genre fit, register/spacing. Consult the `sound-design` skill's critique criteria.
- **Arrangement**: section structure, energy arc, transitions, section roles, phrase length. Consult the `arrangement` skill's critique criteria.
- **Cross-domain issues**: frequency-space reasoning ("the low-mid is crowded — bass and pad are fighting"), coherence across domains (does the bass serve the harmony? does the rhythm serve the groove?).

Consult the genre profile's `common_failure_modes` — these are the lazy-execution patterns to check for.

Produce a written critique organized by domain, with severity/priority for each issue, and named handoffs where a domain skill should take over for the fix.

**Written reasoning:** The critique itself is the reasoning. Organize by domain, lead with the most important issues. Include woven teaching: "The bass and kick are both hitting at 80Hz on every beat — that's why the low end is muddy. The fix is either to move the bass up an octave or sidechain the bass to the kick." Not: "The low end needs work."

**Post-phase:** Declare observations (e.g., "you're overcrowding the low-mid the same way you did last time"). Update memory. Track escape-hatch (though critique is rarely tool-path — it's inherently mentor-path). Check for lesson escalation.

**Output contract:** A written critique organized by domain, with severity/priority and named handoffs to domain skills. Declared observations. Optional lesson artifact.

- [ ] **Step 2: Commit**

```bash
git add skills/critique/SKILL.md
git commit -m "feat: critique skill SKILL.md"
```

---

### Task 2: Skill — `diagnose`

**Files:**
- Create: `skills/diagnose/SKILL.md`

- [ ] **Step 1: Write the diagnose skill SKILL.md**

**When to invoke:** Invoke when the user has a specific problem they can't identify the cause of — "this isn't working and I don't know why", "the drop feels weak", "the bass sounds wrong but I don't know what's wrong". `diagnose` is a targeted hypothesis-driven hunt, distinct from `critique`'s comprehensive sweep.

Boundaries (do not invoke for): comprehensive assessment — that's `critique`. `diagnose` starts from a symptom and hunts for the root cause. Does not own the fix — hands off to the relevant domain skill once diagnosed. `diagnose` differs from `critique` in framing and workflow: critique sweeps; diagnose hunts.

**Pre-phase:** Recall memory for domains relevant to the symptom (if the user says "the bass sounds wrong", recall `["bass", "sound-design", "arrangement"]` — the symptom might be in the bass but the cause might be elsewhere). Surface relevant memory. No taste-probe — diagnosis is craft, not aesthetic.

**Understand the request:** Determine the symptom precisely. Ask the user to be specific if needed: "When you say 'the drop feels weak' — do you mean it lacks energy? lacks impact? feels empty? feels cluttered?" The symptom shapes where to hunt. Determine the genre (consult `knowledge/genres/`). Determine what the user has (the track, the stems, a description).

**Diagnose (the main work):** Follow a hypothesis-driven workflow:
1. **Form hypotheses** about what could cause the symptom. Generate 2-4 candidate hypotheses across domains. Example for "the drop feels weak":
   - H1: The build doesn't create enough tension (arrangement — consult `knowledge/theory/tension-and-release.md`)
   - H2: The drop lacks low-end weight (bass/sound-design — the bass might be too quiet or too high)
   - H3: The drop has too many elements competing (arrangement/sound-design — frequency crowding)
   - H4: The rhythmic energy drops at the transition (rhythm — the percussion pattern might thin out)
2. **Test each hypothesis** against what's in front of the user. Examine the relevant domain for each hypothesis. Consult the relevant theory documents and genre profiles.
3. **Narrow to a diagnosis.** Eliminate hypotheses that don't fit. Confirm the one that does. If multiple hypotheses fit, identify the primary cause and secondary contributors.
4. **Name the handoff.** Once diagnosed, identify which domain skill should handle the fix. Example: "The primary cause is that the bass is an octave too high — the `bass` skill should move it down. There's also a secondary issue: the build is only 8 bars when the genre expects 16 — the `arrangement` skill should extend it."

**Written reasoning:** Present the failed hypotheses, the confirmed root cause, and the named handoff. Include woven teaching: "I checked the build first because weak drops often come from weak builds — but your build is fine, it's 16 bars with a good filter sweep. The problem is the bass: it's at C3 when it should be at C2. That's why the drop has no weight — the low end is missing." Not: "The drop needs more energy."

**Post-phase:** Declare observations. Update memory. Track escape-hatch. Check for lesson escalation — if the same kind of symptom recurs across sessions, a lesson on that pattern is warranted.

**Output contract:** A written diagnosis with failed hypotheses, confirmed root cause, and named handoff to the domain skill that should fix it. Declared observations. Optional lesson artifact.

- [ ] **Step 2: Commit**

```bash
git add skills/diagnose/SKILL.md
git commit -m "feat: diagnose skill SKILL.md"
```

---

### Task 3: Skill — `ear-train`

**Files:**
- Create: `skills/ear-train/SKILL.md`

- [ ] **Step 1: Write the ear-train skill SKILL.md**

**When to invoke:** Invoke when the user wants to deliberately train their ear — "teach me to hear X", "I can't tell what's wrong with my low end", "help me recognize when a chord progression is good". `ear-train` is the most direct expression of the core experience goal: building transferable ear/judgment.

Boundaries (do not invoke for): quick answers — that's the relevant domain skill. `ear-train` has a workflow: identify what to train, give exercises, check back next session. It's deliberate practice, not a one-off explanation. Do not invoke for "what's wrong with this bass" — that's `bass` or `critique`. Invoke for "I want to learn to hear when the bass is wrong".

**Pre-phase:** Recall memory for domains relevant to what the user wants to train. Surface relevant memory — especially previous ear-training check-backs ("last time you were working on hearing low-mid crowding — did you practice?"). No taste-probe — ear-training is craft development, not aesthetic direction.

**Understand the request:** Determine what the user wants to train their ear for. Common ear-training targets:
- Low-end clarity (hearing when bass and kick clash)
- Low-mid crowding (hearing when too many elements occupy the low-mid)
- Harmonic recognition (hearing what chord is playing, what the progression is)
- Groove feel (hearing swing, pocket, velocity patterns)
- Tension and release (hearing when harmony creates tension, when it releases)
- Texture and filter movement (hearing when a filter opens/closes, when texture evolves)

Determine the user's current level (ask if not clear). Determine the genre context (consult `knowledge/genres/` — ear-training is more effective in a genre context the user knows).

**Ear-train (the main work):**
1. **Identify what to train** — narrow the target to something specific and trainable. "Hearing low-mid crowding" is good; "hearing better" is not.
2. **Give exercises** — provide concrete listening exercises:
   - **Reference listening**: point the user to the genre profile and ask them to listen to tracks in that genre, focusing on the specific thing. Example: "Listen to three dub techno tracks and focus on the low-mid. Notice how in good examples, the bass and pad don't overlap — the bass is low, the pad is higher. In lazy examples, they crowd each other."
   - **Self-assessment**: ask the user to apply the listening to their own work. Example: "Now listen to your own track's low-mid. Is the bass and pad relationship more like the good examples or the lazy ones?"
   - **A/B comparison**: if the user has a reference and their own work, compare them.
3. **Set the check-back** — store a check-back note in memory for the next session. Example: "User is training low-mid crowding recognition. Check back next session: ask them to identify whether their current low-mid is crowded, without prompting."

Store the check-back via `MemoryStore.declare(...)` with a special domain tag like `["ear-train"]` and content describing the exercise and what to check.

**Written reasoning:** Explain what to train, why it matters, the exercises, and what to listen for. Include woven teaching (this is the skill where woven teaching is most at home): "When you listen for low-mid crowding, focus on the 200-500Hz range. If the bass and a pad are both in that range, you'll hear a 'boxy' or 'muddy' quality. In good dub techno, the bass stays below 200Hz and the pad sits above 500Hz — there's a gap." Not: "Listen carefully to the low-mid."

**Post-phase:** Declare observations. Update memory — especially the check-back note. Track escape-hatch (ear-training is inherently mentor-path — the user is choosing to build judgment, not grab a quick fix). Check for lesson escalation — if the user has been training the same ear across multiple sessions, a standalone lesson on that ear-skill is warranted.

**Output contract:** An exercise set (what to listen for, references or the user's own work to apply it to) + a check-back note stored in memory for the next session. Written reasoning with woven teaching. Declared observations. Optional lesson artifact.

- [ ] **Step 2: Commit**

```bash
git add skills/ear-train/SKILL.md
git commit -m "feat: ear-train skill SKILL.md"
```

---

### Task 4: Skill — `break-a-habit`

**Files:**
- Create: `skills/break-a-habit/SKILL.md`

- [ ] **Step 1: Write the break-a-habit skill SKILL.md**

**When to invoke:** Invoke when the user wants to explicitly work on a flagged habit across sessions — "I want to work on my low-mid overcrowding", "I keep making the same mistake, help me break it", "you've noticed I overcrowd the low-mid — let's fix that". Goal-shaped entry: the user names the habit they want to break.

Boundaries (do not invoke for): quick fixes — that's the relevant domain skill. `break-a-habit` is a session structure that cuts across domains to target a specific habit. It pulls in whichever domain skills are relevant. Does not own domain expertise — delegates to domain skills for the actual work within the habit-focused session.

**Pre-phase:** Recall memory for the specific habit and related domains. This is the key skill for memory — recall the habit's lifecycle state (noticed-once? pattern? former-habit?), its occurrence count, and its history. Surface the habit's full history to the user: "You've been overcrowding the low-mid for the last 4 sessions — it's a confirmed pattern. Last session you got close to breaking it. Let's keep working on that." No taste-probe — breaking a habit is craft, not aesthetic.

**Understand the request:** Determine the habit (from memory or from the user's statement). Determine the domains involved (low-mid overcrowding involves `["bass", "sound-design", "arrangement"]`). Determine the user's goal for this session (awareness? practice? a specific track where they're applying the fix?).

**Break-a-habit (the main work):**
1. **Acknowledge the habit** — name it clearly and reference its history (mentor voice, not database voice): "Okay, the low-mid thing. You've been doing it for a while. Let's break it."
2. **Explain the habit** — why it happens, what it sounds like, why it's a problem. Consult the relevant theory documents and genre profiles. Example for low-mid crowding: consult `knowledge/theory/voice-leading.md` for register spacing principles, and the genre profile for how the genre handles the low-mid.
3. **Set the focus for this session** — what specifically will the user work on? Options:
   - **Awareness**: the user brings a track and the mentor identifies every instance of the habit.
   - **Practice**: the user works on a new section and the mentor watches for the habit in real-time (as they bring each element).
   - **Fix**: the user brings an existing track and the mentor guides them through fixing the habit (delegating to the relevant domain skill for the actual fix).
4. **Delegate to domain skills** for the actual work. If the habit is low-mid crowding and the user is fixing a bassline, invoke `bass` for the bass fix — but frame it within the habit context ("when you rebuild this bass, keep it below 200Hz — that's the low-mid habit we're breaking").
5. **Check for the habit** throughout the session. Each time the user brings new work, check whether the habit appears. If it does, name it: "that's the low-mid thing again — the bass is in the pad's range." If it doesn't, acknowledge the growth: "clean low-mid on this one — you're breaking the habit."

**Written reasoning:** Explain the habit, why it happens, the session focus, and what to watch for. Include woven teaching (this skill is about building the ear to catch the habit independently): "The reason you keep overcrowding the low-mid is that the bass and pad feel 'thin' separately, so you add more — but together they're too much. The fix isn't fewer elements; it's separating their registers." Not: "Try to avoid overcrowding."

**Post-phase:** Declare observations — especially whether the habit appeared or not in this session. Update memory: if the habit appeared, note it (occurrence count up). If it didn't, note the absence (toward decay to former-habit). Track escape-hatch. Check for lesson escalation — if the habit has been worked on across >=3 sessions, a standalone lesson on the underlying concept is warranted.

**Output contract:** A session plan targeting the habit (awareness/practice/fix mode), with domain skill handoffs for the actual work. Written reasoning with woven teaching. Declared observations (habit appeared or not). Memory updates (occurrence or absence). Optional lesson artifact.

- [ ] **Step 2: Commit**

```bash
git add skills/break-a-habit/SKILL.md
git commit -m "feat: break-a-habit skill SKILL.md"
```

---

### Task 5: Skill — `review-development`

**Files:**
- Create: `skills/review-development/SKILL.md`

- [ ] **Step 1: Write the review-development skill SKILL.md**

**When to invoke:** Invoke when the user wants to reflect on their development — "how am I doing?", "what should I focus on next?", "what habits have I broken?", "what are my weak spots?". `review-development` reads the memory profile and reflects it back as a development report.

Boundaries (do not invoke for): producing track artifacts — this skill is about the user, not the track. Does not produce MIDI or arrangement plans. Owns the reflection on memory and the recommendation for next focus. Do not invoke for "what's wrong with this track" — that's `critique`. Invoke for "what's wrong with me as a producer" (said more kindly than that).

**Pre-phase:** Recall all memory — this skill reads the entire profile. No taste-probe — this is reflection, not aesthetic. No escape-hatch tracking — this skill is inherently mentor-path.

**Understand the request:** Determine what the user wants: a full development review? A focus recommendation? A check on a specific habit? Usually the user wants the full picture.

**Review-development (the main work):** Read the entire memory profile and produce a development report:
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

**Written reasoning:** The development report itself is the reasoning. Organize clearly: what you've worked on, habits (by state), what you've broken, recommended next focus. Include woven teaching where relevant — especially in the "recommended next focus" section, explain *why* this focus serves their development. Use mentor voice throughout: "You've been cleaner on the low-mid lately — keep it up" (not "Habit state: former-habit").

**Post-phase:** Declare observations — if the review itself surfaces a new observation (e.g., "I notice you haven't worked on melody at all — that might be worth exploring"), declare it. Update memory. No escape-hatch tracking. Check for lesson escalation.

**Output contract:** A development report (what they've worked on, habits by lifecycle state, what they've broken, recommended next focus with justification). Declared observations. Memory updates. Optional lesson artifact.

- [ ] **Step 2: Commit**

```bash
git add skills/review-development/SKILL.md
git commit -m "feat: review-development skill SKILL.md"
```

---

### Task 6: Skill — `develop-track`

**Files:**
- Create: `skills/develop-track/SKILL.md`

- [ ] **Step 1: Write the develop-track skill SKILL.md**

**When to invoke:** Invoke when the user wants to construct a whole track — "help me build this track", "I want to make a dub techno track from scratch", "let's develop this project". `develop-track` is the orchestrator that coordinates across domains to build a complete track.

Boundaries (do not invoke for): single-element work — that's the relevant domain skill. `develop-track` does not own domain expertise — it delegates to `arrangement` for shape, then to `bass`/`melody`/`rhythm`/`harmony`/`sound-design` for content, then to `critique` for cross-domain coherence. Owns the *process* of construction and the *coherence* of the result. This is a skill that calls other skills — it is distinct from the Mentor Orchestrator (the relationship layer), which wraps all skill invocations including this one.

**Pre-phase:** Recall memory for domains `["arrangement", "bass", "melody", "rhythm", "harmony", "sound-design"]` — develop-track is cross-domain, so recall everything relevant. Surface relevant memory. Apply taste-probe — "before we start building — what's the vision for this track? what genre? what mood?" — develop-track is highly aesthetic, so the taste-probe is essential.

**Understand the request:** Determine the genre (consult `knowledge/genres/` — the genre profile is the primary input for the whole track). Determine the user's vision (mood, energy, length, purpose). Determine what the user already has (nothing? a sketch? some elements?).

**Develop-track (the main work):** Follow a construction process:
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

**Written reasoning:** Explain the construction process: the arrangement plan, why each part was chosen, how the parts relate, what the genre conventions are doing. Include woven teaching: "The bass is on C while the chord stab is Cm above it — that's bass-as-harmony, the dub techno approach. The stab adds the minor third color; the bass carries the root identity." Not: "The bass and chords work together."

**Post-phase:** Declare observations — develop-track is likely to surface multiple observations across domains. Update memory. Track escape-hatch. Check for lesson escalation — if a concept recurred during the construction, a standalone lesson is warranted.

**Output contract:** A track construction plan + coordinated artifacts (MIDI files per part, arrangement plan, written reasoning linking them). Declared observations. Optional lesson artifact.

- [ ] **Step 2: Commit**

```bash
git add skills/develop-track/SKILL.md
git commit -m "feat: develop-track skill SKILL.md"
```

---

### Task 7: Update skills README — all skills complete

**Files:**
- Modify: `skills/README.md`

- [ ] **Step 1: Update the skills README**

In `skills/README.md`, remove all "(planned)" markers — all 12 skills are now complete. The full inventory:

```markdown
### Domain skills (generate + critique within one domain)

- `bass` — basslines, sub, low-end voice-leading
- `melody` — leads, motifs, top-line development
- `rhythm` — patterns, grooves, percussion content
- `harmony` — chords, progressions, voicings, tonality
- `sound-design` — conceptual sound-design mentoring, synthesis reasoning
- `arrangement` — section structure, energy arc, transitions

### Track-construction skill

- `develop-track` — coordinates across domains to build a whole track

### Cross-domain act skills

- `critique` — comprehensive cross-domain sweep
- `diagnose` — targeted hypothesis-driven troubleshooting
- `ear-train` — deliberate ear-training with check-back workflow

### Development skills (about you, not the track)

- `break-a-habit` — explicit work on a flagged habit across sessions
- `review-development` — reads memory, reflects development, recommends next focus
```

- [ ] **Step 2: Run the full test suite**

Run: `.venv/bin/pytest tests/ -v`
Expected: PASS (34 tests — no regressions; this is a documentation-only change)

- [ ] **Step 3: Commit**

```bash
git add skills/README.md
git commit -m "docs: update skills README — all 12 skills complete"
```

---

## Self-Review

**1. Spec coverage:**
- critique skill — ✓ (Task 1)
- diagnose skill — ✓ (Task 2)
- ear-train skill — ✓ (Task 3)
- break-a-habit skill — ✓ (Task 4)
- review-development skill — ✓ (Task 5)
- develop-track skill — ✓ (Task 6)
- skills README updated — ✓ (Task 7)

All 6 skills follow the SKILL.md pattern. The full inventory of 12 skills (6 domain + develop-track + critique + diagnose + ear-train + break-a-habit + review-development) is complete after this plan.

**2. Placeholder scan:** No TBD or TODO. Each task specifies the exact content requirements for its SKILL.md.

**3. Consistency:** All skills reference the same shared guidance path, use the same workflow structure (pre-phase, understand, main work, written reasoning, post-phase), and follow the same output contract pattern. The cross-domain skills (critique, diagnose) explicitly distinguish themselves from each other (sweep vs hunt). The development skills (break-a-habit, review-development) are memory-centric. develop-track is the only skill that calls other skills as part of its workflow.