from electronic_music_mentor.substrates.validator import (
    validate_genre_profile,
    ValidationError,
)


def test_valid_genre_profile_passes():
    profile = {
        "name": "Dub Techno",
        "tempo_range": {"min": 120, "max": 130, "feel": "hypnotic, patient"},
        "rhythmic_conventions": ["four-on-the-floor kick", "offbeat hats", "sparse percussion"],
        "harmonic_conventions": ["static harmony", "minor tonality", "chord stabs with long reverb"],
        "textural_sonic_conventions": ["haze", "reverb-drenched", "filter movement"],
        "arrangement_conventions": ["long builds", "atmospheric breakdowns", "minimal section changes"],
        "spirit": "Hypnotic immersion through repetition and slow change. Good examples sustain a single idea with patience; lazy examples just repeat a loop without evolution.",
        "common_failure_modes": ["no evolution", "static loop without filter movement", "overcrowded mid"],
    }
    validate_genre_profile(profile)  # should not raise


def test_genre_profile_missing_required_field_fails():
    profile = {
        "name": "Dub Techno",
        "tempo_range": {"min": 120, "max": 130, "feel": "hypnotic, patient"},
        # missing rhythmic_conventions, harmonic_conventions, textural_sonic_conventions,
        # arrangement_conventions, spirit, common_failure_modes
    }
    try:
        validate_genre_profile(profile)
        assert False, "should have raised"
    except ValidationError as e:
        assert "rhythmic_conventions" in str(e) or "missing" in str(e).lower()


def test_genre_profile_spirit_too_short_fails():
    profile = {
        "name": "Dub Techno",
        "tempo_range": {"min": 120, "max": 130, "feel": "hypnotic, patient"},
        "rhythmic_conventions": ["four-on-the-floor kick"],
        "harmonic_conventions": ["static harmony"],
        "textural_sonic_conventions": ["haze"],
        "arrangement_conventions": ["long builds"],
        "spirit": "Hypnotic.",  # too short — no depth
        "common_failure_modes": ["no evolution"],
    }
    try:
        validate_genre_profile(profile)
        assert False, "should have raised — spirit too short"
    except ValidationError as e:
        assert "spirit" in str(e).lower()


def test_valid_theory_document_passes():
    from electronic_music_mentor.substrates.validator import validate_theory_document
    doc = {
        "topic": "Voice-leading",
        "summary": "Principles of smooth voice-leading between chords, focused on electronic music contexts where bass often carries the harmony.",
        "principles": ["minimize movement between voices", "avoid parallel fifths in classical contexts", "in electronic music, bass movement can be wide if it carries the harmony"],
        "electronic_music_notes": "When bass is the harmony, voice-leading rules relax — wide bass leaps are idiomatic.",
        "examples": ["i-VI-III-VII progression in minor with static-bass voice-leading"],
    }
    validate_theory_document(doc)  # should not raise


def test_theory_document_missing_principles_fails():
    from electronic_music_mentor.substrates.validator import validate_theory_document
    doc = {
        "topic": "Voice-leading",
        "summary": "Some summary here.",
        # missing principles, electronic_music_notes, examples
    }
    try:
        validate_theory_document(doc)
        assert False, "should have raised"
    except ValidationError as e:
        assert "principles" in str(e).lower() or "missing" in str(e).lower()