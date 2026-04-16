from f_hs.algo.i_1_bfs import BFS
from f_hs.problem import ProblemSPP
from f_hs.problem.i_1_grid import ProblemGrid


def _key_of(state) -> object:
    """
    ========================================================================
     Return a comparable Key for a State.
     Graph states (key=str) return the string as-is.
     Grid states (key=CellMap) return a (row, col) tuple.
    ========================================================================
    """
    k = state.key
    if hasattr(k, 'row') and hasattr(k, 'col'):
        return (k.row, k.col)
    return k


def _normalize(event: dict) -> dict:
    """
    ========================================================================
     Return a comparable copy of an Event:
     - duration removed (non-deterministic timing)
     - state and parent unwrapped to their keys
     Dict comparison then checks the exact keyset — a pop event
     accidentally carrying a parent key would fail the test.
    ========================================================================
    """
    out = {k: v for k, v in event.items() if k != 'duration'}
    out['state'] = _key_of(event['state'])
    if 'parent' in event:
        p = event['parent']
        out['parent'] = _key_of(p) if p is not None else None
    return out


def test_recording_full_event_sequence_on_graph_abc() -> None:
    """
    ========================================================================
     Assert the exact recorded event sequence for BFS on A -> B -> C.
     Dict comparison pins the schema per event type — pop events
     must NOT carry a parent key; push events MUST.
    ========================================================================
    """
    algo = BFS(problem=ProblemSPP.Factory.graph_abc(),
               is_recording=True)
    algo.run()
    actual = [_normalize(e) for e in algo.recorder.events]
    expected = [
        {'type': 'push', 'state': 'A', 'g': 0, 'parent': None},
        {'type': 'pop',  'state': 'A', 'g': 0},
        {'type': 'push', 'state': 'B', 'g': 1, 'parent': 'A'},
        {'type': 'pop',  'state': 'B', 'g': 1},
        {'type': 'push', 'state': 'C', 'g': 2, 'parent': 'B'},
        {'type': 'pop',  'state': 'C', 'g': 2},
    ]
    assert actual == expected


def test_recording_full_event_sequence_on_grid_3x3() -> None:
    """
    ========================================================================
     Assert the exact recorded event sequence for BFS on an open
     3x3 grid from (0,0) to (2,2). State keys are (row,col) tuples.
     Verifies recording works on CellMap-keyed states and on a
     full breadth-first layered expansion — 9 pushes + 9 pops.
    ========================================================================
    """
    algo = BFS(problem=ProblemGrid.Factory.grid_3x3(),
               is_recording=True)
    algo.run()
    actual = [_normalize(e) for e in algo.recorder.events]
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


def test_recording_full_event_sequence_on_grid_4x4_obstacle() -> None:
    """
    ========================================================================
     Assert the exact recorded event sequence for BFS on a 4x4
     grid with a vertical 2-cell wall at (0,2) and (1,2).
     Start (0,0) -> Goal (0,3). The wall forces a 7-step detour
     through row 2. Verifies obstacle-skipping during successor
     enumeration: cells (0,2) and (1,2) never appear as a state
     or parent in any recorded event. 14 pushes + 14 pops.
    ========================================================================
    """
    algo = BFS(problem=ProblemGrid.Factory.grid_4x4_obstacle(),
               is_recording=True)
    algo.run()
    actual = [_normalize(e) for e in algo.recorder.events]
    expected = [
        {'type': 'push', 'state': (0, 0), 'g': 0, 'parent': None},
        {'type': 'pop',  'state': (0, 0), 'g': 0},
        {'type': 'push', 'state': (0, 1), 'g': 1, 'parent': (0, 0)},
        {'type': 'push', 'state': (1, 0), 'g': 1, 'parent': (0, 0)},
        {'type': 'pop',  'state': (0, 1), 'g': 1},
        {'type': 'push', 'state': (1, 1), 'g': 2, 'parent': (0, 1)},
        {'type': 'pop',  'state': (1, 0), 'g': 1},
        {'type': 'push', 'state': (2, 0), 'g': 2, 'parent': (1, 0)},
        {'type': 'pop',  'state': (1, 1), 'g': 2},
        {'type': 'push', 'state': (2, 1), 'g': 3, 'parent': (1, 1)},
        {'type': 'pop',  'state': (2, 0), 'g': 2},
        {'type': 'push', 'state': (3, 0), 'g': 3, 'parent': (2, 0)},
        {'type': 'pop',  'state': (2, 1), 'g': 3},
        {'type': 'push', 'state': (2, 2), 'g': 4, 'parent': (2, 1)},
        {'type': 'push', 'state': (3, 1), 'g': 4, 'parent': (2, 1)},
        {'type': 'pop',  'state': (3, 0), 'g': 3},
        {'type': 'pop',  'state': (2, 2), 'g': 4},
        {'type': 'push', 'state': (2, 3), 'g': 5, 'parent': (2, 2)},
        {'type': 'push', 'state': (3, 2), 'g': 5, 'parent': (2, 2)},
        {'type': 'pop',  'state': (3, 1), 'g': 4},
        {'type': 'pop',  'state': (2, 3), 'g': 5},
        {'type': 'push', 'state': (1, 3), 'g': 6, 'parent': (2, 3)},
        {'type': 'push', 'state': (3, 3), 'g': 6, 'parent': (2, 3)},
        {'type': 'pop',  'state': (3, 2), 'g': 5},
        {'type': 'pop',  'state': (1, 3), 'g': 6},
        {'type': 'push', 'state': (0, 3), 'g': 7, 'parent': (1, 3)},
        {'type': 'pop',  'state': (3, 3), 'g': 6},
        {'type': 'pop',  'state': (0, 3), 'g': 7},
    ]
    assert actual == expected
    # Obstacle cells never appear as a state or parent
    obstacles = {(0, 2), (1, 2)}
    for e in actual:
        assert e['state'] not in obstacles
        if 'parent' in e and e['parent'] is not None:
            assert e['parent'] not in obstacles
