"""Validators for knowledge-base substrate files.

These enforce that genre-profiles and theory documents have the required
fields and adequate content depth. Used when building knowledge content
and when skills load substrates.
"""


class ValidationError(Exception):
    """Raised when a substrate file fails validation."""


GENRE_PROFILE_REQUIRED_FIELDS = [
    "name",
    "tempo_range",
    "rhythmic_conventions",
    "harmonic_conventions",
    "textural_sonic_conventions",
    "arrangement_conventions",
    "spirit",
    "common_failure_modes",
]

THEORY_DOCUMENT_REQUIRED_FIELDS = [
    "topic",
    "summary",
    "principles",
    "electronic_music_notes",
    "examples",
]

MIN_SPIRIT_LENGTH = 80  # characters — the spirit field needs real depth


def validate_genre_profile(profile: dict) -> None:
    """Validate a genre-profile dict. Raises ValidationError if invalid."""
    missing = [f for f in GENRE_PROFILE_REQUIRED_FIELDS if f not in profile]
    if missing:
        raise ValidationError(f"Genre profile missing required fields: {missing}")

    if len(profile["spirit"]) < MIN_SPIRIT_LENGTH:
        raise ValidationError(
            f"Genre profile 'spirit' field too short ({len(profile['spirit'])} chars, "
            f"need at least {MIN_SPIRIT_LENGTH}). The spirit field needs real depth."
        )

    if not isinstance(profile["tempo_range"], dict) or "min" not in profile["tempo_range"] or "max" not in profile["tempo_range"]:
        raise ValidationError("Genre profile 'tempo_range' must be a dict with 'min' and 'max' keys")


def validate_theory_document(doc: dict) -> None:
    """Validate a theory-document dict. Raises ValidationError if invalid."""
    missing = [f for f in THEORY_DOCUMENT_REQUIRED_FIELDS if f not in doc]
    if missing:
        raise ValidationError(f"Theory document missing required fields: {missing}")

    if not isinstance(doc["principles"], list) or len(doc["principles"]) < 1:
        raise ValidationError("Theory document 'principles' must be a non-empty list")

    if not isinstance(doc["examples"], list) or len(doc["examples"]) < 1:
        raise ValidationError("Theory document 'examples' must be a non-empty list")