import pytest

from f_hs.heuristic.i_0_base import CacheEntry, HBase
from f_hs.state.i_0_base.main import StateBase


def test_call_raises() -> None:
    """
    ========================================================================
     HBase.__call__ raises NotImplementedError by default.
    ========================================================================
    """
    h = HBase.Factory.base()
    with pytest.raises(NotImplementedError):
        h(StateBase[str](key='A'))


def test_is_perfect_default_false() -> None:
    """
    ========================================================================
     HBase.is_perfect defaults to False.
    ========================================================================
    """
    h = HBase.Factory.base()
    assert h.is_perfect(StateBase[str](key='A')) is False


def test_suffix_next_default_none() -> None:
    """
    ========================================================================
     HBase.suffix_next defaults to None.
    ========================================================================
    """
    h = HBase.Factory.base()
    assert h.suffix_next(StateBase[str](key='A')) is None


def test_is_bounded_default_false() -> None:
    """
    ========================================================================
     HBase.is_bounded defaults to False — only HBounded
     subclasses override to True on strictly-tightening bounds.
    ========================================================================
    """
    h = HBase.Factory.base()
    assert h.is_bounded(StateBase[str](key='A')) is False


def test_cache_entry_frozen() -> None:
    """
    ========================================================================
     CacheEntry is frozen — mutation after construction raises.
    ========================================================================
    """
    e = HBase.Factory.entry_pre_goal()
    assert e.h_perfect == 1.0
    assert e.suffix_next.key == 'C'
    with pytest.raises(Exception):
        e.h_perfect = 99.0
