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
     Assert the exact recorded event sequence for AStar on
     A -> B -> C with admissible h = {A:2, B:1, C:0}. Every event
     carries h and f (via AStar._enrich_event), f = g + h holds
     at each event, and pop events do NOT carry a parent key.
    ========================================================================
    """
    h_map = {'A': 2.0, 'B': 1.0, 'C': 0.0}
    algo = AStar(problem=ProblemSPP.Factory.graph_abc(),
                 h=lambda s: h_map.get(s.key, 0.0),
                 is_recording=True)
    algo.run()
    actual = [_normalize(e) for e in algo.recorder.events]
    expected = [
        {'type': 'push', 'state': 'A', 'g': 0,
         'parent': None, 'h': 2.0, 'f': 2.0},
        {'type': 'pop',  'state': 'A', 'g': 0,
         'h': 2.0, 'f': 2.0},
        {'type': 'push', 'state': 'B', 'g': 1,
         'parent': 'A', 'h': 1.0, 'f': 2.0},
        {'type': 'pop',  'state': 'B', 'g': 1,
         'h': 1.0, 'f': 2.0},
        {'type': 'push', 'state': 'C', 'g': 2,
         'parent': 'B', 'h': 0.0, 'f': 2.0},
        {'type': 'pop',  'state': 'C', 'g': 2,
         'h': 0.0, 'f': 2.0},
    ]
    assert actual == expected


def test_recording_full_event_sequence_on_graph_diamond() -> None:
    """
    ========================================================================
     Assert the exact recorded event sequence for AStar on the
     diamond graph A -> {B, C} -> D with h = {A:2, B:1, C:1, D:0}.
     B and C share the same priority (f=2, -g=-1) — the third
     priority element (State, Comparable via HasKey) breaks the
     tie deterministically ('B' < 'C'), so B is popped first and
     the goal D is reached via B without ever expanding C.
    ========================================================================
    """
    h_map = {'A': 2.0, 'B': 1.0, 'C': 1.0, 'D': 0.0}
    algo = AStar(problem=ProblemSPP.Factory.graph_diamond(),
                 h=lambda s: h_map.get(s.key, 0.0),
                 is_recording=True)
    algo.run()
    actual = [_normalize(e) for e in algo.recorder.events]
    expected = [
        {'type': 'push', 'state': 'A', 'g': 0,
         'parent': None, 'h': 2.0, 'f': 2.0},
        {'type': 'pop',  'state': 'A', 'g': 0,
         'h': 2.0, 'f': 2.0},
        {'type': 'push', 'state': 'B', 'g': 1,
         'parent': 'A', 'h': 1.0, 'f': 2.0},
        {'type': 'push', 'state': 'C', 'g': 1,
         'parent': 'A', 'h': 1.0, 'f': 2.0},
        {'type': 'pop',  'state': 'B', 'g': 1,
         'h': 1.0, 'f': 2.0},
        {'type': 'push', 'state': 'D', 'g': 2,
         'parent': 'B', 'h': 0.0, 'f': 2.0},
        {'type': 'pop',  'state': 'D', 'g': 2,
         'h': 0.0, 'f': 2.0},
    ]
    assert actual == expected
    # C pushed but never popped — goal D was reached via B first.
    popped = [e['state'] for e in actual if e['type'] == 'pop']
    assert 'C' not in popped


def test_recording_full_event_sequence_on_graph_decrease() -> None:
    """
    ========================================================================
     Assert the exact recorded event sequence for AStar on the
     weighted decrease-graph (S -> A/B -> X with w(B,X) = 0)
     using h = 0 throughout. A and B tie on (f=1, -g=-1); State
     tiebreak ('A' < 'B') pops A first; A pushes X with g=2;
     B pops next and re-parents X via `decrease_g` (new_g = 1).

     Pins, beyond the existing AStar tests:
       1. The `decrease_g` event type is emitted.
       2. AStar's `_enrich_event` runs on `decrease_g` too —
          the event carries `h` and `f`, not just `state` / `g`
          / `parent`.
       3. The `parent` and `g` on `decrease_g` reflect the NEW
          values (B, 1), not the previous ones (A, 2).
       4. f = g + h holds on the decrease_g event.
    ========================================================================
    """
    algo = AStar.Factory.graph_decrease()
    algo._recorder.is_active = True
    sol = algo.run()
    assert sol.cost == 1.0
    actual = [_normalize(e) for e in algo.recorder.events]
    expected = [
        {'type': 'push', 'state': 'S', 'g': 0, 'parent': None, 'h': 0.0, 'f': 0.0},
        {'type': 'pop',  'state': 'S', 'g': 0, 'h': 0.0, 'f': 0.0},
        {'type': 'push', 'state': 'A', 'g': 1, 'parent': 'S', 'h': 0.0, 'f': 1.0},
        {'type': 'push', 'state': 'B', 'g': 1, 'parent': 'S', 'h': 0.0, 'f': 1.0},
        {'type': 'pop',  'state': 'A', 'g': 1, 'h': 0.0, 'f': 1.0},
        {'type': 'push', 'state': 'X', 'g': 2, 'parent': 'A', 'h': 0.0, 'f': 2.0},
        {'type': 'pop',  'state': 'B', 'g': 1, 'h': 0.0, 'f': 1.0},
        {'type': 'decrease_g', 'state': 'X', 'g': 1, 'parent': 'B', 'h': 0.0, 'f': 1.0},
        {'type': 'pop',  'state': 'X', 'g': 1, 'h': 0.0, 'f': 1.0},
    ]
    assert actual == expected
    # Exactly one decrease_g; carries enriched h/f; new parent/g.
    decrs = [e for e in actual if e['type'] == 'decrease_g']
    assert len(decrs) == 1
    assert decrs[0]['parent'] == 'B'
    assert decrs[0]['g'] == 1
    assert decrs[0]['h'] == 0.0
    assert decrs[0]['f'] == decrs[0]['g'] + decrs[0]['h']


def test_recording_full_event_sequence_on_grid_3x3() -> None:
    """
    ========================================================================
     Assert the exact recorded event sequence for AStar on an open
     3x3 grid from (0,0) to (2,2) with Manhattan heuristic. Every
     state on the path has f = 4 (tight admissible heuristic), so
     (f,-g) ties are common — the State tiebreak picks the
     lexicographically smaller (row,col). Informed-search result:
     6 pushes + 6 pops (vs. BFS's 9+9).
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
        {'type': 'push', 'state': (0, 0), 'g': 0,
         'parent': None, 'h': 4.0, 'f': 4.0},
        {'type': 'pop',  'state': (0, 0), 'g': 0,
         'h': 4.0, 'f': 4.0},
        {'type': 'push', 'state': (0, 1), 'g': 1,
         'parent': (0, 0), 'h': 3.0, 'f': 4.0},
        {'type': 'push', 'state': (1, 0), 'g': 1,
         'parent': (0, 0), 'h': 3.0, 'f': 4.0},
        {'type': 'pop',  'state': (0, 1), 'g': 1,
         'h': 3.0, 'f': 4.0},
        {'type': 'push', 'state': (0, 2), 'g': 2,
         'parent': (0, 1), 'h': 2.0, 'f': 4.0},
        {'type': 'push', 'state': (1, 1), 'g': 2,
         'parent': (0, 1), 'h': 2.0, 'f': 4.0},
        {'type': 'pop',  'state': (0, 2), 'g': 2,
         'h': 2.0, 'f': 4.0},
        {'type': 'push', 'state': (1, 2), 'g': 3,
         'parent': (0, 2), 'h': 1.0, 'f': 4.0},
        {'type': 'pop',  'state': (1, 2), 'g': 3,
         'h': 1.0, 'f': 4.0},
        {'type': 'push', 'state': (2, 2), 'g': 4,
         'parent': (1, 2), 'h': 0.0, 'f': 4.0},
        {'type': 'pop',  'state': (2, 2), 'g': 4,
         'h': 0.0, 'f': 4.0},
    ]
    assert actual == expected
    # Every event has f = g + h.
    for e in actual:
        assert e['f'] == e['g'] + e['h']


