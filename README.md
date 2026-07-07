# Electronic Music Mentor

Agent skills to help you learn electronic music production. An AI mentor for electronic music producers that helps with composition and sound design ideas, without any live connection to a DAW.

It feels like sitting with a world-class producer/mentor who is teaching you to think and hear like they do — not just handing you answers, but building your own judgment over time.

## What this is

A set of opencode skills plus Python infrastructure:
- **Skills** (in `skills/`) — opencode skills for bass, melody, rhythm, harmony, sound-design, arrangement, and more. Each skill is a directory with a `SKILL.md` defining when to invoke it and the workflow it follows.
- **Knowledge substrates** (in `knowledge/`) — music-theory foundations and genre profiles, researched from authoritative references and written in the project's own words. Skills consult these.
- **Python infrastructure** (in `src/`) — MIDI generation (`midi/`), memory store (`memory/`), and substrate validators (`substrates/`).
- **Shared mentor guidance** (in `docs/superpowers/mentor-guidance.md`) — the mentor voice, guards, and behaviors every skill follows.

## Setup

```bash
pip install -e ".[dev]"
pip install mido
```

## Usage

Invoke a skill via opencode, e.g. the `bass` skill to write or critique a bassline. The skill reads the relevant substrates, uses the memory store to recall what it knows about you, and produces a `.mid` file plus written reasoning.

See [`skills/README.md`](skills/README.md) for the full skill inventory and [`docs/superpowers/specs/2026-07-07-electronic-music-mentor-design.md`](docs/superpowers/specs/2026-07-07-electronic-music-mentor-design.md) for the design.