"""
============================================================================
 AStarLookup tests — merged from the previous split files
 (`_tester_cached.py`, `_tester_bounded.py`, `_tester_pathmax.py`).

 Sections:
   1. HCached lifecycle  (cache-hit early-term, harvest,
                          init guards, tiebreak, recording).
   2. HBounded lifecycle (admissibility + is_bounded
                          recording).
   3. propagate_pathmax  (depth None / 0 / int>0, convergence,
                          wave recording, HBounded
                          precondition).

 Counter pins for AStarLookup on the canonical OOSPP problem
 live in `_tester_counters.py`.
============================================================================
"""

import pytest

from f_ds.grids.cell.i_1_map import CellMap

from f_hs.algo.i_0_oospp.i_1_astar import AStar
from f_hs.algo.i_0_oospp.i_2_astar_lookup import AStarLookup
from f_hs.algo.u_event_normalize import normalize
from f_hs.heuristic.i_0_base._cache_entry import CacheEntry
from f_hs.heuristic.i_1_bounded.main import HBounded
from f_hs.heuristic.i_1_callable.main import HCallable
from f_hs.heuristic.i_1_cached.main import HCached
from f_hs.problem import ProblemSPP
from f_hs.problem.i_1_grid import ProblemGrid
from f_hs.state.i_0_base.main import StateBase
from f_hs.state.i_1_cell.main import StateCell


# ────────────────────────────────────────────────────────────────────────────
#  1. HCached lifecycle
# ────────────────────────────────────────────────────────────────────────────


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
        base=HCallable(fn=lambda s: s.key.distance(goal.key)),
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
    assert algo.search_state.cache_hit.to_tuple() == (1, 1)
    assert algo.search_state.goal_reached is None

    path = algo.reconstruct_path()
    assert [s.to_tuple() for s in path] == [
        (0, 0), (1, 0), (1, 1),
        (2, 1), (2, 2), (2, 3), (1, 3), (0, 3),
    ]


def test_counters_pin_graph_abc_cached_at_start() -> None:
    """
    ========================================================================
     Pin counters under cache-hit early-term at the start
     (graph_abc). Start is perfect-h, so the algo pops it once
     and terminates without expanding successors:
     cnt_push=1 (start only), cnt_pop=1, cnt_decrease=0.
     Canonical-OOSPP counter pins live in `_tester_counters.py`.
    ========================================================================
    """
    algo = AStarLookup.Factory.graph_abc_cached_at_start()
    algo.run()
    counters = {k: v for k, v in algo.counters.items()
                if not k.startswith('mem_')}
    assert counters == {
        'cnt_prop_waves': 0,
        'cnt_prop_attempts': 0,
        'cnt_prop_lifts': 0,
        'cnt_push': 1, 'cnt_pop': 1, 'cnt_decrease': 0,
        'cnt_expanded': 0, 'cnt_generated': 1,
    }


def test_counters_pin_graph_abc_cached_at_b() -> None:
    """
    ========================================================================
     Pin counters under cache-hit early-term mid-search
     (graph_abc). Cache covers {B, C}; A pops, generates B
     (cached), B pops and triggers cache-hit termination. Two
     pops, two pushes, no decreases.
    ========================================================================
    """
    algo = AStarLookup.Factory.graph_abc_cached_at_b()
    algo.run()
    counters = {k: v for k, v in algo.counters.items()
                if not k.startswith('mem_')}
    assert counters == {
        'cnt_prop_waves': 0,
        'cnt_prop_attempts': 0,
        'cnt_prop_lifts': 0,
        'cnt_push': 2, 'cnt_pop': 2, 'cnt_decrease': 0,
        'cnt_expanded': 1, 'cnt_generated': 2,
    }


# ────────────────────────────────────────────────────────────────────────────
#  2. HBounded lifecycle
# ────────────────────────────────────────────────────────────────────────────


