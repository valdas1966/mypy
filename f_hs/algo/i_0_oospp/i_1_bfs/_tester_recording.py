"""
============================================================================
 BFS — full event-stream pins. One test per scenario; each
 asserts the complete normalized event list (every field of
 every event, `duration` stripped). Drift in ordering, payload,
 or schema surfaces as a list-diff.

 Scenarios:
   - canonical OOSPP grid (`grid_4x4_obstacle`).
   - graph_abc (toy 3-state linear).
   - graph_decrease (weighted; FIFO re-encounter, no relax).
   - grid_3x3 (open 3x3, BFS-layer expansion).
============================================================================
"""

from f_hs.algo.i_0_oospp.i_1_bfs import BFS
from f_hs.algo.u_event_normalize import normalize
from f_hs.problem import ProblemSPP
from f_hs.problem.i_1_grid import ProblemGrid


def test_recording_canonical_oospp() -> None:
    """
    ========================================================================
     Pin the FULL event stream for BFS on the canonical OOSPP
     problem (28 events, BFS layer order, no h/f).
    ========================================================================
    """
    p = ProblemGrid.Factory.grid_4x4_obstacle()
    algo = BFS(problem=p, is_recording=True)
    algo.run()
    actual = [normalize(e) for e in algo.recorder.events]
    expected = [
        {'type': 'push', 'state': (0, 0), 'g': 0, 'parent': None},
        {'type': 'pop', 'state': (0, 0), 'g': 0},
        {'type': 'push', 'state': (0, 1), 'g': 1, 'parent': (0, 0)},
        {'type': 'push', 'state': (1, 0), 'g': 1, 'parent': (0, 0)},
        {'type': 'pop', 'state': (0, 1), 'g': 1},
        {'type': 'push', 'state': (1, 1), 'g': 2, 'parent': (0, 1)},
        {'type': 'pop', 'state': (1, 0), 'g': 1},
        {'type': 'push', 'state': (2, 0), 'g': 2, 'parent': (1, 0)},
        {'type': 'pop', 'state': (1, 1), 'g': 2},
        {'type': 'push', 'state': (2, 1), 'g': 3, 'parent': (1, 1)},
        {'type': 'pop', 'state': (2, 0), 'g': 2},
        {'type': 'push', 'state': (3, 0), 'g': 3, 'parent': (2, 0)},
        {'type': 'pop', 'state': (2, 1), 'g': 3},
        {'type': 'push', 'state': (2, 2), 'g': 4, 'parent': (2, 1)},
        {'type': 'push', 'state': (3, 1), 'g': 4, 'parent': (2, 1)},
        {'type': 'pop', 'state': (3, 0), 'g': 3},
        {'type': 'pop', 'state': (2, 2), 'g': 4},
        {'type': 'push', 'state': (2, 3), 'g': 5, 'parent': (2, 2)},
        {'type': 'push', 'state': (3, 2), 'g': 5, 'parent': (2, 2)},
        {'type': 'pop', 'state': (3, 1), 'g': 4},
        {'type': 'pop', 'state': (2, 3), 'g': 5},
        {'type': 'push', 'state': (1, 3), 'g': 6, 'parent': (2, 3)},
        {'type': 'push', 'state': (3, 3), 'g': 6, 'parent': (2, 3)},
        {'type': 'pop', 'state': (3, 2), 'g': 5},
        {'type': 'pop', 'state': (1, 3), 'g': 6},
        {'type': 'push', 'state': (0, 3), 'g': 7, 'parent': (1, 3)},
        {'type': 'pop', 'state': (3, 3), 'g': 6},
        {'type': 'pop', 'state': (0, 3), 'g': 7},
    ]
    assert actual == expected


