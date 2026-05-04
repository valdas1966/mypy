"""
============================================================================
 KAStarInc — full event-stream pins. One test per scenario;
 each asserts the complete normalized event list (every field
 of every event, `duration` stripped). KAStarInc emits OMSPP-
 specific meta-events around its sub-search transitions:
 `on_goal`, `update_frontier`, `update_heuristic`.

 Scenarios:
   - canonical OMSPP grid (3 goals): exercises 2 sub-search
     transitions, fast-path on the third goal.
   - grid_4x4_obstacle 2-goal: exercises 1 sub-search
     transition with 4-state `update_heuristic` cluster.
============================================================================
"""

from f_hs.algo.i_1_omspp.i_1_kastar_inc import KAStarInc
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
     Pin the FULL event stream for KAStarInc on the canonical
     OMSPP problem.
    ========================================================================
    """
    p = ProblemGrid.Factory.grid_4x4_obstacle_omspp()
    algo = KAStarInc(problem=p,
                     h=lambda s, g: float(s.distance(g)),
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
        {'type': 'on_goal', 'state': (0, 3), 'g': 7, 'reason': 'expanded', 'goal_index': 0},
        {'type': 'update_frontier', 'num_nodes': 4, 'next_goal_index': 1},
        {'type': 'update_heuristic', 'state': (2, 0), 'h_old': 5, 'h_new': 1},
        {'type': 'update_heuristic', 'state': (3, 3), 'h_old': 3, 'h_new': 3},
        {'type': 'update_heuristic', 'state': (3, 2), 'h_old': 4, 'h_new': 2},
        {'type': 'update_heuristic', 'state': (3, 1), 'h_old': 5, 'h_new': 1},
        {'type': 'pop', 'state': (2, 0), 'g': 2, 'h': 1, 'f': 3},
        {'type': 'push', 'state': (3, 0), 'g': 3, 'parent': (2, 0), 'h': 0, 'f': 3},
        {'type': 'pop', 'state': (3, 0), 'g': 3, 'h': 0, 'f': 3},
        {'type': 'on_goal', 'state': (3, 0), 'g': 3, 'reason': 'expanded', 'goal_index': 1},
        {'type': 'update_frontier', 'num_nodes': 3, 'next_goal_index': 2},
        {'type': 'update_heuristic', 'state': (3, 1), 'h_old': 1, 'h_new': 2},
        {'type': 'update_heuristic', 'state': (3, 2), 'h_old': 2, 'h_new': 1},
        {'type': 'update_heuristic', 'state': (3, 3), 'h_old': 3, 'h_new': 0},
        {'type': 'pop', 'state': (3, 3), 'g': 6, 'h': 0, 'f': 6},
        {'type': 'on_goal', 'state': (3, 3), 'g': 6, 'reason': 'expanded', 'goal_index': 2},
    ]
    assert actual == expected


def test_recording_grid_4x4_obstacle_2goals() -> None:
    """
    ========================================================================
     Pin the FULL event stream for KAStarInc on `grid_4x4_obstacle`
     with goals=[(0,3), (3,3)]. Sub-search 1 closes (0,3) at g=7;
     sub-search 2 resumes from shared state and closes (3,3) at
     g=6. 30 events.
    ========================================================================
    """
    p = _grid_4x4_obstacle_2goals()
    algo = KAStarInc(problem=p,
                     h=lambda s, g: float(s.distance(g)),
                     is_recording=True)
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
        {'type': 'on_goal', 'state': (0, 3), 'g': 7, 'reason': 'expanded', 'goal_index': 0},
        {'type': 'update_frontier', 'num_nodes': 4, 'next_goal_index': 1},
        {'type': 'update_heuristic', 'state': (2, 0), 'h_old': 5, 'h_new': 4},
        {'type': 'update_heuristic', 'state': (3, 3), 'h_old': 3, 'h_new': 0},
        {'type': 'update_heuristic', 'state': (3, 2), 'h_old': 4, 'h_new': 1},
        {'type': 'update_heuristic', 'state': (3, 1), 'h_old': 5, 'h_new': 2},
        {'type': 'pop',  'state': (3, 3), 'g': 6, 'h': 0, 'f': 6},
        {'type': 'on_goal', 'state': (3, 3), 'g': 6, 'reason': 'expanded', 'goal_index': 1},
    ]
    assert actual == expected