def test_astar_with_hbounded_finds_optimal_cost() -> None:
    """
    ========================================================================
     AStar on grid_4x4_obstacle with Manhattan wrapped in
     HBounded — bound (1,0) at h=6 and (2,0) at h=5 (both
     tight). Admissibility preserved (optimal cost 7); bounded
     pop count <= un-bounded baseline.
    ========================================================================
    """
    def sc(r: int, c: int) -> StateCell:
        return StateCell(key=CellMap(row=r, col=c))

    problem_b = ProblemGrid.Factory.grid_4x4_obstacle()
    goal_b = problem_b.goal
    base_algo = AStar(
        problem=problem_b,
        h=lambda s: s.key.distance(goal_b.key),
        is_recording=True,
    )
    base_algo.run()
    base_pops = sum(1 for e in base_algo.recorder.events
                    if e.get('type') == 'pop')

    problem = ProblemGrid.Factory.grid_4x4_obstacle()
    goal = problem.goal
    bounds = {sc(1, 0): 6, sc(2, 0): 5}
    h = HBounded(
        base=HCallable(fn=lambda s: s.key.distance(goal.key)),
        bounds=bounds,
    )
    algo = AStarLookup(problem=problem, h=h, is_recording=True)

    sol = algo.run()
    assert sol.cost == 7

    bounded_pops = sum(1 for e in algo.recorder.events
                       if e.get('type') == 'pop')
    assert bounded_pops <= base_pops


def test_recording_hbounded_tightens_h_on_grid_4x4_obstacle(
        ) -> None:
    """
    ========================================================================
     HBounded bounds (1,0) at h=6 (tight; h*((1,0))=6). (1,0)'s
     bump to f=7 dominates it out of the pop set. Pins
     is_bounded on push-only of a pruned state.
    ========================================================================
    """
    def sc(r: int, c: int) -> StateCell:
        return StateCell(key=CellMap(row=r, col=c))

    problem = ProblemGrid.Factory.grid_4x4_obstacle()
    goal = problem.goal
    bounds = {sc(1, 0): 6}
    h = HBounded(
        base=HCallable(fn=lambda s: s.key.distance(goal.key)),
        bounds=bounds,
    )
    algo = AStarLookup(problem=problem, h=h, is_recording=True)

    sol = algo.run()
    assert sol.cost == 7

    actual = [normalize(e) for e in algo.recorder.events]
    expected = [
        {'type': 'push', 'state': (0, 0), 'g': 0, 'parent': None, 'h': 3, 'f': 3},
        {'type': 'pop',  'state': (0, 0), 'g': 0, 'h': 3, 'f': 3},
        {'type': 'push', 'state': (0, 1), 'g': 1, 'parent': (0, 0), 'h': 2, 'f': 3},
        {'type': 'push', 'state': (1, 0), 'g': 1, 'parent': (0, 0), 'h': 6, 'f': 7, 'is_bounded': True},
        {'type': 'pop',  'state': (0, 1), 'g': 1, 'h': 2, 'f': 3},
        {'type': 'push', 'state': (1, 1), 'g': 2, 'parent': (0, 1), 'h': 3, 'f': 5},
        {'type': 'pop',  'state': (1, 1), 'g': 2, 'h': 3, 'f': 5},
        {'type': 'push', 'state': (2, 1), 'g': 3, 'parent': (1, 1), 'h': 4, 'f': 7},
        {'type': 'pop',  'state': (2, 1), 'g': 3, 'h': 4, 'f': 7},
        {'type': 'push', 'state': (2, 2), 'g': 4, 'parent': (2, 1), 'h': 3, 'f': 7},
        {'type': 'push', 'state': (3, 1), 'g': 4, 'parent': (2, 1), 'h': 5, 'f': 9},
        {'type': 'push', 'state': (2, 0), 'g': 4, 'parent': (2, 1), 'h': 5, 'f': 9},
        {'type': 'pop',  'state': (2, 2), 'g': 4, 'h': 3, 'f': 7},
        {'type': 'push', 'state': (2, 3), 'g': 5, 'parent': (2, 2), 'h': 2, 'f': 7},
        {'type': 'push', 'state': (3, 2), 'g': 5, 'parent': (2, 2), 'h': 4, 'f': 9},
        {'type': 'pop',  'state': (2, 3), 'g': 5, 'h': 2, 'f': 7},
        {'type': 'push', 'state': (1, 3), 'g': 6, 'parent': (2, 3), 'h': 1, 'f': 7},
        {'type': 'push', 'state': (3, 3), 'g': 6, 'parent': (2, 3), 'h': 3, 'f': 9},
        {'type': 'pop',  'state': (1, 3), 'g': 6, 'h': 1, 'f': 7},
        {'type': 'push', 'state': (0, 3), 'g': 7, 'parent': (1, 3), 'h': 0, 'f': 7},
        {'type': 'pop',  'state': (0, 3), 'g': 7, 'h': 0, 'f': 7},
    ]
    assert actual == expected
    assert len(actual) == 21

    popped_states = {e['state'] for e in actual
                     if e['type'] == 'pop'}
    assert (1, 0) not in popped_states
    push_10 = [e for e in actual
               if e['type'] == 'push' and e['state'] == (1, 0)][0]
    assert push_10['h'] == 6 and push_10['f'] == 7
    assert push_10.get('is_bounded') is True
    for e in actual:
        if e['state'] != (1, 0):
            assert 'is_bounded' not in e
    for e in actual:
        assert 'is_cached' not in e


