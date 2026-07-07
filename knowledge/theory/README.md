# Theory Substrate

Music-theory foundations as they apply to electronic music. Consumed by the `harmony`, `bass`, `melody`, `rhythm`, and `arrangement` skills.

## Documents

- [Voice-leading](voice-leading.md) — smooth chord connection, with electronic-music specifics on bass-as-harmony and register spacing
- [Diatonic harmony](diatonic-harmony.md) — the seven diatonic chords, common progressions, and how electronic genres use them
- [Chromatic harmony](chromatic-harmony.md) — borrowed chords, secondary dominants, modulation, and their use in electronic music
- [Bass-as-harmony](bass-as-harmony.md) — when the bass carries the harmonic identity, the defining approach in many electronic genres
- [Static harmony](static-harmony.md) — pedal points and two-chord loops, driving through rhythm and texture
- [Rhythmic subdivision and groove](rhythmic-subdivision.md) — grids, swing, pocket, velocity, and groove signatures
- [Phrase and form](phrase-and-form.md) — motifs, repetition, variation, additive form, and energy arcs
- [Tension and release](tension-and-release.md) — harmonic, rhythmic, and textural tension; the build-drop

## Format

Each theory document is a markdown file with YAML front-matter validated by `electronic_music_mentor.substrates.validator.validate_theory_document`, loaded by `electronic_music_mentor.substrates.loader.load_theory_document`:
- `topic`
- `summary`
- `principles` (list)
- `electronic_music_notes`
- `examples` (list)
- `## Sources` section at the bottom with attributions