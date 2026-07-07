# Genre Profiles Substrate

One file per electronic music genre, encoding the spirit of each genre. Consumed by all domain skills.

## Documents

- [Dub Techno](dub-techno.md) — hypnotic immersion through repetition and slow change
- [Deep House](deep-house.md) — warmth and soul through groove and harmony
- [Detroit Techno](detroit-techno.md) — mechanical precision with emotive depth
- [Jungle / Drum & Bass](jungle-drum-and-bass.md) — breakbeat energy and sub-bass weight
- [UK Garage](uk-garage.md) — bouncy, forward-leaning swing and broken patterns
- [Ambient](ambient.md) — atmosphere and sustained mood over rhythm
- [Minimal Techno](minimal-techno.md) — depth through reduction; each element matters more
- [Electro](electro.md) — robotic funk through 808 programming and vocoder
- [IDM / Braindance](idm-braindance.md) — exploration and intricacy over groove and convention

## Format

Each genre profile is a markdown file with YAML front-matter validated by `electronic_music_mentor.substrates.validator.validate_genre_profile`, loaded by `electronic_music_mentor.loader.load_genre_profile`:
- `name`
- `tempo_range` (dict with `min`, `max`, `feel`)
- `rhythmic_conventions` (list)
- `harmonic_conventions` (list)
- `textural_sonic_conventions` (list)
- `arrangement_conventions` (list)
- `spirit` (substantial prose — what the genre is trying to do, what good examples do, what lazy examples miss)
- `common_failure_modes` (list)
- `## Sources` section at the bottom with attributions