def test_recording_hbounded_popped_state_on_grid_4x4_obstacle(
        ) -> None:
    """
    ========================================================================
     HBounded bounds (1,1) at h=5 (tight). (1,1) IS popped, so
     is_bounded=True appears on BOTH push AND pop.
    ========================================================================
    """
    def sc(r: int, c: int) -> StateCell:
        return StateCell(key=CellMap(row=r, col=c))

    problem = ProblemGrid.Factory.grid_4x4_obstacle()
    goal = problem.goal
    bounds = {sc(1, 1): 5}
    h = HBounded(
        base=HCallable(fn=lambda s: s.key.distance(goal.key)),
        bounds=bounds,
    )
    algo = AStarLookup(problem=problem, h=h, is_recording=True)
    sol = algo.run()
    assert sol.cost == 7

    actual = [normalize(e) for e in algo.recorder.events]
    expected = [
        {'type': 'push', 'state': (0, 0), 'g': 0, 'parent': None, 'h': 3, 'f': 3},
        {'type': 'pop',  'state': (0, 0), 'g': 0, 'h': 3, 'f': 3},
        {'type': 'push', 'state': (0, 1), 'g': 1, 'parent': (0, 0), 'h': 2, 'f': 3},
        {'type': 'push', 'state': (1, 0), 'g': 1, 'parent': (0, 0), 'h': 4, 'f': 5},
        {'type': 'pop',  'state': (0, 1), 'g': 1, 'h': 2, 'f': 3},
        {'type': 'push', 'state': (1, 1), 'g': 2, 'parent': (0, 1), 'h': 5, 'f': 7, 'is_bounded': True},
        {'type': 'pop',  'state': (1, 0), 'g': 1, 'h': 4, 'f': 5},
        {'type': 'push', 'state': (2, 0), 'g': 2, 'parent': (1, 0), 'h': 5, 'f': 7},
        {'type': 'pop',  'state': (1, 1), 'g': 2, 'h': 5, 'f': 7, 'is_bounded': True},
        {'type': 'push', 'state': (2, 1), 'g': 3, 'parent': (1, 1), 'h': 4, 'f': 7},
        {'type': 'pop',  'state': (2, 1), 'g': 3, 'h': 4, 'f': 7},
        {'type': 'push', 'state': (2, 2), 'g': 4, 'parent': (2, 1), 'h': 3, 'f': 7},
        {'type': 'push', 'state': (3, 1), 'g': 4, 'parent': (2, 1), 'h': 5, 'f': 9},
        {'type': 'pop',  'state': (2, 2), 'g': 4, 'h': 3, 'f': 7},
        {'type': 'push', 'state': (2, 3), 'g': 5, 'parent': (2, 2), 'h': 2, 'f': 7},
        {'type': 'push', 'state': (3, 2), 'g': 5, 'parent': (2, 2), 'h': 4, 'f': 9},
        {'type': 'pop',  'state': (2, 3), 'g': 5, 'h': 2, 'f': 7},
        {'type': 'push', 'state': (1, 3), 'g': 6, 'parent': (2, 3), 'h': 1, 'f': 7},
        {'type': 'push', 'state': (3, 3), 'g': 6, 'parent': (2, 3), 'h': 3, 'f': 9},
        {'type': 'pop',  'state': (1, 3), 'g': 6, 'h': 1, 'f': 7},
        {'type': 'push', 'state': (0, 3), 'g': 7, 'parent': (1, 3), 'h': 0, 'f': 7},
        {'type': 'pop',  'state': (0, 3), 'g': 7, 'h': 0, 'f': 7},
    ]
    assert actual == expected
    assert len(actual) == 22

    bounded = [e for e in actual if e.get('is_bounded')]
    assert len(bounded) == 2
    assert {e['type'] for e in bounded} == {'push', 'pop'}
    assert all(e['state'] == (1, 1) for e in bounded)
    for e in actual:
        if e['state'] != (1, 1):
            assert 'is_bounded' not in e
    for e in actual:
        assert 'is_cached' not in e


