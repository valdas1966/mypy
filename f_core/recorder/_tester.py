import pytest
from f_core.recorder import Recorder


@pytest.fixture
def active() -> Recorder:
    """
    ========================================================================
     Create an active Recorder.
    ========================================================================
    """
    return Recorder.Factory.active()


@pytest.fixture
def inactive() -> Recorder:
    """
    ========================================================================
     Create an inactive Recorder.
    ========================================================================
    """
    return Recorder.Factory.inactive()


def test_active_records(active: Recorder) -> None:
    """
    ========================================================================
     Test that an active Recorder records events.
    ========================================================================
    """
    active.record({'type': 'test', 'value': 1})
    active.record({'type': 'test', 'value': 2})
    assert len(active) == 2
    assert active.events[0] == {'type': 'test', 'value': 1}
    assert active.events[1] == {'type': 'test', 'value': 2}


def test_inactive_ignores(inactive: Recorder) -> None:
    """
    ========================================================================
     Test that an inactive Recorder ignores events.
    ========================================================================
    """
    inactive.record({'type': 'test', 'value': 1})
    assert len(inactive) == 0
    assert inactive.events == []


def test_bool(active: Recorder, inactive: Recorder) -> None:
    """
    ========================================================================
     Test the __bool__() method.
    ========================================================================
    """
    assert bool(active)
    assert not bool(inactive)


def test_clear(active: Recorder) -> None:
    """
    ========================================================================
     Test the clear() method.
    ========================================================================
    """
    active.record({'type': 'test'})
    active.record({'type': 'test'})
    assert len(active) == 2
    active.clear()
    assert len(active) == 0


def test_events_returns_copy(active: Recorder) -> None:
    """
    ========================================================================
     Test that events property returns a copy (not reference).
    ========================================================================
    """
    active.record({'type': 'test'})
    events = active.events
    events.append({'type': 'fake'})
    assert len(active) == 1


def test_is_active_setter() -> None:
    """
    ========================================================================
     Test the is_active setter.
    ========================================================================
    """
    recorder = Recorder(is_active=False)
    recorder.record({'type': 'ignored'})
    assert len(recorder) == 0
    recorder.is_active = True
    recorder.record({'type': 'recorded'})
    assert len(recorder) == 1


def test_to_dataframe(active: Recorder) -> None:
    """
    ========================================================================
     Test the to_dataframe() method.
    ========================================================================
    """
    active.record({'type': 'a', 'value': 1})
    active.record({'type': 'b', 'value': 2})
    df = active.to_dataframe()
    assert len(df) == 2
    assert list(df.columns) == ['type', 'value']
