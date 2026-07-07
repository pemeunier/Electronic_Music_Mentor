# Knowledge Base

Substrates consumed by Electronic Music Mentor skills. This is the foundation the whole system reasons on.

## Sourcing rules

All content in this directory is **original writing** produced through active research of authoritative references — theory texts, production books, documented genre histories, technical references, and credible online material.

Rules:
- Study sources, synthesize, and rewrite in the project's own words and structure.
- Keep citations/attributions to sources (in a `## Sources` section at the bottom of each file).
- Never reproduce verbatim text from copyrighted sources.
- Content grows over time; under-profiled topics are flagged rather than improvised shallowly.

## Structure

- `theory/` — the `theory` substrate: music-theory foundations (harmony, voice-leading, rhythm, form) as they apply to electronic music. Consumed by `harmony`, `bass`, `melody`, `rhythm`, `arrangement`.
- `genres/` — the `genre-profiles` substrate: one file per genre, encoding the spirit of each electronic music genre. Consumed by all domain skills.

## Validation

Run `python -m electronic_music_mentor.substrates.validator <path>` to validate a substrate file against its schema. Use this when adding or modifying knowledge content.