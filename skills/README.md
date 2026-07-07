# Electronic Music Mentor Skills

Each skill is an opencode skill: a directory with a `SKILL.md` describing when to invoke it, the workflow it follows, and its output contract. Skills are invoked via the opencode `skill` tool or by mentioning them in conversation.

## Shared guidance

Every skill follows the shared mentor voice, guards, and post-phase behaviors defined in [`../docs/superpowers/mentor-guidance.md`](../docs/superpowers/mentor-guidance.md). Each skill's `SKILL.md` references this — the mentor consistency comes from shared guidance, not from a separate orchestrator process.

## Skill inventory

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

## Substrates (not skills)

Skills consult shared knowledge resources stored as files under `knowledge/`:
- `knowledge/theory/` — music-theory foundations (the `theory` substrate)
- `knowledge/genres/` — genre profiles (the `genre-profiles` substrate)

User memory is stored in `~/.electronic-music-mentor/memory` (or a project-local equivalent), managed by `electronic_music_mentor.memory.MemoryStore`.