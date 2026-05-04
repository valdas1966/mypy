"""
============================================================================
 AStarLookup — full event-stream pins. One test per
 param-config; each asserts the complete normalized event
 list (every field of every event, `duration` stripped).

 Configurations covered:
   - canonical (no cache, no bounds): plain AStar trace.
   - with cache (graph_abc, cached at B): cache-hit early
     termination; `is_cached` flags on push/pop of cached
     states.
   - with cache (grid_4x4, optimal-suffix cached): early-
     terminate after popping a cached state along the
     optimal path.
   - with bounds (grid_4x4, prune (1,0)=6): bounded state
     pushed but never popped; `is_bounded` flag on push.
   - with bounds (grid_4x4, lift (1,1)=5): bounded state
     popped; `is_bounded` flag on both push and pop.
   - with bounds + propagate_pathmax(depth=2) seeded at
     (1,1)=5: 2 waves; back-edge skip; only (0,1) tightens.
   - with bounds + propagate_pathmax(depth=2) seeded at
     (0,0)=7: 2 waves; multi-wave compounding tightens
     (0,1), (1,0), (1,1).
   - with bounds + propagate_pathmax(depth=None) seeded at
     (0,0)=7: runs to convergence (3 waves: third is no-op,
     loop exits).
============================================================================
"""

from f_ds.grids.cell.i_1_map import CellMap

from f_hs.algo.i_0_oospp.i_2_astar_lookup import AStarLookup
from f_hs.algo.u_event_normalize import normalize
from f_hs.heuristic.i_1_bounded.main import HBounded
from f_hs.heuristic.i_1_callable.main import HCallable
from f_hs.problem.i_1_grid import ProblemGrid
from f_hs.state.i_1_cell.main import StateCell


def _sc(r: int, c: int) -> StateCell:
    return StateCell(key=CellMap(row=r, col=c))


def test_recording_canonical_oospp_no_cache_no_bounds() -> None:
    """
    ========================================================================
     Pin the FULL event stream for AStarLookup with no cache /
     no bounds — heuristic chain collapses to HCallable(h).
     Equivalent to plain AStar's 22-event sequence.
    ========================================================================
    """
    p = ProblemGrid.Factory.grid_4x4_obstacle()
    goal = p.goal
    algo = AStarLookup(problem=p,
                       h=lambda s: float(s.distance(goal)),
                       is_recording=True)
    algo.run()
    actual = [normalize(e) for e in algo.recorder.events]
    expected = [
        {'type': 'push', 'state': (0, 0), 'g': 0, 'parent': None, 'h': 3, 'f': 3},
        {'type': 'pop', 'state': (0, 0), 'g': 0, 'h': 3, 'f': 3},
        {'type': 'push', 'state': (0, 1), 'g': 1, 'parent': (0, 0), 'h': 2, 'f': 3},
        {'type': 'push', 'state': (1, 0), 'g': 1, 'parent': (0, 0), 'h': 4, 'f': 5},
        {'type': 'pop', 'state': (0, 1), 'g': 1, 'h': 2, 'f': 3},
        {'type': 'push', 'state': (1, 1), 'g': 2, 'parent': (0, 1), 'h': 3, 'f': 5},
        {'type': 'pop', 'state': (1, 1), 'g': 2, 'h': 3, 'f': 5},
        {'type': 'push', 'state': (2, 1), 'g': 3, 'parent': (1, 1), 'h': 4, 'f': 7},
        {'type': 'pop', 'state': (1, 0), 'g': 1, 'h': 4, 'f': 5},
        {'type': 'push', 'state': (2, 0), 'g': 2, 'parent': (1, 0), 'h': 5, 'f': 7},
        {'type': 'pop', 'state': (2, 1), 'g': 3, 'h': 4, 'f': 7},
        {'type': 'push', 'state': (2, 2), 'g': 4, 'parent': (2, 1), 'h': 3, 'f': 7},
        {'type': 'push', 'state': (3, 1), 'g': 4, 'parent': (2, 1), 'h': 5, 'f': 9},
        {'type': 'pop', 'state': (2, 2), 'g': 4, 'h': 3, 'f': 7},
        {'type': 'push', 'state': (2, 3), 'g': 5, 'parent': (2, 2), 'h': 2, 'f': 7},
        {'type': 'push', 'state': (3, 2), 'g': 5, 'parent': (2, 2), 'h': 4, 'f': 9},
        {'type': 'pop', 'state': (2, 3), 'g': 5, 'h': 2, 'f': 7},
        {'type': 'push', 'state': (1, 3), 'g': 6, 'parent': (2, 3), 'h': 1, 'f': 7},
        {'type': 'push', 'state': (3, 3), 'g': 6, 'parent': (2, 3), 'h': 3, 'f': 9},
        {'type': 'pop', 'state': (1, 3), 'g': 6, 'h': 1, 'f': 7},
        {'type': 'push', 'state': (0, 3), 'g': 7, 'parent': (1, 3), 'h': 0, 'f': 7},
        {'type': 'pop', 'state': (0, 3), 'g': 7, 'h': 0, 'f': 7},
    ]
    assert actual == expected


