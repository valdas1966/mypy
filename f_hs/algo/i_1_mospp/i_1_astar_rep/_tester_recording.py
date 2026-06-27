"""
============================================================================
 AStarRepMOSPP — full event-stream pins. One test per scenario;
 each asserts the complete normalized event list (`duration`
 stripped). Mirror of `KxAStarOMSPP`'s recording tester with
 the axis-swap event schema:

   - push / pop / decrease_g  — from each inner AStar.
   - on_start                 — per start at sub-search end;
                                payload: state, g, reason,
                                start_index. `reason ∈
                                {expanded, already_reached,
                                unreachable}`. NEVER
                                `already_closed` (no shared
                                CLOSED set).
   - update_frontier          — NEVER emitted (no transition).

 The event stream concatenates k independent AStar streams
 interleaved with per-start `on_start` markers.

 Scenarios:
   - canonical MOSPP grid (3 starts): independent A*s from
     (0,3), (3,0), (3,3) to (0,0). 57 events.
   - 2-start `grid_4x4_obstacle` variant: independent A*s
     from (0,3), (3,3) to (0,0). 45 events.
============================================================================
"""

from f_hs.algo.i_1_mospp.i_1_astar_rep import AStarRepMOSPP
from f_hs.algo.u_event_normalize import normalize
from f_hs.problem.i_1_grid import ProblemGrid


def _grid_4x4_obstacle_2starts() -> ProblemGrid:
    """
    ========================================================================
     4x4 obstacle grid with starts=[(0,3), (3,3)] and goal
     (0,0). Mirror of the OMSPP 2-goal variant.
    ========================================================================
    """
    p = ProblemGrid.Factory.grid_4x4_obstacle()
    grid = p.grid
    p._starts = [p._states[grid[0][3]], p._states[grid[3][3]]]
    p._goals = [p._states[grid[0][0]]]
    return p


