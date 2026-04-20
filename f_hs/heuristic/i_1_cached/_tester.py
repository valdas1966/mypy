from f_hs.heuristic.i_0_base._cache_entry import CacheEntry
from f_hs.heuristic.i_1_callable.main import HCallable
from f_hs.heuristic.i_1_cached import HCached
from f_hs.state.i_0_base.main import StateBase


def test_call_hit_returns_h_perfect() -> None:
    """
    ========================================================================
     HCached.__call__ returns the cached h_perfect on hit.
    ========================================================================
    """
    h = HCached.Factory.graph_abc_full()
    assert h(StateBase[str](key='A')) == 2.0
    assert h(StateBase[str](key='B')) == 1.0
    assert h(StateBase[str](key='C')) == 0.0


def test_call_miss_delegates_to_base() -> None:
    """
    ========================================================================
     On a cache miss, HCached delegates to self._base. With the
     partial factory, only A misses the cache — it takes the
     base callable's value (2.0). B and C hit the cache and
     return 1.0 / 0.0 (not the sentinel 99.0).
    ========================================================================
    """
    h = HCached.Factory.graph_abc_partial()
    assert h(StateBase[str](key='A')) == 2.0
    assert h(StateBase[str](key='B')) == 1.0
    assert h(StateBase[str](key='C')) == 0.0


def test_is_perfect_only_on_hits() -> None:
    """
    ========================================================================
     is_perfect is True iff the state is in the cache.
    ========================================================================
    """
    h = HCached.Factory.graph_abc_partial()
    assert h.is_perfect(StateBase[str](key='A')) is False
    assert h.is_perfect(StateBase[str](key='B')) is True
    assert h.is_perfect(StateBase[str](key='C')) is True


def test_suffix_next_traces_path() -> None:
    """
    ========================================================================
     suffix_next walks the cached optimal path; the goal entry
     points to None (end of suffix).
    ========================================================================
    """
    h = HCached.Factory.graph_abc_full()
    assert h.suffix_next(StateBase[str](key='A')).key == 'B'
    assert h.suffix_next(StateBase[str](key='B')).key == 'C'
    assert h.suffix_next(StateBase[str](key='C')) is None


def test_suffix_next_miss_is_none() -> None:
    """
    ========================================================================
     On a cache miss, suffix_next returns None (no path info).
    ========================================================================
    """
    h = HCached.Factory.graph_abc_partial()
    assert h.suffix_next(StateBase[str](key='A')) is None


def test_goal_property() -> None:
    """
    ========================================================================
     HCached.goal exposes the goal the cache was harvested for.
    ========================================================================
    """
    h = HCached.Factory.graph_abc_full()
    assert h.goal.key == 'C'


def test_constructor_takes_defensive_copy() -> None:
    """
    ========================================================================
     Mutating the source dict after construction does not affect
     HCached's view — the constructor takes a shallow copy. Pins
     the static-cache decision.
    ========================================================================
    """
    c = StateBase[str](key='C')
    src = {c: CacheEntry(h_perfect=0.0, suffix_next=None)}
    h = HCached(base=HCallable(fn=lambda s: 5.0),
                cache=src, goal=c)
    src.clear()
    assert h.is_perfect(c) is True
    assert h(c) == 0.0
