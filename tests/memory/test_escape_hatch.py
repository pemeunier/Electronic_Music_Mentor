from electronic_music_mentor.memory.escape_hatch import EscapeHatchTracker


def test_initial_ratio_is_balanced(tmp_path):
    tracker = EscapeHatchTracker(tmp_path / "escape_hatch.json")
    assert tracker.ratio() == 0.0  # no invocations yet


def test_record_tool_path_increments_tool_count(tmp_path):
    tracker = EscapeHatchTracker(tmp_path / "escape_hatch.json")
    tracker.record("tool")
    tracker.record("tool")
    tracker.record("mentor")
    assert tracker.ratio() > 0.6  # 2/3 tool path


def test_threshold_triggers_when_ratio_above_70_percent(tmp_path):
    tracker = EscapeHatchTracker(tmp_path / "escape_hatch.json")
    # 4 tool, 1 mentor = 0.8
    for _ in range(4):
        tracker.record("tool")
    tracker.record("mentor")
    assert tracker.should_name_dependency(threshold=0.7) is True


def test_threshold_does_not_trigger_below_70_percent(tmp_path):
    tracker = EscapeHatchTracker(tmp_path / "escape_hatch.json")
    tracker.record("tool")
    tracker.record("mentor")
    tracker.record("mentor")
    assert tracker.should_name_dependency(threshold=0.7) is False


def test_persist_and_reload(tmp_path):
    path = tmp_path / "escape_hatch.json"
    tracker = EscapeHatchTracker(path)
    tracker.record("tool")
    tracker.save()
    tracker2 = EscapeHatchTracker(path)
    assert tracker2.ratio() > 0.0


def test_window_only_counts_last_n_sessions(tmp_path):
    tracker = EscapeHatchTracker(tmp_path / "escape_hatch.json", window=3)
    # 5 tool invocations, but only last 3 counted
    for _ in range(5):
        tracker.record("tool")
    assert tracker.total_in_window() == 3