"""
============================================================================
 KDijkstra — recording pin on the canonical OMSPP problem
 (`Factory.grid_4x4_obstacle_omspp`: start (0,0), goals (0,3)
 / (3,0) / (3,3); per-goal optimal costs 7 / 3 / 6).

 KDijkstra runs a SINGLE inner Dijkstra pass and emits
 `on_goal` at the moment each goal is popped (interleaved
 with the search). Identical event stream to KBFS on this
 uniform-cost grid (Dijkstra's `(g, -g, state)` priority
 under h≡0 matches BFS FIFO insertion order). No
 `update_heuristic`, no `update_frontier`, no
 `'already_closed'` reason.
============================================================================
"""

from f_hs.algo.i_1_omspp.i_2_kdijkstra import KDijkstra
from f_hs.algo.u_event_normalize import normalize
from f_hs.problem.i_1_grid import ProblemGrid


def test_recording_canonical_omspp_full_event_stream() -> None:
    """
    ========================================================================
     Pin the FULL event stream (every field of every event,
     `duration` stripped) on the canonical OMSPP problem.

     Subsumes the partial pins (event-type counts, pop
     sequence, h/f schema) — any drift in ordering, payload
     fields, or event types surfaces here as a dict-list diff.

     Identical 31-event sequence to KBFS on this canonical
     (uniform-cost grid + h ≡ 0 → `(g, -g, state)` priority
     order matches BFS's FIFO insertion order). Pinned here
     independently from KBFS so a future divergence in either
     algo's tiebreak surfaces in both testers, not just one.

     Layout: 14 push / 14 pop in g-order from (0,0), with 3
     `on_goal` events INTERLEAVED at the moment each goal is
     popped — (3,0) at g=3 (input idx=1), (3,3) at g=6
     (input idx=2), (0,3) at g=7 (input idx=0; final pop
     terminates the search). All `reason='expanded'`.
    ========================================================================
    """
    p = ProblemGrid.Factory.grid_4x4_obstacle_omspp()
    algo = KDijkstra(problem=p, is_recording=True)
    algo.run()

    actual = [normalize(e) for e in algo.recorder.events]
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
        {'type': 'on_goal', 'state': (3, 0), 'g': 3, 'reason': 'expanded', 'goal_index': 1},
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
        {'type': 'on_goal', 'state': (3, 3), 'g': 6, 'reason': 'expanded', 'goal_index': 2},
        {'type': 'pop',  'state': (0, 3), 'g': 7},
        {'type': 'on_goal', 'state': (0, 3), 'g': 7, 'reason': 'expanded', 'goal_index': 0},
    ]
    assert actual == expected
