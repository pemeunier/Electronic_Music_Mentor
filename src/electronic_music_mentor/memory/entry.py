"""Observation entry and lifecycle states for the memory store."""

from dataclasses import dataclass, field
from enum import Enum


class LifecycleState(str, Enum):
    NOTICED_ONCE = "noticed-once"
    PATTERN = "pattern"
    FORMER_HABIT = "former-habit"


@dataclass
class ObservationEntry:
    id: str
    content: str
    domains: list[str]
    state: LifecycleState
    first_noticed_session: int
    last_seen_session: int
    occurrences: int
    corrected: bool
    source: str  # "declared" (mentor noticed) or "user-stated"