def test_recording_cache_graph_abc_cached_at_b() -> None:
    """
    ========================================================================
     Pin the FULL event stream for AStarLookup with HCached
     covering {B, C} on graph A → B → C. Pops A (uncached);
     expands to B (cached); pops B and triggers cache-hit
     early termination. `is_cached` flag on push/pop of B
     only.
    ========================================================================
    """
    algo = AStarLookup.Factory.graph_abc_cached_at_b()
    algo._recorder.is_active = True
    algo.run()
    actual = [normalize(e) for e in algo.recorder.events]
    expected = [
        {'type': 'push', 'state': 'A', 'g': 0, 'parent': None, 'h': 2, 'f': 2},
        {'type': 'pop',  'state': 'A', 'g': 0, 'h': 2, 'f': 2},
        {'type': 'push', 'state': 'B', 'g': 1, 'parent': 'A', 'h': 1, 'f': 2, 'is_cached': True},
        {'type': 'pop',  'state': 'B', 'g': 1, 'h': 1, 'f': 2, 'is_cached': True},
    ]
    assert actual == expected


def test_recording_bounds_prune_grid_4x4_obstacle() -> None:
    """
    ========================================================================
     Pin the FULL event stream for AStarLookup with HBounded
     bounding (1,0)=6 (tight; h*((1,0))=6). The bumped f=7
     dominates (1,0) out of the pop set — pushed but never
     popped. `is_bounded` flag on push only.
    ========================================================================
    """
    p = ProblemGrid.Factory.grid_4x4_obstacle()
    goal = p.goal
    h = HBounded(
        base=HCallable(fn=lambda s: s.distance(goal)),
        bounds={_sc(1, 0): 6},
    )
    algo = AStarLookup(problem=p, h=h, is_recording=True)
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


def test_recording_bounds_lift_popped_grid_4x4_obstacle() -> None:
    """
    ========================================================================
     Pin the FULL event stream for AStarLookup with HBounded
     bounding (1,1)=5 (tight). (1,1) IS popped — so
     `is_bounded` flag appears on BOTH push AND pop of (1,1).
    ========================================================================
    """
    p = ProblemGrid.Factory.grid_4x4_obstacle()
    goal = p.goal
    h = HBounded(
        base=HCallable(fn=lambda s: s.distance(goal)),
        bounds={_sc(1, 1): 5},
    )
    algo = AStarLookup(problem=p, h=h, is_recording=True)
    algo.run()
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


