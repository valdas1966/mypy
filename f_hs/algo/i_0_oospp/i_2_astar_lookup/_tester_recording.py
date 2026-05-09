"""
============================================================================
 AStarLookup — full event-stream pins on the canonical OOSPP
 problem (`grid_4x4_obstacle`: start (0,0), goal (0,3), wall
 at (0,2)/(1,2), Manhattan h, optimal cost 7).

 Mirrors `_tester_counters.py` one-to-one — same four
 scenarios, same problem, same param choices — but assertions
 are at the event-stream level (every field of every
 normalized event, manually pinned). The two files together
 give a full per-scenario lock:
   - `_tester_counters.py` pins the integer summary.
   - `_tester_recording.py` pins the full timeline that
     produced that summary.

 Configurations:
   - test_recording_baseline           — no cache, no bounds.
                                         Plain AStar trace
                                         (22 events).
   - test_recording_cached             — cache (1,1) at
                                         h_perfect=5. Cache-
                                         hit early-term on
                                         (1,1) pop (9 events).
   - test_recording_bounded            — bound (1,0) at h=6.
                                         (1,0) pushed but
                                         pruned from pop set
                                         (21 events).
   - test_recording_bounded_propagated — bound (0,0) at h=7
                                         + propagate_pathmax(
                                         depth=None). 3 waves;
                                         wave 2 is the
                                         no-tighten exit
                                         signal (31 events:
                                         3 propagate_wave +
                                         7 propagate +
                                         21 search).
============================================================================
"""

from f_ds.grids.cell.i_1_map import CellMap

from f_hs.algo.i_0_oospp.i_2_astar_lookup import AStarLookup
from f_hs.algo.u_event_normalize import normalize
from f_hs.heuristic.i_0_base._cache_entry import CacheEntry
from f_hs.problem.i_1_grid import ProblemGrid
from f_hs.state.i_1_cell.main import StateCell


