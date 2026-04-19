from f_hs.algo.i_2_dijkstra import Dijkstra
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
     Dict comparison then checks the exact keyset — a Dijkstra event
     accidentally carrying h or f (from AStar) would fail the test.
    ========================================================================
    """
    out = {k: v for k, v in event.items() if k != 'duration'}
    out['state'] = _key_of(event['state'])
    if 'parent' in event:
        p = event['parent']
        out['parent'] = _key_of(p) if p is not None else None
    return out


def test_recording_no_h_or_f_fields() -> None:
    """
    ========================================================================
     Dijkstra overrides AStar's _enrich_event to a no-op — its
     events must NOT carry h or f. h=0 is constant and f=g is
     derivable, so both violate the framework Recording Principle.
     This test pins the schema across every event type on a
     non-trivial grid problem.
    ========================================================================
    """
    algo = Dijkstra.Factory.grid_3x3_obstacle()
    algo._recorder = algo._recorder.__class__(is_active=True)
    algo.run()
    for e in algo.recorder.events:
        assert 'h' not in e, f'unexpected h on {e["type"]} event'
        assert 'f' not in e, f'unexpected f on {e["type"]} event'


def test_recording_full_event_sequence_on_graph_abc() -> None:
    """
    ========================================================================
     Assert the exact recorded event sequence for Dijkstra on
     A -> B -> C. Schema matches BFS (no h / f).
    ========================================================================
    """
    algo = Dijkstra(problem=ProblemSPP.Factory.graph_abc(),
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


def test_recording_full_event_sequence_on_graph_diamond() -> None:
    """
    ========================================================================
     Assert the exact recorded event sequence for Dijkstra on the
     diamond A -> {B, C} -> D. Unlike AStar (which reaches D via B
     and never expands C because an admissible h pulls the goal
     down in priority), Dijkstra expands BOTH B and C before the
     goal D — there is no heuristic to prefer one g=1 state over
     the other at the g=2 frontier. State tiebreak puts B before
     C ('B' < 'C'). C's attempt to push D is a no-op (new_g == g,
     not strictly less).
    ========================================================================
    """
    algo = Dijkstra(problem=ProblemSPP.Factory.graph_diamond(),
                    is_recording=True)
    algo.run()
    actual = [_normalize(e) for e in algo.recorder.events]
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
    # C is popped before D (fully expanded), unlike AStar.
    popped = [e['state'] for e in actual if e['type'] == 'pop']
    assert popped.index('C') < popped.index('D')


def test_recording_full_event_sequence_on_graph_decrease() -> None:
    """
    ========================================================================
     Assert the exact recorded event sequence for Dijkstra on the
     weighted decrease-graph (S -> A/B -> X with w(B,X) = 0).
     A and B tie on (g=1, -g=-1); State tiebreak ('A' < 'B') pops
     A first; A pushes X with g=2; B pops next and re-parents X
     via `decrease_g` (new_g = 1 + 0 = 1 < 2).

     Pins, beyond the existing Dijkstra tests:
       1. The `decrease_g` event type is emitted.
       2. The `decrease_g` event carries NO `h` or `f` fields
          (Dijkstra's _enrich_event is a no-op on decrease_g
          too, not just on push / pop).
       3. The `parent` and `g` on `decrease_g` reflect the NEW
          values (B, 1), not the previous ones (A, 2).
    ========================================================================
    """
    algo = Dijkstra.Factory.graph_decrease()
    algo._recorder.is_active = True
    sol = algo.run()
    assert sol.cost == 1.0
    actual = [_normalize(e) for e in algo.recorder.events]
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
    decrs = [e for e in actual if e['type'] == 'decrease_g']
    assert len(decrs) == 1
    assert decrs[0]['parent'] == 'B'
    assert decrs[0]['g'] == 1
    # Schema pin: decrease_g must NOT carry h or f on Dijkstra.
    assert 'h' not in decrs[0]
    assert 'f' not in decrs[0]


def test_recording_full_event_sequence_on_grid_3x3() -> None:
    """
    ========================================================================
     Assert the exact recorded event sequence for Dijkstra on an
     open 3x3 grid from (0,0) to (2,2). On unit-cost edges and
     with the State tiebreak, Dijkstra's expansion order matches
     BFS's exactly — 9 pushes + 9 pops, identical event schema
     (no h / f).
    ========================================================================
    """
    algo = Dijkstra(problem=ProblemGrid.Factory.grid_3x3(),
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
     Assert the exact recorded event sequence for Dijkstra on the
     4x4 grid with a vertical 2-cell wall at (0,2) and (1,2).
     Start (0,0) -> Goal (0,3). On unit-cost edges Dijkstra
     behaves identically to BFS — 14 pushes + 14 pops, same
     expansion order. Obstacle cells never appear as state or
     parent.
    ========================================================================
    """
    algo = Dijkstra(problem=ProblemGrid.Factory.grid_4x4_obstacle(),
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
    # Obstacle cells (0,2) and (1,2) never appear as state or parent.
    obstacles = {(0, 2), (1, 2)}
    for e in actual:
        assert e['state'] not in obstacles
        if 'parent' in e and e['parent'] is not None:
            assert e['parent'] not in obstacles
