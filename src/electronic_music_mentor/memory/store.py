"""MemoryStore: reads, writes, and manages the lifecycle of observations."""

import json
import re
from pathlib import Path

from .entry import ObservationEntry, LifecycleState


def _slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")[:60]


class MemoryStore:
    """Stores observations about the user as a producer.

    Owns the lifecycle: noticed-once -> pattern -> former-habit.
    Corrected observations are excluded from recall unless they recur
    despite the correction (which clears the correction and re-raises).
    """

    def __init__(self, path: Path):
        self.path = Path(path)
        self.entries: list[ObservationEntry] = []
        self.load()

    def declare(
        self,
        content: str,
        domains: list[str],
        session: int,
        source: str,
    ) -> ObservationEntry:
        existing = self._find_by_content(content)
        if existing is None:
            entry = ObservationEntry(
                id=_slugify(content),
                content=content,
                domains=domains,
                state=LifecycleState.NOTICED_ONCE,
                first_noticed_session=session,
                last_seen_session=session,
                occurrences=1,
                corrected=False,
                source=source,
            )
            self.entries.append(entry)
            return entry

        # Recurrence
        existing.occurrences += 1
        existing.last_seen_session = session
        existing.corrected = False  # re-raise clears correction
        if existing.state == LifecycleState.NOTICED_ONCE:
            existing.state = LifecycleState.PATTERN
        elif existing.state == LifecycleState.FORMER_HABIT:
            existing.state = LifecycleState.PATTERN  # relapse -> pattern
        return existing

    def correct(self, content: str) -> bool:
        existing = self._find_by_content(content)
        if existing is None:
            return False
        existing.corrected = True
        return True

    def recall(self, domains: list[str]) -> list[ObservationEntry]:
        domain_set = set(domains)
        return [
            e for e in self.entries
            if not e.corrected and domain_set.intersection(e.domains)
        ]

    def decay(self, current_session: int, absence_threshold: int) -> list[ObservationEntry]:
        """Age down patterns not seen in `absence_threshold` sessions to former-habit.

        Returns the entries that were decayed.
        """
        decayed = []
        for entry in self.entries:
            if entry.state == LifecycleState.PATTERN:
                sessions_absent = current_session - entry.last_seen_session
                if sessions_absent >= absence_threshold:
                    entry.state = LifecycleState.FORMER_HABIT
                    decayed.append(entry)
        return decayed

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        data = [e.__dict__ for e in self.entries]
        for d in data:
            d["state"] = d["state"].value
        self.path.write_text(json.dumps(data, indent=2))

    def load(self) -> None:
        if not self.path.exists():
            self.entries = []
            return
        data = json.loads(self.path.read_text())
        self.entries = []
        for d in data:
            d["state"] = LifecycleState(d["state"])
            self.entries.append(ObservationEntry(**d))

    def _find_by_content(self, content: str) -> ObservationEntry | None:
        for entry in self.entries:
            if entry.content == content:
                return entry
        return None