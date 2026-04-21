import pytest

from f_ds.grids.cell.i_1_map import CellMap

from f_hs.algo.i_1_astar import AStar
from f_hs.algo.i_2_astar_lookup import AStarLookup
from f_hs.algo.i_2_astar_lookup._utils import normalize
from f_hs.heuristic.i_0_base._cache_entry import CacheEntry
from f_hs.heuristic.i_1_callable.main import HCallable
from f_hs.heuristic.i_1_cached.main import HCached
from f_hs.problem import ProblemSPP
from f_hs.problem.i_1_grid import ProblemGrid
from f_hs.state.i_0_base.main import StateBase
from f_hs.state.i_1_cell.main import StateCell


def test_cache_hit_early_term() -> None:
    """
    ========================================================================
     With HCached covering the start state, AStarLookup pops A,
     fires _early_exit (is_perfect(A) is True), and returns
     cost = g(A) + h_perfect(A) = 0 + 2 = 2 without expanding
     B or C. search_state reports cache_hit=A; goal_reached
     stays None. reconstruct_path stitches: A -> B -> C.
    ========================================================================
    """
    algo = AStarLookup.Factory.graph_abc_cached_at_start()
    sol = algo.run()
    assert bool(sol) is True
    assert sol.cost == 2
    s = algo.search_state
    assert s.cache_hit is not None and s.cache_hit.key == 'A'
    assert s.goal_reached is None
    assert s.closed == set()
    path = algo.reconstruct_path()
    assert [p.key for p in path] == ['A', 'B', 'C']


def test_to_cache_round_trip() -> None:
    """
    ========================================================================
     Run AStarLookup to completion on graph_abc with a trivial
     goal-only cache; harvest via to_cache(); feed into a fresh
     AStar. The fresh run terminates via cache_hit on the start.
    ========================================================================
    """
    problem = ProblemSPP.Factory.graph_abc()
    goal = problem.goals[0]
    first = AStarLookup(problem=problem,
                     h=HCached(base=HCallable(fn=lambda s: 0),
                               cache={goal: CacheEntry(
                                   h_perfect=0,
                                   suffix_next=None)},
                               goal=goal))
    sol1 = first.run()
    assert sol1.cost == 2
    cache = first.to_cache()
    assert len(cache) == 3
    assert {s.key for s in cache} == {'A', 'B', 'C'}

    problem2 = ProblemSPP.Factory.graph_abc()
    goal2 = problem2.goals[0]
    h = HCached(base=HCallable(fn=lambda s: 0),
                cache=cache, goal=goal2)
    second = AStarLookup(problem=problem2, h=h)
    assert isinstance(second, AStarLookup)
    sol2 = second.run()
    assert sol2.cost == 2
    assert second.search_state.cache_hit is not None
    assert second.search_state.cache_hit.key == 'A'
    assert second.search_state.closed == set()


def test_to_cache_after_cache_hit() -> None:
    """
    ========================================================================
     Non-degenerate harvest via cache_hit termination on B
     (cache covers {B, C}). to_cache() emits A (newly-discovered
     prefix) + B (terminal with suffix_next pointing to C from
     existing cache).
    ========================================================================
    """
    algo = AStarLookup.Factory.graph_abc_cached_at_b()
    algo.run()
    assert algo.search_state.cache_hit is not None
    assert algo.search_state.cache_hit.key == 'B'

    harvested = algo.to_cache()
    by_key = {s.key: e for s, e in harvested.items()}
    assert set(by_key) == {'A', 'B'}
    assert by_key['A'].h_perfect == 2
    assert by_key['A'].suffix_next.key == 'B'
    assert by_key['B'].h_perfect == 1
    assert by_key['B'].suffix_next.key == 'C'


def test_init_raises_on_goal_mismatch() -> None:
    """
    ========================================================================
     HCached whose goal is NOT in problem.goals fails loud at
     __init__. Cache harvested against the wrong goal silently
     violates admissibility.
    ========================================================================
    """
    z = StateBase[str](key='Z')
    bad_cache = {z: CacheEntry(h_perfect=0, suffix_next=None)}
    with pytest.raises(ValueError, match='not a goal'):
        AStarLookup(problem=ProblemSPP.Factory.graph_abc(),
                    cache=bad_cache, goal=z)


def test_is_cached_tiebreak_picks_cached_over_uncached() -> None:
    """
    ========================================================================
     Priority = (f, -g, cache_rank, state). cache_rank prefers
     cached (0) over uncached (1) on (f, -g) tie. Pins the
     tiebreak is load-bearing — not just noop inherited from
     state-order.
    ========================================================================
    """
    problem = ProblemSPP.Factory.graph_abc()
    a = StateBase[str](key='A')
    c = StateBase[str](key='C')
    cache = {c: CacheEntry(h_perfect=2, suffix_next=None)}
    h = HCached(base=HCallable(fn=lambda s: 2),
                cache=cache, goal=c)
    algo = AStarLookup(problem=problem, h=h)

    algo._search.g[a] = 2
    algo._search.g[c] = 2
    prio_a = algo._priority(state=a)
    prio_c = algo._priority(state=c)
    assert prio_a[0] == prio_c[0] == 4     # f
    assert prio_a[1] == prio_c[1] == -2    # -g
    assert prio_c[2] == 0 and prio_a[2] == 1
    assert prio_c < prio_a
    # State tiebreak alone would pick A (< C); cache_rank flips it.
    assert prio_a[3] < prio_c[3]