def test_recording_pathmax_depth_2_from_seed_1_1() -> None:
    """
    ========================================================================
     Pin the FULL event stream for AStarLookup with HBounded
     seed (1,1)=5 followed by `propagate_pathmax(depth=2)`.
     Wave 0: 3 attempts from (1,1); only (0,1) tightens to 4.
     Wave 1: 1 attempt from (0,1); back-edge to (1,1) skipped
     (last-tightener optimization). 28 events total
     (2 waves + 4 propagate + 22 search).
    ========================================================================
    """
    p = ProblemGrid.Factory.grid_4x4_obstacle()
    goal = p.goal
    h = HBounded(
        base=HCallable(fn=lambda s: s.distance(goal)),
        bounds={_sc(1, 1): 5},
    )
    algo = AStarLookup(problem=p, h=h, is_recording=True)
    algo.propagate_pathmax(depth=2)
    algo.run()
    actual = [normalize(e) for e in algo.recorder.events]
    expected = [
        {'type': 'propagate_wave', 'depth': 0, 'num_sources': 1},
        {'type': 'propagate', 'state': (0, 1), 'parent': (1, 1), 'h_parent': 5, 'h': 4, 'was_improved': True},
        {'type': 'propagate', 'state': (2, 1), 'parent': (1, 1), 'h_parent': 5, 'h': 4, 'was_improved': False},
        {'type': 'propagate', 'state': (1, 0), 'parent': (1, 1), 'h_parent': 5, 'h': 4, 'was_improved': False},
        {'type': 'propagate_wave', 'depth': 1, 'num_sources': 1},
        {'type': 'propagate', 'state': (0, 0), 'parent': (0, 1), 'h_parent': 4, 'h': 3, 'was_improved': False},
        {'type': 'push', 'state': (0, 0), 'g': 0, 'parent': None, 'h': 3, 'f': 3},
        {'type': 'pop',  'state': (0, 0), 'g': 0, 'h': 3, 'f': 3},
        {'type': 'push', 'state': (0, 1), 'g': 1, 'parent': (0, 0), 'h': 4, 'f': 5, 'is_bounded': True},
        {'type': 'push', 'state': (1, 0), 'g': 1, 'parent': (0, 0), 'h': 4, 'f': 5},
        {'type': 'pop',  'state': (0, 1), 'g': 1, 'h': 4, 'f': 5, 'is_bounded': True},
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


def test_recording_pathmax_depth_2_from_seed_0_0_multiwave() -> None:
    """
    ========================================================================
     Pin the FULL event stream for AStarLookup with HBounded
     seed (0,0)=7 followed by `propagate_pathmax(depth=2)`.
     Multi-wave: wave 0 tightens (0,1) and (1,0); wave 1
     tightens (1,1) (and (1,1)-from-(1,0) is no-op since
     (0,1) tightened it first). Search pruned to 21 events.
    ========================================================================
    """
    p = ProblemGrid.Factory.grid_4x4_obstacle()
    goal = p.goal
    h = HBounded(
        base=HCallable(fn=lambda s: s.distance(goal)),
        bounds={_sc(0, 0): 7},
    )
    algo = AStarLookup(problem=p, h=h, is_recording=True)
    algo.propagate_pathmax(depth=2)
    algo.run()
    actual = [normalize(e) for e in algo.recorder.events]
    expected = [
        {'type': 'propagate_wave', 'depth': 0, 'num_sources': 1},
        {'type': 'propagate', 'state': (0, 1), 'parent': (0, 0), 'h_parent': 7, 'h': 6, 'was_improved': True},
        {'type': 'propagate', 'state': (1, 0), 'parent': (0, 0), 'h_parent': 7, 'h': 6, 'was_improved': True},
        {'type': 'propagate_wave', 'depth': 1, 'num_sources': 2},
        {'type': 'propagate', 'state': (1, 1), 'parent': (0, 1), 'h_parent': 6, 'h': 5, 'was_improved': True},
        {'type': 'propagate', 'state': (1, 1), 'parent': (1, 0), 'h_parent': 6, 'h': 5, 'was_improved': False},
        {'type': 'propagate', 'state': (2, 0), 'parent': (1, 0), 'h_parent': 6, 'h': 5, 'was_improved': False},
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


def test_recording_pathmax_depth_none_convergence() -> None:
    """
    ========================================================================
     Pin the FULL event stream for AStarLookup with HBounded
     seed (0,0)=7 followed by `propagate_pathmax(depth=None)`
     — runs to convergence. 3 waves run; wave 2's targets
     all no-op (loop exits). Same search trace as depth=2.
    ========================================================================
    """
    p = ProblemGrid.Factory.grid_4x4_obstacle()
    goal = p.goal
    h = HBounded(
        base=HCallable(fn=lambda s: s.distance(goal)),
        bounds={_sc(0, 0): 7},
    )
    algo = AStarLookup(problem=p, h=h, is_recording=True)
    algo.propagate_pathmax()  # depth=None
    algo.run()
    actual = [normalize(e) for e in algo.recorder.events]
    expected = [
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
