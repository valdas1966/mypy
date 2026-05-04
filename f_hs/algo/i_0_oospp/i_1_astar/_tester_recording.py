"""
============================================================================
 AStar — full event-stream pins. One test per scenario; each
 asserts the complete normalized event list (every field of
 every event, `duration` stripped).
============================================================================
"""

from f_hs.algo.i_0_oospp.i_1_astar import AStar
from f_hs.algo.u_event_normalize import normalize
from f_hs.problem import ProblemSPP
from f_hs.problem.i_1_grid import ProblemGrid


def test_recording_canonical_oospp() -> None:
    """
    ========================================================================
     Pin the FULL event stream for AStar on the canonical
     OOSPP problem (`grid_4x4_obstacle`, Manhattan h, 22 events).
    ========================================================================
    """
    p = ProblemGrid.Factory.grid_4x4_obstacle()
    goal = p.goal
    algo = AStar(problem=p,
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


def test_recording_graph_abc() -> None:
    """
    ========================================================================
     Pin the FULL event stream for AStar on A → B → C with
     admissible h = {A:2, B:1, C:0}.
    ========================================================================
    """
    h_map = {'A': 2.0, 'B': 1.0, 'C': 0.0}
    algo = AStar(problem=ProblemSPP.Factory.graph_abc(),
                 h=lambda s: h_map.get(s.key, 0.0),
                 is_recording=True)
    algo.run()
    actual = [normalize(e) for e in algo.recorder.events]
    expected = [
        {'type': 'push', 'state': 'A', 'g': 0, 'parent': None, 'h': 2, 'f': 2},
        {'type': 'pop',  'state': 'A', 'g': 0, 'h': 2, 'f': 2},
        {'type': 'push', 'state': 'B', 'g': 1, 'parent': 'A', 'h': 1, 'f': 2},
        {'type': 'pop',  'state': 'B', 'g': 1, 'h': 1, 'f': 2},
        {'type': 'push', 'state': 'C', 'g': 2, 'parent': 'B', 'h': 0, 'f': 2},
        {'type': 'pop',  'state': 'C', 'g': 2, 'h': 0, 'f': 2},
    ]
    assert actual == expected


def test_recording_graph_diamond() -> None:
    """
    ========================================================================
     Pin the FULL event stream for AStar on diamond
     A → {B, C} → D with h = {A:2, B:1, C:1, D:0}. State
     tiebreak picks B over C at the f=2 frontier.
    ========================================================================
    """
    h_map = {'A': 2.0, 'B': 1.0, 'C': 1.0, 'D': 0.0}
    algo = AStar(problem=ProblemSPP.Factory.graph_diamond(),
                 h=lambda s: h_map.get(s.key, 0.0),
                 is_recording=True)
    algo.run()
    actual = [normalize(e) for e in algo.recorder.events]
    expected = [
        {'type': 'push', 'state': 'A', 'g': 0, 'parent': None, 'h': 2, 'f': 2},
        {'type': 'pop',  'state': 'A', 'g': 0, 'h': 2, 'f': 2},
        {'type': 'push', 'state': 'B', 'g': 1, 'parent': 'A', 'h': 1, 'f': 2},
        {'type': 'push', 'state': 'C', 'g': 1, 'parent': 'A', 'h': 1, 'f': 2},
        {'type': 'pop',  'state': 'B', 'g': 1, 'h': 1, 'f': 2},
        {'type': 'push', 'state': 'D', 'g': 2, 'parent': 'B', 'h': 0, 'f': 2},
        {'type': 'pop',  'state': 'D', 'g': 2, 'h': 0, 'f': 2},
    ]
    assert actual == expected


def test_recording_graph_decrease() -> None:
    """
    ========================================================================
     Pin the FULL event stream for AStar on the weighted
     decrease-graph (S → A/B → X, w(B,X)=0, h=0). Exercises
     `decrease_g` with AStar's h/f enrichment.
    ========================================================================
    """
    algo = AStar.Factory.graph_decrease()
    algo._recorder.is_active = True
    algo.run()
    actual = [normalize(e) for e in algo.recorder.events]
    expected = [
        {'type': 'push', 'state': 'S', 'g': 0, 'parent': None, 'h': 0, 'f': 0},
        {'type': 'pop',  'state': 'S', 'g': 0, 'h': 0, 'f': 0},
        {'type': 'push', 'state': 'A', 'g': 1, 'parent': 'S', 'h': 0, 'f': 1},
        {'type': 'push', 'state': 'B', 'g': 1, 'parent': 'S', 'h': 0, 'f': 1},
        {'type': 'pop',  'state': 'A', 'g': 1, 'h': 0, 'f': 1},
        {'type': 'push', 'state': 'X', 'g': 2, 'parent': 'A', 'h': 0, 'f': 2},
        {'type': 'pop',  'state': 'B', 'g': 1, 'h': 0, 'f': 1},
        {'type': 'decrease_g', 'state': 'X', 'g': 1, 'parent': 'B', 'h': 0, 'f': 1},
        {'type': 'pop',  'state': 'X', 'g': 1, 'h': 0, 'f': 1},
    ]
    assert actual == expected


def test_recording_grid_3x3() -> None:
    """
    ========================================================================
     Pin the FULL event stream for AStar on open 3x3 grid
     (0,0) → (2,2), Manhattan h. Every state has f=4 (tight).
    ========================================================================
    """
    problem = ProblemGrid.Factory.grid_3x3()
    goal = problem.goal
    algo = AStar(problem=problem,
                 h=lambda s: float(s.distance(goal)),
                 is_recording=True)
    algo.run()
    actual = [normalize(e) for e in algo.recorder.events]
    expected = [
        {'type': 'push', 'state': (0, 0), 'g': 0, 'parent': None, 'h': 4, 'f': 4},
        {'type': 'pop',  'state': (0, 0), 'g': 0, 'h': 4, 'f': 4},
        {'type': 'push', 'state': (0, 1), 'g': 1, 'parent': (0, 0), 'h': 3, 'f': 4},
        {'type': 'push', 'state': (1, 0), 'g': 1, 'parent': (0, 0), 'h': 3, 'f': 4},
        {'type': 'pop',  'state': (0, 1), 'g': 1, 'h': 3, 'f': 4},
        {'type': 'push', 'state': (0, 2), 'g': 2, 'parent': (0, 1), 'h': 2, 'f': 4},
        {'type': 'push', 'state': (1, 1), 'g': 2, 'parent': (0, 1), 'h': 2, 'f': 4},
        {'type': 'pop',  'state': (0, 2), 'g': 2, 'h': 2, 'f': 4},
        {'type': 'push', 'state': (1, 2), 'g': 3, 'parent': (0, 2), 'h': 1, 'f': 4},
        {'type': 'pop',  'state': (1, 2), 'g': 3, 'h': 1, 'f': 4},
        {'type': 'push', 'state': (2, 2), 'g': 4, 'parent': (1, 2), 'h': 0, 'f': 4},
        {'type': 'pop',  'state': (2, 2), 'g': 4, 'h': 0, 'f': 4},
    ]
    assert actual == expected


def test_recording_grid_3x3_obstacle() -> None:
    """
    ========================================================================
     Pin the FULL event stream for AStar on 3x3 grid with
     obstacle at (1,1). (0,0) → (2,2). The full pin guarantees
     the obstacle cell never appears as a state or parent.
    ========================================================================
    """
    problem = ProblemGrid.Factory.grid_3x3_obstacle()
    goal = problem.goal
    algo = AStar(problem=problem,
                 h=lambda s: float(s.distance(goal)),
                 is_recording=True)
    algo.run()
    actual = [normalize(e) for e in algo.recorder.events]
    expected = [
        {'type': 'push', 'state': (0, 0), 'g': 0, 'parent': None, 'h': 4, 'f': 4},
        {'type': 'pop',  'state': (0, 0), 'g': 0, 'h': 4, 'f': 4},
        {'type': 'push', 'state': (0, 1), 'g': 1, 'parent': (0, 0), 'h': 3, 'f': 4},
        {'type': 'push', 'state': (1, 0), 'g': 1, 'parent': (0, 0), 'h': 3, 'f': 4},
        {'type': 'pop',  'state': (0, 1), 'g': 1, 'h': 3, 'f': 4},
        {'type': 'push', 'state': (0, 2), 'g': 2, 'parent': (0, 1), 'h': 2, 'f': 4},
        {'type': 'pop',  'state': (0, 2), 'g': 2, 'h': 2, 'f': 4},
        {'type': 'push', 'state': (1, 2), 'g': 3, 'parent': (0, 2), 'h': 1, 'f': 4},
        {'type': 'pop',  'state': (1, 2), 'g': 3, 'h': 1, 'f': 4},
        {'type': 'push', 'state': (2, 2), 'g': 4, 'parent': (1, 2), 'h': 0, 'f': 4},
        {'type': 'pop',  'state': (2, 2), 'g': 4, 'h': 0, 'f': 4},
    ]
    assert actual == expected