def test_recording_is_cached_marker_on_graph_abc_cached_at_b(
        ) -> None:
    """
    ========================================================================
     HCached covering {B, C}. AStarLookup pops A (not cached),
     expands to B, pops B and early-exits. Pins is_cached flag
     on push/pop of cached states; absent on uncached events.
    ========================================================================
    """
    algo = AStarLookup.Factory.graph_abc_cached_at_b()
    algo._recorder.is_active = True
    sol = algo.run()
    assert sol.cost == 2

    actual = [normalize(e) for e in algo.recorder.events]
    expected = [
        {'type': 'push', 'state': 'A', 'g': 0, 'parent': None, 'h': 2, 'f': 2},
        {'type': 'pop',  'state': 'A', 'g': 0, 'h': 2, 'f': 2},
        {'type': 'push', 'state': 'B', 'g': 1, 'parent': 'A', 'h': 1, 'f': 2, 'is_cached': True},
        {'type': 'pop',  'state': 'B', 'g': 1, 'h': 1, 'f': 2, 'is_cached': True},
    ]
    assert actual == expected

    cached_pops = [e for e in actual
                   if e['type'] == 'pop' and e.get('is_cached')]
    assert len(cached_pops) == 1
    assert cached_pops[0]['state'] == 'B'
    for e in actual:
        if e['state'] != 'B':
            assert 'is_cached' not in e
    assert algo.search_state.cache_hit is not None
    assert algo.search_state.cache_hit.key == 'B'


def test_recording_on_grid_4x4_obstacle_with_cached_optimal_suffix(
        ) -> None:
    """
    ========================================================================
     HCached covering the optimal path from (0,1) to (0,3).
     8 events vs 22 un-cached. Pins is_cached visibility +
     suffix stitching + push-but-never-popped cached state.
    ========================================================================
    """
    problem = ProblemGrid.Factory.grid_4x4_obstacle()
    goal = problem.goal

    def sc(r: int, c: int) -> StateCell:
        return StateCell(key=CellMap(row=r, col=c))

    p01, p11, p21, p22 = sc(0, 1), sc(1, 1), sc(2, 1), sc(2, 2)
    p23, p13, p03 = sc(2, 3), sc(1, 3), sc(0, 3)

    cache = {
        p01: CacheEntry(h_perfect=6, suffix_next=p11),
        p11: CacheEntry(h_perfect=5, suffix_next=p21),
        p21: CacheEntry(h_perfect=4, suffix_next=p22),
        p22: CacheEntry(h_perfect=3, suffix_next=p23),
        p23: CacheEntry(h_perfect=2, suffix_next=p13),
        p13: CacheEntry(h_perfect=1, suffix_next=p03),
        p03: CacheEntry(h_perfect=0, suffix_next=None),
    }
    h = HCached(
        base=HCallable(fn=lambda s: s.distance(goal)),
        cache=cache,
        goal=p03,
    )
    algo = AStarLookup(problem=problem, h=h, is_recording=True)
    assert isinstance(algo, AStarLookup)

    sol = algo.run()
    assert sol.cost == 7

    actual = [normalize(e) for e in algo.recorder.events]
    expected = [
        {'type': 'push', 'state': (0, 0), 'g': 0, 'parent': None, 'h': 3, 'f': 3},
        {'type': 'pop',  'state': (0, 0), 'g': 0, 'h': 3, 'f': 3},
        {'type': 'push', 'state': (0, 1), 'g': 1, 'parent': (0, 0), 'h': 6, 'f': 7, 'is_cached': True},
        {'type': 'push', 'state': (1, 0), 'g': 1, 'parent': (0, 0), 'h': 4, 'f': 5},
        {'type': 'pop',  'state': (1, 0), 'g': 1, 'h': 4, 'f': 5},
        {'type': 'push', 'state': (1, 1), 'g': 2, 'parent': (1, 0), 'h': 5, 'f': 7, 'is_cached': True},
        {'type': 'push', 'state': (2, 0), 'g': 2, 'parent': (1, 0), 'h': 5, 'f': 7},
        {'type': 'pop',  'state': (1, 1), 'g': 2, 'h': 5, 'f': 7, 'is_cached': True},
    ]
    assert actual == expected
    assert len(actual) == 8

    cached_pushes = [e for e in actual
                     if e['type'] == 'push' and e.get('is_cached')]
    cached_pops = [e for e in actual
                   if e['type'] == 'pop' and e.get('is_cached')]
    assert {e['state'] for e in cached_pushes} == {(0, 1), (1, 1)}
    assert len(cached_pops) == 1
    assert cached_pops[0]['state'] == (1, 1)

    popped_states = {e['state'] for e in actual
                     if e['type'] == 'pop'}
    assert (0, 1) not in popped_states

    for e in actual:
        if e['state'] not in {(0, 1), (1, 1)}:
            assert 'is_cached' not in e

    assert actual[-1]['type'] == 'pop'
    assert actual[-1].get('is_cached') is True
    assert algo.search_state.cache_hit is not None
    assert algo.search_state.cache_hit.rc == (1, 1)
    assert algo.search_state.goal_reached is None

    path = algo.reconstruct_path()
    assert [s.rc for s in path] == [
        (0, 0), (1, 0), (1, 1),
        (2, 1), (2, 2), (2, 3), (1, 3), (0, 3),
    ]