def test_recording_full_event_sequence_on_grid_3x3_obstacle() -> None:
    """
    ========================================================================
     Assert the exact recorded event sequence for AStar on a 3x3
     grid with obstacle at (1,1), from (0,0) to (2,2), Manhattan h.
     Obstacle cell (1,1) never appears as state or parent in any
     event. The search still finds cost 4 (going around the
     obstacle via the top-right or bottom-left corridor).
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
        {'type': 'push', 'state': (0, 0), 'g': 0,
         'parent': None, 'h': 4.0, 'f': 4.0},
        {'type': 'pop',  'state': (0, 0), 'g': 0,
         'h': 4.0, 'f': 4.0},
        {'type': 'push', 'state': (0, 1), 'g': 1,
         'parent': (0, 0), 'h': 3.0, 'f': 4.0},
        {'type': 'push', 'state': (1, 0), 'g': 1,
         'parent': (0, 0), 'h': 3.0, 'f': 4.0},
        {'type': 'pop',  'state': (0, 1), 'g': 1,
         'h': 3.0, 'f': 4.0},
        {'type': 'push', 'state': (0, 2), 'g': 2,
         'parent': (0, 1), 'h': 2.0, 'f': 4.0},
        {'type': 'pop',  'state': (0, 2), 'g': 2,
         'h': 2.0, 'f': 4.0},
        {'type': 'push', 'state': (1, 2), 'g': 3,
         'parent': (0, 2), 'h': 1.0, 'f': 4.0},
        {'type': 'pop',  'state': (1, 2), 'g': 3,
         'h': 1.0, 'f': 4.0},
        {'type': 'push', 'state': (2, 2), 'g': 4,
         'parent': (1, 2), 'h': 0.0, 'f': 4.0},
        {'type': 'pop',  'state': (2, 2), 'g': 4,
         'h': 0.0, 'f': 4.0},
    ]
    assert actual == expected
    # Obstacle cell (1,1) never appears as state or parent.
    obstacle = (1, 1)
    for e in actual:
        assert e['state'] != obstacle
        if 'parent' in e and e['parent'] is not None:
            assert e['parent'] != obstacle


def test_recording_full_event_sequence_on_grid_4x4_obstacle() -> None:
    """
    ========================================================================
     Assert the exact recorded event sequence for AStar on a 4x4
     grid with a vertical 2-cell wall at (0,2) and (1,2).
     Start (0,0) -> Goal (0,3). The wall forces a 7-step detour
     through row 2. Manhattan h is admissible but loose (ignores
     the wall) — f-values along the detour rise to 5, 7, 9 as
     A* expands into row 1, 2, 3 before reaching the goal.
     Obstacle cells (0,2) and (1,2) never appear as state or
     parent in any event. 11 pushes + 11 pops — vs. BFS's 14+14
     on the same problem, showing the heuristic's pruning power.
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
        {'type': 'push', 'state': (0, 0), 'g': 0, 'parent': None, 'h': 3.0, 'f': 3.0},
        {'type': 'pop',  'state': (0, 0), 'g': 0, 'h': 3.0, 'f': 3.0},
        {'type': 'push', 'state': (0, 1), 'g': 1, 'parent': (0, 0), 'h': 2.0, 'f': 3.0},
        {'type': 'push', 'state': (1, 0), 'g': 1, 'parent': (0, 0), 'h': 4.0, 'f': 5.0},
        {'type': 'pop',  'state': (0, 1), 'g': 1, 'h': 2.0, 'f': 3.0},
        {'type': 'push', 'state': (1, 1), 'g': 2, 'parent': (0, 1), 'h': 3.0, 'f': 5.0},
        {'type': 'pop',  'state': (1, 1), 'g': 2, 'h': 3.0, 'f': 5.0},
        {'type': 'push', 'state': (2, 1), 'g': 3, 'parent': (1, 1), 'h': 4.0, 'f': 7.0},
        {'type': 'pop',  'state': (1, 0), 'g': 1, 'h': 4.0, 'f': 5.0},
        {'type': 'push', 'state': (2, 0), 'g': 2, 'parent': (1, 0), 'h': 5.0, 'f': 7.0},
        {'type': 'pop',  'state': (2, 1), 'g': 3, 'h': 4.0, 'f': 7.0},
        {'type': 'push', 'state': (2, 2), 'g': 4, 'parent': (2, 1), 'h': 3.0, 'f': 7.0},
        {'type': 'push', 'state': (3, 1), 'g': 4, 'parent': (2, 1), 'h': 5.0, 'f': 9.0},
        {'type': 'pop',  'state': (2, 2), 'g': 4, 'h': 3.0, 'f': 7.0},
        {'type': 'push', 'state': (2, 3), 'g': 5, 'parent': (2, 2), 'h': 2.0, 'f': 7.0},
        {'type': 'push', 'state': (3, 2), 'g': 5, 'parent': (2, 2), 'h': 4.0, 'f': 9.0},
        {'type': 'pop',  'state': (2, 3), 'g': 5, 'h': 2.0, 'f': 7.0},
        {'type': 'push', 'state': (1, 3), 'g': 6, 'parent': (2, 3), 'h': 1.0, 'f': 7.0},
        {'type': 'push', 'state': (3, 3), 'g': 6, 'parent': (2, 3), 'h': 3.0, 'f': 9.0},
        {'type': 'pop',  'state': (1, 3), 'g': 6, 'h': 1.0, 'f': 7.0},
        {'type': 'push', 'state': (0, 3), 'g': 7, 'parent': (1, 3), 'h': 0.0, 'f': 7.0},
        {'type': 'pop',  'state': (0, 3), 'g': 7, 'h': 0.0, 'f': 7.0},
    ]
    assert actual == expected
    # Obstacle cells never appear as state or parent.
    obstacles = {(0, 2), (1, 2)}
    for e in actual:
        assert e['state'] not in obstacles
        if 'parent' in e and e['parent'] is not None:
            assert e['parent'] not in obstacles