# ────────────────────────────────────────────────────────────────────────────
#  3. propagate_pathmax
# ────────────────────────────────────────────────────────────────────────────


def test_propagate_pathmax_raises_without_hbounded() -> None:
    """
    ========================================================================
     Calling propagate_pathmax on an AStarLookup whose h has no
     HBounded in its chain raises ValueError — no target
     storage for tightened bounds.
    ========================================================================
    """
    a = StateBase[str](key='A')
    cache = {a: CacheEntry(h_perfect=0, suffix_next=None)}
    h = HCached(base=HCallable(fn=lambda s: 0),
                cache=cache, goal=a)
    algo = AStarLookup(problem=ProblemSPP.Factory.graph_start_is_goal(),
                 h=h)
    assert isinstance(algo, AStarLookup)
    with pytest.raises(ValueError, match='HBounded'):
        algo.propagate_pathmax(depth=2)


def test_propagate_pathmax_grid_4x4_depth_1_from_bounded_seed(
        ) -> None:
    """
    ========================================================================
     Seed HBounded with (1,1)=5. Depth=1 propagates from (1,1)
     to (0,1), (2,1), (1,0). Only (0,1) tightens.
    ========================================================================
    """
    def sc(r: int, c: int) -> StateCell:
        return StateCell(key=CellMap(row=r, col=c))

    problem = ProblemGrid.Factory.grid_4x4_obstacle()
    goal = problem.goal
    h = HBounded(
        base=HCallable(fn=lambda s: s.key.distance(goal.key)),
        bounds={sc(1, 1): 5},
    )
    algo = AStarLookup(problem=problem, h=h)
    assert isinstance(algo, AStarLookup)
    updates = algo.propagate_pathmax(depth=1)
    assert updates == {sc(0, 1): 4}
    assert h(sc(0, 1)) == 4
    assert h.is_bounded(state=sc(0, 1)) is True
    assert h.is_bounded(state=sc(2, 1)) is False
    assert h.is_bounded(state=sc(1, 0)) is False


def test_propagate_pathmax_depth_none_runs_to_convergence(
        ) -> None:
    """
    ========================================================================
     `depth=None` (default) propagates until convergence — stops
     when a wave tightens nothing. Seed (0,0)=7: wave 1 tightens
     (0,1) and (1,0); wave 2 tightens (1,1); wave 3 tightens no
     more. Result equals explicit depth=2 for this topology.
    ========================================================================
    """
    def sc(r: int, c: int) -> StateCell:
        return StateCell(key=CellMap(row=r, col=c))

    problem = ProblemGrid.Factory.grid_4x4_obstacle()
    goal = problem.goal
    h = HBounded(
        base=HCallable(fn=lambda s: s.key.distance(goal.key)),
        bounds={sc(0, 0): 7},
    )
    algo = AStarLookup(problem=problem, h=h)
    updates = algo.propagate_pathmax()   # depth=None default
    assert updates == {
        sc(0, 1): 6,
        sc(1, 0): 6,
        sc(1, 1): 5,
    }