def test_recording_canonical_mospp() -> None:
    """
    ========================================================================
     Pin the FULL event stream for AStarRepMOSPP on the
     canonical MOSPP problem. Three independent A* sub-
     searches, no state sharing. Each starts with `push` of a
     different start state under h = Manhattan to (0,0).
    ========================================================================
    """
    p = ProblemGrid.Factory.grid_4x4_obstacle_mospp()
    algo = AStarRepMOSPP(problem=p,
                        h=lambda s, g: float(s.key.distance(g.key)),
                        is_recording=True)
    algo.run()
    actual = [normalize(e) for e in algo.recorder.events]
    expected = [
        # ── Sub-search 1: start=(0,3), goal=(0,0) ──
        {'type': 'push', 'state': (0, 3), 'g': 0, 'parent': None, 'h': 3, 'f': 3},
        {'type': 'pop',  'state': (0, 3), 'g': 0, 'h': 3, 'f': 3},
        {'type': 'push', 'state': (1, 3), 'g': 1, 'parent': (0, 3), 'h': 4, 'f': 5},
        {'type': 'pop',  'state': (1, 3), 'g': 1, 'h': 4, 'f': 5},
        {'type': 'push', 'state': (2, 3), 'g': 2, 'parent': (1, 3), 'h': 5, 'f': 7},
        {'type': 'pop',  'state': (2, 3), 'g': 2, 'h': 5, 'f': 7},
        {'type': 'push', 'state': (3, 3), 'g': 3, 'parent': (2, 3), 'h': 6, 'f': 9},
        {'type': 'push', 'state': (2, 2), 'g': 3, 'parent': (2, 3), 'h': 4, 'f': 7},
        {'type': 'pop',  'state': (2, 2), 'g': 3, 'h': 4, 'f': 7},
        {'type': 'push', 'state': (3, 2), 'g': 4, 'parent': (2, 2), 'h': 5, 'f': 9},
        {'type': 'push', 'state': (2, 1), 'g': 4, 'parent': (2, 2), 'h': 3, 'f': 7},
        {'type': 'pop',  'state': (2, 1), 'g': 4, 'h': 3, 'f': 7},
        {'type': 'push', 'state': (1, 1), 'g': 5, 'parent': (2, 1), 'h': 2, 'f': 7},
        {'type': 'push', 'state': (3, 1), 'g': 5, 'parent': (2, 1), 'h': 4, 'f': 9},
        {'type': 'push', 'state': (2, 0), 'g': 5, 'parent': (2, 1), 'h': 2, 'f': 7},
        {'type': 'pop',  'state': (1, 1), 'g': 5, 'h': 2, 'f': 7},
        {'type': 'push', 'state': (0, 1), 'g': 6, 'parent': (1, 1), 'h': 1, 'f': 7},
        {'type': 'push', 'state': (1, 0), 'g': 6, 'parent': (1, 1), 'h': 1, 'f': 7},
        {'type': 'pop',  'state': (0, 1), 'g': 6, 'h': 1, 'f': 7},
        {'type': 'push', 'state': (0, 0), 'g': 7, 'parent': (0, 1), 'h': 0, 'f': 7},
        {'type': 'pop',  'state': (0, 0), 'g': 7, 'h': 0, 'f': 7},
        {'type': 'on_start', 'state': (0, 3), 'g': 7, 'reason': 'expanded', 'start_index': 0},
        # ── Sub-search 2: start=(3,0), goal=(0,0) ──
        {'type': 'push', 'state': (3, 0), 'g': 0, 'parent': None, 'h': 3, 'f': 3},
        {'type': 'pop',  'state': (3, 0), 'g': 0, 'h': 3, 'f': 3},
        {'type': 'push', 'state': (2, 0), 'g': 1, 'parent': (3, 0), 'h': 2, 'f': 3},
        {'type': 'push', 'state': (3, 1), 'g': 1, 'parent': (3, 0), 'h': 4, 'f': 5},
        {'type': 'pop',  'state': (2, 0), 'g': 1, 'h': 2, 'f': 3},
        {'type': 'push', 'state': (1, 0), 'g': 2, 'parent': (2, 0), 'h': 1, 'f': 3},
        {'type': 'push', 'state': (2, 1), 'g': 2, 'parent': (2, 0), 'h': 3, 'f': 5},
        {'type': 'pop',  'state': (1, 0), 'g': 2, 'h': 1, 'f': 3},
        {'type': 'push', 'state': (0, 0), 'g': 3, 'parent': (1, 0), 'h': 0, 'f': 3},
        {'type': 'push', 'state': (1, 1), 'g': 3, 'parent': (1, 0), 'h': 2, 'f': 5},
        {'type': 'pop',  'state': (0, 0), 'g': 3, 'h': 0, 'f': 3},
        {'type': 'on_start', 'state': (3, 0), 'g': 3, 'reason': 'expanded', 'start_index': 1},
        # ── Sub-search 3: start=(3,3), goal=(0,0) ──
        {'type': 'push', 'state': (3, 3), 'g': 0, 'parent': None, 'h': 6, 'f': 6},
        {'type': 'pop',  'state': (3, 3), 'g': 0, 'h': 6, 'f': 6},
        {'type': 'push', 'state': (2, 3), 'g': 1, 'parent': (3, 3), 'h': 5, 'f': 6},
        {'type': 'push', 'state': (3, 2), 'g': 1, 'parent': (3, 3), 'h': 5, 'f': 6},
        {'type': 'pop',  'state': (2, 3), 'g': 1, 'h': 5, 'f': 6},
        {'type': 'push', 'state': (1, 3), 'g': 2, 'parent': (2, 3), 'h': 4, 'f': 6},
        {'type': 'push', 'state': (2, 2), 'g': 2, 'parent': (2, 3), 'h': 4, 'f': 6},
        {'type': 'pop',  'state': (1, 3), 'g': 2, 'h': 4, 'f': 6},
        {'type': 'push', 'state': (0, 3), 'g': 3, 'parent': (1, 3), 'h': 3, 'f': 6},
        {'type': 'pop',  'state': (0, 3), 'g': 3, 'h': 3, 'f': 6},
        {'type': 'pop',  'state': (2, 2), 'g': 2, 'h': 4, 'f': 6},
        {'type': 'push', 'state': (2, 1), 'g': 3, 'parent': (2, 2), 'h': 3, 'f': 6},
        {'type': 'pop',  'state': (2, 1), 'g': 3, 'h': 3, 'f': 6},
        {'type': 'push', 'state': (1, 1), 'g': 4, 'parent': (2, 1), 'h': 2, 'f': 6},
        {'type': 'push', 'state': (3, 1), 'g': 4, 'parent': (2, 1), 'h': 4, 'f': 8},
        {'type': 'push', 'state': (2, 0), 'g': 4, 'parent': (2, 1), 'h': 2, 'f': 6},
        {'type': 'pop',  'state': (1, 1), 'g': 4, 'h': 2, 'f': 6},
        {'type': 'push', 'state': (0, 1), 'g': 5, 'parent': (1, 1), 'h': 1, 'f': 6},
        {'type': 'push', 'state': (1, 0), 'g': 5, 'parent': (1, 1), 'h': 1, 'f': 6},
        {'type': 'pop',  'state': (0, 1), 'g': 5, 'h': 1, 'f': 6},
        {'type': 'push', 'state': (0, 0), 'g': 6, 'parent': (0, 1), 'h': 0, 'f': 6},
        {'type': 'pop',  'state': (0, 0), 'g': 6, 'h': 0, 'f': 6},
        {'type': 'on_start', 'state': (3, 3), 'g': 6, 'reason': 'expanded', 'start_index': 2},
    ]
    assert actual == expected


