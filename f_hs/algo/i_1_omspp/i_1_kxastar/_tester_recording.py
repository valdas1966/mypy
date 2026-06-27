"""
============================================================================
 KxAStarOMSPP — full event-stream pins. One test per scenario;
 each asserts the complete normalized event list (every field
 of every event, `duration` stripped). KxAStarOMSPP emits a
 SUBSET of the canonical OMSPP 5-event schema:

   - push / pop / decrease_g  — from each inner AStar via the
                                shared recorder.
   - on_goal                  — per goal at sub-search end;
                                reason ∈ {expanded,
                                already_reached, unreachable}.
                                `already_closed` is NEVER
                                emitted (no shared CLOSED set).
   - update_frontier          — NEVER emitted (no shared
                                frontier transition between
                                sub-searches).

 No state sharing means every sub-search starts from (0,0)
 again under its own h(·, goal_i). The event stream concatenates
 k independent AStar event streams interleaved with per-goal
 `on_goal` markers.

 Scenarios:
   - canonical OMSPP grid (3 goals): three independent
     sub-searches from (0,0) — to (0,3), then (3,0), then
     (3,3). 55 events total.
   - grid_4x4_obstacle 2-goal: two independent sub-searches
     from (0,0) — to (0,3), then (3,3). 43 events total.
============================================================================
"""

from f_hs.algo.i_1_omspp.i_1_kxastar import KxAStarOMSPP
from f_hs.algo.u_event_normalize import normalize
from f_hs.problem.i_1_grid import ProblemGrid


def _grid_4x4_obstacle_2goals() -> ProblemGrid:
    """
    ========================================================================
     4x4 grid with wall cells at (0,2) and (1,2). Start (0,0),
     goals [(0,3), (3,3)]. Optimal costs 7 and 6.
    ========================================================================
    """
    p = ProblemGrid.Factory.grid_4x4_obstacle()
    grid = p.grid
    p._goals = [p._states[grid[0][3]], p._states[grid[3][3]]]
    return p


def test_recording_canonical_omspp() -> None:
    """
    ========================================================================
     Pin the FULL event stream for KxAStarOMSPP on the canonical
     OMSPP problem. Three independent A* sub-searches, no
     state sharing: each starts with a fresh `push (0,0)`
     under its own h. No `update_frontier` events, no lazy
     re-push events.
    ========================================================================
    """
    p = ProblemGrid.Factory.grid_4x4_obstacle_omspp()
    algo = KxAStarOMSPP(problem=p,
                   h=lambda s, g: float(s.key.distance(g.key)),
                   is_recording=True)
    algo.run()
    actual = [normalize(e) for e in algo.recorder.events]
    expected = [
        # ── Sub-search 1: goal (0,3); h = Manhattan to (0,3) ──
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
        {'type': 'on_goal', 'state': (0, 3), 'g': 7, 'reason': 'expanded', 'goal_index': 0},
        # ── Sub-search 2: goal (3,0); h = Manhattan to (3,0) ──
        {'type': 'push', 'state': (0, 0), 'g': 0, 'parent': None, 'h': 3, 'f': 3},
        {'type': 'pop',  'state': (0, 0), 'g': 0, 'h': 3, 'f': 3},
        {'type': 'push', 'state': (0, 1), 'g': 1, 'parent': (0, 0), 'h': 4, 'f': 5},
        {'type': 'push', 'state': (1, 0), 'g': 1, 'parent': (0, 0), 'h': 2, 'f': 3},
        {'type': 'pop',  'state': (1, 0), 'g': 1, 'h': 2, 'f': 3},
        {'type': 'push', 'state': (1, 1), 'g': 2, 'parent': (1, 0), 'h': 3, 'f': 5},
        {'type': 'push', 'state': (2, 0), 'g': 2, 'parent': (1, 0), 'h': 1, 'f': 3},
        {'type': 'pop',  'state': (2, 0), 'g': 2, 'h': 1, 'f': 3},
        {'type': 'push', 'state': (2, 1), 'g': 3, 'parent': (2, 0), 'h': 2, 'f': 5},
        {'type': 'push', 'state': (3, 0), 'g': 3, 'parent': (2, 0), 'h': 0, 'f': 3},
        {'type': 'pop',  'state': (3, 0), 'g': 3, 'h': 0, 'f': 3},
        {'type': 'on_goal', 'state': (3, 0), 'g': 3, 'reason': 'expanded', 'goal_index': 1},
        # ── Sub-search 3: goal (3,3); h = Manhattan to (3,3) ──
        {'type': 'push', 'state': (0, 0), 'g': 0, 'parent': None, 'h': 6, 'f': 6},
        {'type': 'pop',  'state': (0, 0), 'g': 0, 'h': 6, 'f': 6},
        {'type': 'push', 'state': (0, 1), 'g': 1, 'parent': (0, 0), 'h': 5, 'f': 6},
        {'type': 'push', 'state': (1, 0), 'g': 1, 'parent': (0, 0), 'h': 5, 'f': 6},
        {'type': 'pop',  'state': (0, 1), 'g': 1, 'h': 5, 'f': 6},
        {'type': 'push', 'state': (1, 1), 'g': 2, 'parent': (0, 1), 'h': 4, 'f': 6},
        {'type': 'pop',  'state': (1, 1), 'g': 2, 'h': 4, 'f': 6},
        {'type': 'push', 'state': (2, 1), 'g': 3, 'parent': (1, 1), 'h': 3, 'f': 6},
        {'type': 'pop',  'state': (2, 1), 'g': 3, 'h': 3, 'f': 6},
        {'type': 'push', 'state': (2, 2), 'g': 4, 'parent': (2, 1), 'h': 2, 'f': 6},
        {'type': 'push', 'state': (3, 1), 'g': 4, 'parent': (2, 1), 'h': 2, 'f': 6},
        {'type': 'push', 'state': (2, 0), 'g': 4, 'parent': (2, 1), 'h': 4, 'f': 8},
        {'type': 'pop',  'state': (2, 2), 'g': 4, 'h': 2, 'f': 6},
        {'type': 'push', 'state': (2, 3), 'g': 5, 'parent': (2, 2), 'h': 1, 'f': 6},
        {'type': 'push', 'state': (3, 2), 'g': 5, 'parent': (2, 2), 'h': 1, 'f': 6},
        {'type': 'pop',  'state': (2, 3), 'g': 5, 'h': 1, 'f': 6},
        {'type': 'push', 'state': (1, 3), 'g': 6, 'parent': (2, 3), 'h': 2, 'f': 8},
        {'type': 'push', 'state': (3, 3), 'g': 6, 'parent': (2, 3), 'h': 0, 'f': 6},
        {'type': 'pop',  'state': (3, 3), 'g': 6, 'h': 0, 'f': 6},
        {'type': 'on_goal', 'state': (3, 3), 'g': 6, 'reason': 'expanded', 'goal_index': 2},
    ]
    assert actual == expected