def test_recording_propagate_wave_events_mark_wave_boundaries(
        ) -> None:
    """
    ========================================================================
     `propagate_wave` events mark the start of each wave that
     runs. Pins:
       1. One wave event per iteration that actually runs.
       2. Depths count from 0 upward.
       3. Emitted BEFORE the wave's attempts (each wave event
          precedes all `propagate` events whose source belongs
          to that wave).
       4. State-less meta-event — no `state` field, no `parent`.
       5. `propagate_pathmax(depth=0)` emits zero wave events
          (loop body never executes).
    ========================================================================
    """
    def sc(r: int, c: int) -> StateCell:
        return StateCell(key=CellMap(row=r, col=c))

    problem = ProblemGrid.Factory.grid_4x4_obstacle()
    goal = problem.goal
    h = HBounded(
        base=HCallable(fn=lambda s: s.key.distance(goal.key)),
        bounds={sc(0, 0): 7},
    )
    algo = AStarLookup(problem=problem, h=h, is_recording=True)
    algo.propagate_pathmax()   # depth=None, runs to convergence

    events = [normalize(e) for e in algo.recorder.events]
    wave_events = [e for e in events
                   if e['type'] == 'propagate_wave']
    # Three waves ran: wave 0 seeded by (0,0)=7 (1 source);
    # wave 1 by (0,1) and (1,0) (2 sources); wave 2 by (1,1)
    # (1 source, all targets no-op → loop exits).
    assert [e['depth'] for e in wave_events] == [0, 1, 2]
    assert [e['num_sources'] for e in wave_events] == [1, 2, 1]
    for w in wave_events:
        assert 'state' not in w
        assert 'parent' not in w
        assert 'g' not in w
        assert 'h' not in w
        assert 'num_sources' in w

    # Each wave event precedes its wave's propagate events.
    idx_wave_0 = events.index(wave_events[0])
    idx_wave_1 = events.index(wave_events[1])
    # First propagate (from seed (0,0)) comes after wave 0.
    first_prop = next(i for i, e in enumerate(events)
                      if e['type'] == 'propagate')
    assert idx_wave_0 < first_prop < idx_wave_1

    # depth=0 → no wave events.
    h2 = HBounded(
        base=HCallable(fn=lambda s: s.key.distance(goal.key)),
        bounds={sc(0, 0): 7},
    )
    algo2 = AStarLookup(problem=problem, h=h2, is_recording=True)
    algo2.propagate_pathmax(depth=0)
    assert not any(e['type'] == 'propagate_wave'
                   for e in algo2.recorder.events)


def test_propagate_pathmax_depth_zero_is_noop() -> None:
    """
    ========================================================================
     `depth=0` is a valid no-op; returns {} without entering the
     wave loop.
    ========================================================================
    """
    def sc(r: int, c: int) -> StateCell:
        return StateCell(key=CellMap(row=r, col=c))

    problem = ProblemGrid.Factory.grid_4x4_obstacle()
    goal = problem.goal
    h = HBounded(
        base=HCallable(fn=lambda s: s.key.distance(goal.key)),
        bounds={sc(0, 0): 7},
    )
    algo = AStarLookup(problem=problem, h=h)
    assert algo.propagate_pathmax(depth=0) == {}


def test_propagate_pathmax_grid_4x4_depth_2_compounds() -> None:
    """
    ========================================================================
     Depth=2 from seed (1,1)=5: wave 1 tightens (0,1) to 4.
     Wave 2 back-edge (0,1)->(1,1) is SKIPPED (last-tightener
     optimisation). (0,1)->(0,0) attempted: no tighten. Final
     updates == {(0,1): 4}.
    ========================================================================
    """
    def sc(r: int, c: int) -> StateCell:
        return StateCell(key=CellMap(row=r, col=c))

    problem = ProblemGrid.Factory.grid_4x4_obstacle()
    goal = problem.goal
    h = HBounded(
        base=HCallable(fn=lambda s: s.key.distance(goal.key)),
        bounds={sc(1, 1): 5},
    )
    algo = AStarLookup(problem=problem, h=h)
    updates = algo.propagate_pathmax(depth=2)
    assert updates == {sc(0, 1): 4}
    assert h(sc(0, 0)) == 3
    assert h.is_bounded(state=sc(0, 0)) is False
    assert h(sc(1, 1)) == 5
