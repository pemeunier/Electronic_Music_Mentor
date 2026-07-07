"""EscapeHatchTracker: tracks mentor-path vs. tool-path invocation ratio."""

import json
from collections import deque
from pathlib import Path


class EscapeHatchTracker:
    """Records tool-path and mentor-path invocations and computes the ratio.

    Used by the orchestrator logic to decide whether to name the dependency
    (guard for risk 3). A sliding window keeps only recent invocations so
    the ratio reflects current behavior, not all-time history.
    """

    def __init__(self, path: Path, window: int = 10):
        self.path = Path(path)
        self.window = window
        self.invocations: deque[str] = deque(maxlen=window)
        self.load()

    def record(self, path_type: str) -> None:
        """Record an invocation. path_type is 'tool' or 'mentor'."""
        if path_type not in ("tool", "mentor"):
            raise ValueError(f"path_type must be 'tool' or 'mentor', got {path_type}")
        self.invocations.append(path_type)
        self.save()

    def ratio(self) -> float:
        if not self.invocations:
            return 0.0
        tool_count = sum(1 for p in self.invocations if p == "tool")
        return tool_count / len(self.invocations)

    def total_in_window(self) -> int:
        return len(self.invocations)

    def should_name_dependency(self, threshold: float = 0.7) -> bool:
        return self.ratio() >= threshold

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(list(self.invocations)))

    def load(self) -> None:
        if not self.path.exists():
            self.invocations = deque(maxlen=self.window)
            return
        data = json.loads(self.path.read_text())
        self.invocations = deque(data, maxlen=self.window)