def test_recording_graph_abc() -> None:
    """
    ========================================================================
     Pin the FULL event stream for BFS on graph A → B → C.
    ========================================================================
    """
    algo = BFS(problem=ProblemSPP.Factory.graph_abc(),
               is_recording=True)
    algo.run()
    actual = [normalize(e) for e in algo.recorder.events]
    expected = [
        {'type': 'push', 'state': 'A', 'g': 0, 'parent': None},
        {'type': 'pop',  'state': 'A', 'g': 0},
        {'type': 'push', 'state': 'B', 'g': 1, 'parent': 'A'},
        {'type': 'pop',  'state': 'B', 'g': 1},
        {'type': 'push', 'state': 'C', 'g': 2, 'parent': 'B'},
        {'type': 'pop',  'state': 'C', 'g': 2},
    ]
    assert actual == expected


def test_recording_graph_decrease() -> None:
    """
    ========================================================================
     Pin the FULL event stream for BFS on the weighted
     decrease-graph (S → A/B → X with w(B,X) = 0). FIFO pops
     A before B; A pushes X with g=2; B re-encounters X with
     new_g = 1 + 0 = 1 < 2, but FIFO has NO decrease op, so the
     better path is NOT adopted — no `decrease_g` event, and X
     pops with its original g=2 (BFS is non-optimal on weighted
     graphs; relaxation is A*'s job, not FIFO's).
    ========================================================================
    """
    algo = BFS.Factory.graph_decrease()
    algo._recorder.is_active = True
    algo.run()
    actual = [normalize(e) for e in algo.recorder.events]
    expected = [
        {'type': 'push', 'state': 'S', 'g': 0, 'parent': None},
        {'type': 'pop',  'state': 'S', 'g': 0},
        {'type': 'push', 'state': 'A', 'g': 1, 'parent': 'S'},
        {'type': 'push', 'state': 'B', 'g': 1, 'parent': 'S'},
        {'type': 'pop',  'state': 'A', 'g': 1},
        {'type': 'push', 'state': 'X', 'g': 2, 'parent': 'A'},
        {'type': 'pop',  'state': 'B', 'g': 1},
        {'type': 'pop',  'state': 'X', 'g': 2},
    ]
    assert actual == expected


def test_recording_grid_3x3() -> None:
    """
    ========================================================================
     Pin the FULL event stream for BFS on an open 3x3 grid
     from (0,0) to (2,2) — 18 events (9 push + 9 pop).
    ========================================================================
    """
    algo = BFS(problem=ProblemGrid.Factory.grid_3x3(),
               is_recording=True)
    algo.run()
    actual = [normalize(e) for e in algo.recorder.events]
    expected = [
        {'type': 'push', 'state': (0, 0), 'g': 0, 'parent': None},
        {'type': 'pop',  'state': (0, 0), 'g': 0},
        {'type': 'push', 'state': (0, 1), 'g': 1, 'parent': (0, 0)},
        {'type': 'push', 'state': (1, 0), 'g': 1, 'parent': (0, 0)},
        {'type': 'pop',  'state': (0, 1), 'g': 1},
        {'type': 'push', 'state': (0, 2), 'g': 2, 'parent': (0, 1)},
        {'type': 'push', 'state': (1, 1), 'g': 2, 'parent': (0, 1)},
        {'type': 'pop',  'state': (1, 0), 'g': 1},
        {'type': 'push', 'state': (2, 0), 'g': 2, 'parent': (1, 0)},
        {'type': 'pop',  'state': (0, 2), 'g': 2},
        {'type': 'push', 'state': (1, 2), 'g': 3, 'parent': (0, 2)},
        {'type': 'pop',  'state': (1, 1), 'g': 2},
        {'type': 'push', 'state': (2, 1), 'g': 3, 'parent': (1, 1)},
        {'type': 'pop',  'state': (2, 0), 'g': 2},
        {'type': 'pop',  'state': (1, 2), 'g': 3},
        {'type': 'push', 'state': (2, 2), 'g': 4, 'parent': (1, 2)},
        {'type': 'pop',  'state': (2, 1), 'g': 3},
        {'type': 'pop',  'state': (2, 2), 'g': 4},
    ]
    assert actual == expected
