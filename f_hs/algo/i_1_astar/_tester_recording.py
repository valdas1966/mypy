from f_hs.algo.i_1_astar import AStar
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
     Simple AStar on A -> B -> C with admissible h = {A:2, B:1,
     C:0}. Every event carries h and f (int-cast). Pop events do
     NOT carry a parent key. No is_cached / is_bounded flags.
    ========================================================================
    """
    h_map = {'A': 2.0, 'B': 1.0, 'C': 0.0}
    algo = AStar(problem=ProblemSPP.Factory.graph_abc(),
                 h=lambda s: h_map.get(s.key, 0.0),
                 is_recording=True)
    assert type(algo) is AStar
    algo.run()
    actual = [_normalize(e) for e in algo.recorder.events]
    expected = [
        {'type': 'push', 'state': 'A', 'g': 0, 'parent': None, 'h': 2, 'f': 2},
        {'type': 'pop',  'state': 'A', 'g': 0, 'h': 2, 'f': 2},
        {'type': 'push', 'state': 'B', 'g': 1, 'parent': 'A', 'h': 1, 'f': 2},
        {'type': 'pop',  'state': 'B', 'g': 1, 'h': 1, 'f': 2},
        {'type': 'push', 'state': 'C', 'g': 2, 'parent': 'B', 'h': 0, 'f': 2},
        {'type': 'pop',  'state': 'C', 'g': 2, 'h': 0, 'f': 2},
    ]
    assert actual == expected
    for e in actual:
        assert 'is_cached' not in e
        assert 'is_bounded' not in e


def test_recording_full_event_sequence_on_graph_diamond() -> None:
    """
    ========================================================================
     Diamond graph A -> {B, C} -> D with h = {A:2, B:1, C:1, D:0}.
     B and C tie on (f=2, -g=-1) — State tiebreak picks B.
    ========================================================================
    """
    h_map = {'A': 2.0, 'B': 1.0, 'C': 1.0, 'D': 0.0}
    algo = AStar(problem=ProblemSPP.Factory.graph_diamond(),
                 h=lambda s: h_map.get(s.key, 0.0),
                 is_recording=True)
    algo.run()
    actual = [_normalize(e) for e in algo.recorder.events]
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
    popped = [e['state'] for e in actual if e['type'] == 'pop']
    assert 'C' not in popped


def test_recording_full_event_sequence_on_graph_decrease() -> None:
    """
    ========================================================================
     Weighted decrease-graph (S -> A/B -> X with w(B,X) = 0), h=0.
     Exercises `decrease_g` event with AStar's h/f enrichment.
    ========================================================================
    """
    algo = AStar.Factory.graph_decrease()
    algo._recorder.is_active = True
    sol = algo.run()
    assert sol.cost == 1.0
    actual = [_normalize(e) for e in algo.recorder.events]
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
    decrs = [e for e in actual if e['type'] == 'decrease_g']
    assert len(decrs) == 1
    assert decrs[0]['parent'] == 'B'
    assert decrs[0]['g'] == 1
    assert decrs[0]['h'] == 0
    assert decrs[0]['f'] == decrs[0]['g'] + decrs[0]['h']


def test_recording_full_event_sequence_on_grid_3x3() -> None:
    """
    ========================================================================
     Open 3x3 grid (0,0) to (2,2), Manhattan h. Every state has
     f=4 (tight). 6 pushes + 6 pops.
    ========================================================================
    """
    problem = ProblemGrid.Factory.grid_3x3()
    goal = problem.goal
    algo = AStar(problem=problem,
                 h=lambda s: float(s.distance(goal)),
                 is_recording=True)
    algo.run()
    actual = [_normalize(e) for e in algo.recorder.events]
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
    for e in actual:
        assert e['f'] == e['g'] + e['h']


def test_recording_full_event_sequence_on_grid_3x3_obstacle(
        ) -> None:
    """
    ========================================================================
     3x3 grid with obstacle at (1,1). (0,0) -> (2,2). Obstacle
     cell never appears as state or parent.
    ========================================================================
    """
    problem = ProblemGrid.Factory.grid_3x3_obstacle()
    goal = problem.goal
    algo = AStar(problem=problem,
                 h=lambda s: float(s.distance(goal)),
                 is_recording=True)
    algo.run()
    actual = [_normalize(e) for e in algo.recorder.events]
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
    obstacle = (1, 1)
    for e in actual:
        assert e['state'] != obstacle
        if 'parent' in e and e['parent'] is not None:
            assert e['parent'] != obstacle


def test_recording_full_event_sequence_on_grid_4x4_obstacle(
        ) -> None:
    """
    ========================================================================
     4x4 grid with a vertical 2-cell wall at (0,2) and (1,2).
     (0,0) -> (0,3). 11 pushes + 11 pops = 22 events.
    ========================================================================
    """
    problem = ProblemGrid.Factory.grid_4x4_obstacle()
    goal = problem.goal
    algo = AStar(problem=problem,
                 h=lambda s: float(s.distance(goal)),
                 is_recording=True)
    algo.run()
    actual = [_normalize(e) for e in algo.recorder.events]
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
    obstacles = {(0, 2), (1, 2)}
    for e in actual:
        assert e['state'] not in obstacles
        if 'parent' in e and e['parent'] is not None:
            assert e['parent'] not in obstacles
