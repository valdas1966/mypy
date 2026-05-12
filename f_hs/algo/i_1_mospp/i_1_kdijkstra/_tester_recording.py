"""
============================================================================
 KDijkstraMOSPP — recording pin on the canonical MOSPP problem
 (`Factory.grid_4x4_obstacle_mospp`: starts (0,3) / (3,0) /
 (3,3); goal (0,0); per-start optimal costs 7 / 3 / 6).

 KDijkstraMOSPP delegates to OMSPP `KDijkstra` via the flipped
 view. The flipped view of the canonical MOSPP problem is
 structurally identical to `grid_4x4_obstacle_omspp`, so the
 inner Dijkstra traces the exact same 14-push / 14-pop
 sequence as OMSPP's canonical recording pin — but the
 recorder shim rewrites the 3 `on_goal` events as `on_start`
 (with `start_index` instead of `goal_index`). Identical
 event stream to KBFSMOSPP on uniform weights.

 Discovery order: (3,0) at g=3 (start_idx=1) → (3,3) at g=6
 (start_idx=2) → (0,3) at g=7 (start_idx=0). All
 `reason='expanded'`.
============================================================================
"""

from f_hs.algo.i_1_mospp.i_1_kdijkstra import KDijkstraMOSPP
from f_hs.algo.u_event_normalize import normalize
from f_hs.problem.i_1_grid import ProblemGrid


def test_recording_canonical_mospp_full_event_stream() -> None:
    """
    ========================================================================
     Pin the FULL event stream (every field of every event,
     `duration` stripped) on the canonical MOSPP problem.
     Mirror of OMSPP `KDijkstra`'s canonical pin with
     `on_goal` → `on_start` and `goal_index` → `start_index`.
    ========================================================================
    """
    p = ProblemGrid.Factory.grid_4x4_obstacle_mospp()
    algo = KDijkstraMOSPP(problem=p, is_recording=True)
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
        {'type': 'on_start', 'state': (3, 0), 'g': 3, 'reason': 'expanded', 'start_index': 1},
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
        {'type': 'on_start', 'state': (3, 3), 'g': 6, 'reason': 'expanded', 'start_index': 2},
        {'type': 'pop',  'state': (0, 3), 'g': 7},
        {'type': 'on_start', 'state': (0, 3), 'g': 7, 'reason': 'expanded', 'start_index': 0},
    ]
    assert actual == expected
