from electronic_music_mentor.memory.entry import (
    ObservationEntry,
    LifecycleState,
)


def test_observation_entry_noticed_once():
    entry = ObservationEntry(
        id="low-mid-overcrowd",
        content="tends to overcrowd the low-mid",
        domains=["arrangement", "sound-design"],
        state=LifecycleState.NOTICED_ONCE,
        first_noticed_session=1,
        last_seen_session=1,
        occurrences=1,
        corrected=False,
        source="declared",
    )
    assert entry.id == "low-mid-overcrowd"
    assert entry.state == LifecycleState.NOTICED_ONCE
    assert entry.domains == ["arrangement", "sound-design"]
    assert entry.occurrences == 1
    assert entry.corrected is False
    assert entry.source == "declared"


def test_lifecycle_states_are_distinct():
    assert LifecycleState.NOTICED_ONCE != LifecycleState.PATTERN
    assert LifecycleState.PATTERN != LifecycleState.FORMER_HABIT
    assert LifecycleState.NOTICED_ONCE != LifecycleState.FORMER_HABIT