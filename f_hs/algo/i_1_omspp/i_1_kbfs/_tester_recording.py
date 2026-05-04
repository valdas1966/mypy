"""
============================================================================
 KBFS — recording pin on the canonical OMSPP problem
 (`Factory.grid_4x4_obstacle_omspp`: start (0,0), goals (0,3)
 / (3,0) / (3,3); per-goal optimal costs 7 / 3 / 6).

 KBFS runs a SINGLE inner BFS pass and emits `on_goal` at the
 moment each goal is popped (interleaved with the search,
 not deferred to a per-goal sub-search end). No
 `decrease_g` (FIFO), no `update_heuristic` (no h), no
 `update_frontier` (no per-goal sub-search restarts), no
 `'already_closed'` reason. Discovery order on this map:
 (3,0) at g=3 → (3,3) at g=6 → (0,3) at g=7.
============================================================================
"""

from f_hs.algo.i_1_omspp.i_1_kbfs import KBFS
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

     Layout: 14 push / 14 pop in BFS layer order from (0,0),
     with 3 `on_goal` events INTERLEAVED at the moment each
     goal is popped — (3,0) at g=3 (input idx=1), (3,3) at
     g=6 (input idx=2), (0,3) at g=7 (input idx=0; final pop
     terminates the search). All `reason='expanded'`.
    ========================================================================
    """
    p = ProblemGrid.Factory.grid_4x4_obstacle_omspp()
    algo = KBFS(problem=p, is_recording=True)
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
