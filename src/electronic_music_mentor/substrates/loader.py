"""Loader for knowledge-base substrate files.

Parses markdown files with YAML front-matter into dicts, runs the
appropriate validator, and returns the parsed content (front-matter
fields plus the prose body).
"""

import re
from pathlib import Path

import yaml

from .validator import validate_theory_document, ValidationError


class LoadError(Exception):
    """Raised when a substrate file cannot be loaded or is invalid."""


FRONT_MATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)$", re.DOTALL)


def load_theory_document(path: Path) -> dict:
    """Load a theory document from a markdown file with YAML front-matter.

    Returns a dict with the front-matter fields plus a 'body' key containing
    the prose content (everything after the front-matter).

    Raises LoadError if the file has no front-matter, fails to parse, or
    fails validation.
    """
    path = Path(path)
    text = path.read_text()

    match = FRONT_MATTER_RE.match(text)
    if not match:
        raise LoadError(
            f"Could not find YAML front-matter in {path}. "
            "Theory documents must start with '---' delimiters."
        )

    yaml_text, body = match.groups()
    try:
        front_matter = yaml.safe_load(yaml_text)
    except yaml.YAMLError as e:
        raise LoadError(f"Failed to parse YAML front-matter in {path}: {e}") from e

    if not isinstance(front_matter, dict):
        raise LoadError(f"Front-matter in {path} is not a dict (got {type(front_matter).__name__})")

    try:
        validate_theory_document(front_matter)
    except ValidationError as e:
        raise LoadError(f"Validation failed for {path}: {e}") from e

    front_matter["body"] = body
    return front_matter