# Genre Profiles Substrate

One file per electronic music genre, encoding the spirit of each genre. Consumed by all domain skills.

## Planned genres (content to be built in a later plan)

- Dub Techno
- Deep House
- Detroit Techno
- Jungle / Drum & Bass
- UK Garage
- Ambient
- Minimal Techno
- Electro
- IDM / Braindance
- (others as the system grows)

## Format

Each genre profile is a Markdown file with front-matter fields validated by `electronic_music_mentor.substrates.validator.validate_genre_profile`:
- `name`
- `tempo_range` (dict with `min`, `max`, `feel`)
- `rhythmic_conventions` (list)
- `harmonic_conventions` (list)
- `textural_sonic_conventions` (list)
- `arrangement_conventions` (list)
- `spirit` (substantial prose — what the genre is trying to do, what good examples do, what lazy examples miss)
- `common_failure_modes` (list)
- `## Sources` section at the bottom with attributions