def test_recording_grid_4x4_obstacle_2starts() -> None:
    """
    ========================================================================
     Pin the FULL event stream for AStarRepMOSPP on the 2-start
     `grid_4x4_obstacle` variant (starts=[(0,3),(3,3)], goal
     (0,0)). Two independent A*s — no state sharing, no
     update_frontier.
    ========================================================================
    """
    p = _grid_4x4_obstacle_2starts()
    algo = AStarRepMOSPP(problem=p,
                        h=lambda s, g: float(s.key.distance(g.key)),
                        is_recording=True)
    algo.run()
    actual = [normalize(e) for e in algo.recorder.events]
    expected = [
        # ── Sub-search 1: start=(0,3), goal=(0,0) ──
        {'type': 'push', 'state': (0, 3), 'g': 0, 'parent': None, 'h': 3, 'f': 3},
        {'type': 'pop',  'state': (0, 3), 'g': 0, 'h': 3, 'f': 3},
        {'type': 'push', 'state': (1, 3), 'g': 1, 'parent': (0, 3), 'h': 4, 'f': 5},
        {'type': 'pop',  'state': (1, 3), 'g': 1, 'h': 4, 'f': 5},
        {'type': 'push', 'state': (2, 3), 'g': 2, 'parent': (1, 3), 'h': 5, 'f': 7},
        {'type': 'pop',  'state': (2, 3), 'g': 2, 'h': 5, 'f': 7},
        {'type': 'push', 'state': (3, 3), 'g': 3, 'parent': (2, 3), 'h': 6, 'f': 9},
        {'type': 'push', 'state': (2, 2), 'g': 3, 'parent': (2, 3), 'h': 4, 'f': 7},
        {'type': 'pop',  'state': (2, 2), 'g': 3, 'h': 4, 'f': 7},
        {'type': 'push', 'state': (3, 2), 'g': 4, 'parent': (2, 2), 'h': 5, 'f': 9},
        {'type': 'push', 'state': (2, 1), 'g': 4, 'parent': (2, 2), 'h': 3, 'f': 7},
        {'type': 'pop',  'state': (2, 1), 'g': 4, 'h': 3, 'f': 7},
        {'type': 'push', 'state': (1, 1), 'g': 5, 'parent': (2, 1), 'h': 2, 'f': 7},
        {'type': 'push', 'state': (3, 1), 'g': 5, 'parent': (2, 1), 'h': 4, 'f': 9},
        {'type': 'push', 'state': (2, 0), 'g': 5, 'parent': (2, 1), 'h': 2, 'f': 7},
        {'type': 'pop',  'state': (1, 1), 'g': 5, 'h': 2, 'f': 7},
        {'type': 'push', 'state': (0, 1), 'g': 6, 'parent': (1, 1), 'h': 1, 'f': 7},
        {'type': 'push', 'state': (1, 0), 'g': 6, 'parent': (1, 1), 'h': 1, 'f': 7},
        {'type': 'pop',  'state': (0, 1), 'g': 6, 'h': 1, 'f': 7},
        {'type': 'push', 'state': (0, 0), 'g': 7, 'parent': (0, 1), 'h': 0, 'f': 7},
        {'type': 'pop',  'state': (0, 0), 'g': 7, 'h': 0, 'f': 7},
        {'type': 'on_start', 'state': (0, 3), 'g': 7, 'reason': 'expanded', 'start_index': 0},
        # ── Sub-search 2: start=(3,3), goal=(0,0) ──
        {'type': 'push', 'state': (3, 3), 'g': 0, 'parent': None, 'h': 6, 'f': 6},
        {'type': 'pop',  'state': (3, 3), 'g': 0, 'h': 6, 'f': 6},
        {'type': 'push', 'state': (2, 3), 'g': 1, 'parent': (3, 3), 'h': 5, 'f': 6},
        {'type': 'push', 'state': (3, 2), 'g': 1, 'parent': (3, 3), 'h': 5, 'f': 6},
        {'type': 'pop',  'state': (2, 3), 'g': 1, 'h': 5, 'f': 6},
        {'type': 'push', 'state': (1, 3), 'g': 2, 'parent': (2, 3), 'h': 4, 'f': 6},
        {'type': 'push', 'state': (2, 2), 'g': 2, 'parent': (2, 3), 'h': 4, 'f': 6},
        {'type': 'pop',  'state': (1, 3), 'g': 2, 'h': 4, 'f': 6},
        {'type': 'push', 'state': (0, 3), 'g': 3, 'parent': (1, 3), 'h': 3, 'f': 6},
        {'type': 'pop',  'state': (0, 3), 'g': 3, 'h': 3, 'f': 6},
        {'type': 'pop',  'state': (2, 2), 'g': 2, 'h': 4, 'f': 6},
        {'type': 'push', 'state': (2, 1), 'g': 3, 'parent': (2, 2), 'h': 3, 'f': 6},
        {'type': 'pop',  'state': (2, 1), 'g': 3, 'h': 3, 'f': 6},
        {'type': 'push', 'state': (1, 1), 'g': 4, 'parent': (2, 1), 'h': 2, 'f': 6},
        {'type': 'push', 'state': (3, 1), 'g': 4, 'parent': (2, 1), 'h': 4, 'f': 8},
        {'type': 'push', 'state': (2, 0), 'g': 4, 'parent': (2, 1), 'h': 2, 'f': 6},
        {'type': 'pop',  'state': (1, 1), 'g': 4, 'h': 2, 'f': 6},
        {'type': 'push', 'state': (0, 1), 'g': 5, 'parent': (1, 1), 'h': 1, 'f': 6},
        {'type': 'push', 'state': (1, 0), 'g': 5, 'parent': (1, 1), 'h': 1, 'f': 6},
        {'type': 'pop',  'state': (0, 1), 'g': 5, 'h': 1, 'f': 6},
        {'type': 'push', 'state': (0, 0), 'g': 6, 'parent': (0, 1), 'h': 0, 'f': 6},
        {'type': 'pop',  'state': (0, 0), 'g': 6, 'h': 0, 'f': 6},
        {'type': 'on_start', 'state': (3, 3), 'g': 6, 'reason': 'expanded', 'start_index': 1},
    ]
    assert actual == expected
