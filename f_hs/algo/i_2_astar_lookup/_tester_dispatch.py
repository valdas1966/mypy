import pytest

from f_hs.algo.i_1_astar import AStar
from f_hs.heuristic.i_0_base._cache_entry import CacheEntry
from f_hs.heuristic.i_1_bounded.main import HBounded
from f_hs.heuristic.i_1_callable.main import HCallable
from f_hs.heuristic.i_1_cached.main import HCached
from f_hs.problem import ProblemSPP
from f_hs.state.i_0_base.main import StateBase


def test_simple_astar_rejects_hcached() -> None:
    """
    ========================================================================
     Simple AStar rejects HCached `h` with a TypeError that
     redirects to AStarLookup. Silently accepting would be a
     correctness trap (no early exit, no suffix stitch, no
     admissibility guard).
    ========================================================================
    """
    a = StateBase[str](key='A')
    cache = {a: CacheEntry(h_perfect=0, suffix_next=None)}
    h = HCached(base=HCallable(fn=lambda s: 0),
                cache=cache, goal=a)
    with pytest.raises(TypeError, match='AStarLookup'):
        AStar(problem=ProblemSPP.Factory.graph_start_is_goal(),
              h=h)


def test_simple_astar_rejects_hbounded() -> None:
    """
    ========================================================================
     Simple AStar rejects HBounded `h` — redirects to AStarLookup
     (where propagate_pathmax and is_bounded flag live).
    ========================================================================
    """
    h = HBounded(base=HCallable(fn=lambda s: 0), bounds={})
    with pytest.raises(TypeError, match='AStarLookup'):
        AStar(problem=ProblemSPP.Factory.graph_abc(), h=h)


def test_simple_astar_accepts_search_state() -> None:
    """
    ========================================================================
     Simple AStar accepts `search_state` natively — it's an
     AlgoSPP capability, not a Pro feature. No dispatch, no
     class promotion.
    ========================================================================
    """
    from f_hs.algo.i_0_base._search_state import SearchStateSPP
    from f_hs.frontier.i_1_priority.main import FrontierPriority
    seed = SearchStateSPP[StateBase[str]](
        frontier=FrontierPriority[StateBase[str]]())
    algo = AStar(problem=ProblemSPP.Factory.graph_abc(),
                 h=lambda s: 0, search_state=seed)
    assert type(algo) is AStar
    assert algo._frontier_dirty is True
    assert algo.search_state is seed
