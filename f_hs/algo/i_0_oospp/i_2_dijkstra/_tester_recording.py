"""
============================================================================
 Dijkstra — full event-stream pins. One test per scenario;
 each asserts the complete normalized event list (every field
 of every event, `duration` stripped). The full pin
 implicitly verifies `Dijkstra._enrich_event` no-op (no h/f
 fields on any event) — any drift would surface as a list-diff.
============================================================================
"""

from f_hs.algo.i_0_oospp.i_2_dijkstra import Dijkstra
from f_hs.algo.u_event_normalize import normalize
from f_hs.problem import ProblemSPP
from f_hs.problem.i_1_grid import ProblemGrid


def test_recording_canonical_oospp() -> None:
    """
    ========================================================================
     Pin the FULL event stream for Dijkstra on the canonical
     OOSPP problem (28 events).
    ========================================================================
    """
    p = ProblemGrid.Factory.grid_4x4_obstacle()
    algo = Dijkstra(problem=p, is_recording=True)
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
     Pin the FULL event stream for Dijkstra on A → B → C.
    ========================================================================
    """
    algo = Dijkstra(problem=ProblemSPP.Factory.graph_abc(),
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


def test_recording_graph_diamond() -> None:
    """
    ========================================================================
     Pin the FULL event stream for Dijkstra on diamond
     A → {B, C} → D. Unlike AStar, Dijkstra expands BOTH B
     and C (no heuristic to prefer one g=1 state at the
     frontier). State tiebreak puts B before C.
    ========================================================================
    """
    algo = Dijkstra(problem=ProblemSPP.Factory.graph_diamond(),
                    is_recording=True)
    algo.run()
    actual = [normalize(e) for e in algo.recorder.events]
    expected = [
        {'type': 'push', 'state': 'A', 'g': 0, 'parent': None},
        {'type': 'pop',  'state': 'A', 'g': 0},
        {'type': 'push', 'state': 'B', 'g': 1, 'parent': 'A'},
        {'type': 'push', 'state': 'C', 'g': 1, 'parent': 'A'},
        {'type': 'pop',  'state': 'B', 'g': 1},
        {'type': 'push', 'state': 'D', 'g': 2, 'parent': 'B'},
        {'type': 'pop',  'state': 'C', 'g': 1},
        {'type': 'pop',  'state': 'D', 'g': 2},
    ]
    assert actual == expected


def test_recording_graph_decrease() -> None:
    """
    ========================================================================
     Pin the FULL event stream for Dijkstra on the weighted
     decrease-graph (S → A/B → X, w(B,X)=0). State tiebreak
     pops A first; B re-parents X via `decrease_g`. Verifies
     `decrease_g` schema (no h/f fields) via the full pin.
    ========================================================================
    """
    algo = Dijkstra.Factory.graph_decrease()
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
        {'type': 'decrease_g', 'state': 'X', 'g': 1, 'parent': 'B'},
        {'type': 'pop',  'state': 'X', 'g': 1},
    ]
    assert actual == expected


def test_recording_grid_3x3() -> None:
    """
    ========================================================================
     Pin the FULL event stream for Dijkstra on open 3x3 grid
     (0,0) → (2,2). On unit-cost edges and with State
     tiebreak, Dijkstra's expansion order matches BFS exactly.
    ========================================================================
    """
    algo = Dijkstra(problem=ProblemGrid.Factory.grid_3x3(),
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