def test_recording_baseline() -> None:
    """
    ========================================================================
     Canonical OOSPP, no cache, no bounds — heuristic chain
     collapses to HCallable(Manhattan). Pin the FULL 22-event
     trace (13 push + 9 pop). Pop count matches
     test_counters_baseline (cnt_pop=9).
    ========================================================================
    """
    problem = ProblemGrid.Factory.grid_4x4_obstacle()
    goal = problem.goal
    algo = AStarLookup(
        problem=problem,
        h=lambda s: float(s.distance(goal)),
        is_recording=True,
    )
    algo.run()
    actual = [normalize(e) for e in algo.recorder.events]
    expected = [
        {'type': 'push', 'state': (0, 0), 'g': 0, 'parent': None, 'h': 3, 'f': 3},
        {'type': 'pop',  'state': (0, 0), 'g': 0, 'h': 3, 'f': 3},
        {'type': 'push', 'state': (0, 1), 'g': 1, 'parent': (0, 0), 'h': 2, 'f': 3},
        {'type': 'push', 'state': (1, 0), 'g': 1, 'parent': (0, 0), 'h': 4, 'f': 5},
        {'type': 'pop',  'state': (0, 1), 'g': 1, 'h': 2, 'f': 3},
        {'type': 'push', 'state': (1, 1), 'g': 2, 'parent': (0, 1), 'h': 3, 'f': 5},
        {'type': 'pop',  'state': (1, 1), 'g': 2, 'h': 3, 'f': 5},
        {'type': 'push', 'state': (2, 1), 'g': 3, 'parent': (1, 1), 'h': 4, 'f': 7},
        {'type': 'pop',  'state': (1, 0), 'g': 1, 'h': 4, 'f': 5},
        {'type': 'push', 'state': (2, 0), 'g': 2, 'parent': (1, 0), 'h': 5, 'f': 7},
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


def test_recording_cached() -> None:
    """
    ========================================================================
     Canonical OOSPP + cache (1,1) at h_perfect=5. Only push
     of (1,1) carries `is_cached=True`; (0,1) and (1,0) push
     at the cheap Manhattan f=3/f=5 unaffected. (1,1) pops
     first within the f=7 group via cache_rank=0; cache-hit
     early-term fires on its pop (9 events: 5 push + 4 pop).
     Push/pop counts match test_counters_cached (cnt_push=5,
     cnt_pop=4).
    ========================================================================
    """
    problem = ProblemGrid.Factory.grid_4x4_obstacle()
    goal = problem.goal
    s11 = StateCell(key=CellMap(row=1, col=1))
    cache = {s11: CacheEntry(h_perfect=5, suffix_next=None)}
    algo = AStarLookup(
        problem=problem,
        h=lambda s: float(s.distance(goal)),
        cache=cache,
        goal=goal,
        is_recording=True,
    )
    algo.run()
    actual = [normalize(e) for e in algo.recorder.events]
    expected = [
        {'type': 'push', 'state': (0, 0), 'g': 0, 'parent': None, 'h': 3, 'f': 3},
        {'type': 'pop',  'state': (0, 0), 'g': 0, 'h': 3, 'f': 3},
        {'type': 'push', 'state': (0, 1), 'g': 1, 'parent': (0, 0), 'h': 2, 'f': 3},
        {'type': 'push', 'state': (1, 0), 'g': 1, 'parent': (0, 0), 'h': 4, 'f': 5},
        {'type': 'pop',  'state': (0, 1), 'g': 1, 'h': 2, 'f': 3},
        {'type': 'push', 'state': (1, 1), 'g': 2, 'parent': (0, 1), 'h': 5, 'f': 7, 'is_cached': True},
        {'type': 'pop',  'state': (1, 0), 'g': 1, 'h': 4, 'f': 5},
        {'type': 'push', 'state': (2, 0), 'g': 2, 'parent': (1, 0), 'h': 5, 'f': 7},
        {'type': 'pop',  'state': (1, 1), 'g': 2, 'h': 5, 'f': 7, 'is_cached': True},
    ]
    assert actual == expected
    assert len(actual) == 9


def test_recording_bounded() -> None:
    """
    ========================================================================
     Canonical OOSPP + bound (1,0) at h=6 (= h*((1,0))). The
     bumped f=7 dominates (1,0) out of the pop set — pushed
     once with `is_bounded=True`, never popped. 21 events
     (vs 22 baseline; the missing pop is (1,0)'s, plus a (2,0)
     push gone with it isn't — wait, (2,0) is pushed via (2,1)
     in the bound trace too, so counts shift). Push/pop
     counts match test_counters_bounded (cnt_push=13,
     cnt_pop=8).
    ========================================================================
    """
    problem = ProblemGrid.Factory.grid_4x4_obstacle()
    goal = problem.goal
    s10 = StateCell(key=CellMap(row=1, col=0))
    bounds = {s10: 6}
    algo = AStarLookup(
        problem=problem,
        h=lambda s: float(s.distance(goal)),
        bounds=bounds,
        is_recording=True,
    )
    algo.run()
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


def test_recording_bounded_propagated() -> None:
    """
    ========================================================================
     Canonical OOSPP + bound (0,0) at h=7 + pre-search
     `propagate_pathmax(depth=None)` (run to convergence).
     31 events total: 3 propagate_wave + 7 propagate + 21
     search. Wave 2 is the no-tighten exit signal — the
     `propagate_wave` event still fires (wave count = 3) and
     the wave's 2 propagate attempts both report
     `was_improved=False`, then sources go empty and the loop
     exits. Push/pop counts (post-propagate group) match
     test_counters_bounded_propagated.
    ========================================================================
    """
    problem = ProblemGrid.Factory.grid_4x4_obstacle()
    goal = problem.goal
    s00 = StateCell(key=CellMap(row=0, col=0))
    bounds = {s00: 7}
    algo = AStarLookup(
        problem=problem,
        h=lambda s: float(s.distance(goal)),
        bounds=bounds,
        is_recording=True,
    )
    algo.propagate_pathmax()
    algo.run()
    actual = [normalize(e) for e in algo.recorder.events]
    expected = [
        # Pre-search pathmax — 3 waves (wave 2 is exit signal).
        {'type': 'propagate_wave', 'depth': 0, 'num_sources': 1},
        {'type': 'propagate', 'state': (0, 1), 'parent': (0, 0), 'h_parent': 7, 'h': 6, 'was_improved': True},
        {'type': 'propagate', 'state': (1, 0), 'parent': (0, 0), 'h_parent': 7, 'h': 6, 'was_improved': True},
        {'type': 'propagate_wave', 'depth': 1, 'num_sources': 2},
        {'type': 'propagate', 'state': (1, 1), 'parent': (0, 1), 'h_parent': 6, 'h': 5, 'was_improved': True},
        {'type': 'propagate', 'state': (1, 1), 'parent': (1, 0), 'h_parent': 6, 'h': 5, 'was_improved': False},
        {'type': 'propagate', 'state': (2, 0), 'parent': (1, 0), 'h_parent': 6, 'h': 5, 'was_improved': False},
        {'type': 'propagate_wave', 'depth': 2, 'num_sources': 1},
        {'type': 'propagate', 'state': (2, 1), 'parent': (1, 1), 'h_parent': 5, 'h': 4, 'was_improved': False},
        {'type': 'propagate', 'state': (1, 0), 'parent': (1, 1), 'h_parent': 5, 'h': 6, 'was_improved': False},
        # Search — the lifted h on (0,1)/(1,0)/(1,1) prunes
        # one pop and one expansion vs the no-propagate trace.
        {'type': 'push', 'state': (0, 0), 'g': 0, 'parent': None, 'h': 7, 'f': 7, 'is_bounded': True},
        {'type': 'pop',  'state': (0, 0), 'g': 0, 'h': 7, 'f': 7, 'is_bounded': True},
        {'type': 'push', 'state': (0, 1), 'g': 1, 'parent': (0, 0), 'h': 6, 'f': 7, 'is_bounded': True},
        {'type': 'push', 'state': (1, 0), 'g': 1, 'parent': (0, 0), 'h': 6, 'f': 7, 'is_bounded': True},
        {'type': 'pop',  'state': (0, 1), 'g': 1, 'h': 6, 'f': 7, 'is_bounded': True},
        {'type': 'push', 'state': (1, 1), 'g': 2, 'parent': (0, 1), 'h': 5, 'f': 7, 'is_bounded': True},
        {'type': 'pop',  'state': (1, 1), 'g': 2, 'h': 5, 'f': 7, 'is_bounded': True},
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
    assert len(actual) == 31