def test_recording_grid_4x4_obstacle_2goals() -> None:
    """
    ========================================================================
     Pin the FULL event stream for KxAStarOMSPP on `grid_4x4_obstacle`
     with goals=[(0,3), (3,3)]. Two INDEPENDENT sub-searches:
     sub-search 1 finds (0,3) at g=7, sub-search 2 starts
     fresh from (0,0) under h(·, (3,3)) and finds (3,3) at
     g=6. No `update_frontier`, no lazy re-push.
    ========================================================================
    """
    p = _grid_4x4_obstacle_2goals()
    algo = KxAStarOMSPP(problem=p,
                   h=lambda s, g: float(s.key.distance(g.key)),
                   is_recording=True)
    algo.run()
    actual = [normalize(e) for e in algo.recorder.events]
    expected = [
        # ── Sub-search 1: goal (0,3); h = Manhattan to (0,3) ──
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
        {'type': 'on_goal', 'state': (0, 3), 'g': 7, 'reason': 'expanded', 'goal_index': 0},
        # ── Sub-search 2: goal (3,3); h = Manhattan to (3,3) ──
        {'type': 'push', 'state': (0, 0), 'g': 0, 'parent': None, 'h': 6, 'f': 6},
        {'type': 'pop',  'state': (0, 0), 'g': 0, 'h': 6, 'f': 6},
        {'type': 'push', 'state': (0, 1), 'g': 1, 'parent': (0, 0), 'h': 5, 'f': 6},
        {'type': 'push', 'state': (1, 0), 'g': 1, 'parent': (0, 0), 'h': 5, 'f': 6},
        {'type': 'pop',  'state': (0, 1), 'g': 1, 'h': 5, 'f': 6},
        {'type': 'push', 'state': (1, 1), 'g': 2, 'parent': (0, 1), 'h': 4, 'f': 6},
        {'type': 'pop',  'state': (1, 1), 'g': 2, 'h': 4, 'f': 6},
        {'type': 'push', 'state': (2, 1), 'g': 3, 'parent': (1, 1), 'h': 3, 'f': 6},
        {'type': 'pop',  'state': (2, 1), 'g': 3, 'h': 3, 'f': 6},
        {'type': 'push', 'state': (2, 2), 'g': 4, 'parent': (2, 1), 'h': 2, 'f': 6},
        {'type': 'push', 'state': (3, 1), 'g': 4, 'parent': (2, 1), 'h': 2, 'f': 6},
        {'type': 'push', 'state': (2, 0), 'g': 4, 'parent': (2, 1), 'h': 4, 'f': 8},
        {'type': 'pop',  'state': (2, 2), 'g': 4, 'h': 2, 'f': 6},
        {'type': 'push', 'state': (2, 3), 'g': 5, 'parent': (2, 2), 'h': 1, 'f': 6},
        {'type': 'push', 'state': (3, 2), 'g': 5, 'parent': (2, 2), 'h': 1, 'f': 6},
        {'type': 'pop',  'state': (2, 3), 'g': 5, 'h': 1, 'f': 6},
        {'type': 'push', 'state': (1, 3), 'g': 6, 'parent': (2, 3), 'h': 2, 'f': 8},
        {'type': 'push', 'state': (3, 3), 'g': 6, 'parent': (2, 3), 'h': 0, 'f': 6},
        {'type': 'pop',  'state': (3, 3), 'g': 6, 'h': 0, 'f': 6},
        {'type': 'on_goal', 'state': (3, 3), 'g': 6, 'reason': 'expanded', 'goal_index': 1},
    ]
    assert actual == expected
