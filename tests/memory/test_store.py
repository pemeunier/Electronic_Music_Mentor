import json
from pathlib import Path

from electronic_music_mentor.memory.store import MemoryStore
from electronic_music_mentor.memory.entry import LifecycleState


def test_declare_new_observation_starts_as_noticed_once(tmp_path):
    store = MemoryStore(tmp_path / "memory.json")
    entry = store.declare(
        content="tends to overcrowd the low-mid",
        domains=["arrangement", "sound-design"],
        session=1,
        source="declared",
    )
    assert entry.state == LifecycleState.NOTICED_ONCE
    assert entry.occurrences == 1
    assert entry.first_noticed_session == 1
    assert entry.last_seen_session == 1
    assert entry.corrected is False


def test_declare_recurrence_graduates_to_pattern(tmp_path):
    store = MemoryStore(tmp_path / "memory.json")
    store.declare(content="tends to overcrowd the low-mid", domains=["arrangement"], session=1, source="declared")
    entry = store.declare(content="tends to overcrowd the low-mid", domains=["arrangement"], session=2, source="declared")
    assert entry.state == LifecycleState.PATTERN
    assert entry.occurrences == 2
    assert entry.last_seen_session == 2


def test_recall_returns_observations_for_domain(tmp_path):
    store = MemoryStore(tmp_path / "memory.json")
    store.declare(content="tends to overcrowd the low-mid", domains=["arrangement", "sound-design"], session=1, source="declared")
    store.declare(content="melodies start on the same beat every time", domains=["melody"], session=1, source="declared")
    recalled = store.recall(domains=["arrangement"])
    assert len(recalled) == 1
    assert "low-mid" in recalled[0].content


def test_correct_marks_observation_and_excludes_from_recall(tmp_path):
    store = MemoryStore(tmp_path / "memory.json")
    store.declare(content="tends to overcrowd the low-mid", domains=["arrangement"], session=1, source="declared")
    store.correct("tends to overcrowd the low-mid")
    # Corrected observations are excluded from recall unless they recur despite correction
    recalled = store.recall(domains=["arrangement"])
    assert len(recalled) == 0


def test_corrected_observation_recurrs_despite_correction_re_raises(tmp_path):
    store = MemoryStore(tmp_path / "memory.json")
    store.declare(content="tends to overcrowd the low-mid", domains=["arrangement"], session=1, source="declared")
    store.correct("tends to overcrowd the low-mid")
    # Recurs despite correction
    entry = store.declare(content="tends to overcrowd the low-mid", domains=["arrangement"], session=2, source="declared")
    assert entry.corrected is False  # correction cleared by re-raise
    assert entry.state == LifecycleState.PATTERN
    # Now recallable again
    recalled = store.recall(domains=["arrangement"])
    assert len(recalled) == 1


def test_persist_and_reload(tmp_path):
    path = tmp_path / "memory.json"
    store = MemoryStore(path)
    store.declare(content="tends to overcrowd the low-mid", domains=["arrangement"], session=1, source="declared")
    store.save()
    store2 = MemoryStore(path)
    store2.load()
    recalled = store2.recall(domains=["arrangement"])
    assert len(recalled) == 1


def test_decay_ages_pattern_to_former_habit_after_threshold(tmp_path):
    store = MemoryStore(tmp_path / "memory.json")
    # Sessions 1 and 2 establish a pattern
    store.declare(content="tends to overcrowd the low-mid", domains=["arrangement"], session=1, source="declared")
    store.declare(content="tends to overcrowd the low-mid", domains=["arrangement"], session=2, source="declared")
    # Session 6 is 4 sessions later (threshold = 3)
    decayed = store.decay(current_session=6, absence_threshold=3)
    assert len(decayed) == 1
    assert decayed[0].state == LifecycleState.FORMER_HABIT


def test_decay_does_not_age_recent_patterns(tmp_path):
    store = MemoryStore(tmp_path / "memory.json")
    store.declare(content="tends to overcrowd the low-mid", domains=["arrangement"], session=1, source="declared")
    store.declare(content="tends to overcrowd the low-mid", domains=["arrangement"], session=2, source="declared")
    # Session 3 is only 1 session later
    decayed = store.decay(current_session=3, absence_threshold=3)
    assert len(decayed) == 0


def test_decay_does_not_age_noticed_once(tmp_path):
    store = MemoryStore(tmp_path / "memory.json")
    store.declare(content="tends to overcrowd the low-mid", domains=["arrangement"], session=1, source="declared")
    decayed = store.decay(current_session=10, absence_threshold=3)
    assert len(decayed) == 0  # noticed-once doesn't decay (it just isn't recalled strongly)


def test_former_habit_relapse_returns_to_pattern_on_declare(tmp_path):
    store = MemoryStore(tmp_path / "memory.json")
    store.declare(content="tends to overcrowd the low-mid", domains=["arrangement"], session=1, source="declared")
    store.declare(content="tends to overcrowd the low-mid", domains=["arrangement"], session=2, source="declared")
    store.decay(current_session=6, absence_threshold=3)
    # Relapse at session 7
    entry = store.declare(content="tends to overcrowd the low-mid", domains=["arrangement"], session=7, source="declared")
    assert entry.state == LifecycleState.PATTERN