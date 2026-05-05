"""
============================================================================
 AStarBPMX — full event-stream pins on the canonical OOSPP
 problem (`grid_4x4_obstacle`) for each Felner pathmax rule.
 One test method per rule; each asserts the complete
 normalized event list (every field of every event,
 `duration` stripped).

 CASCADE tests `depth_bpmx=None` (full reach);
 Rules 1 / 2 / 3 test `depth_bpmx=1` (isolated rule).
 Rule 2 fires `pathmax_apply` lifts at "local minimum"
 cells where the obstacle blocks every h-decreasing
 successor; Rules 1 / 3 attempt but never lift under
 consistent Manhattan h, so their streams are byte-identical
 to plain AStar's 22-event sequence.
============================================================================
"""

from f_hs.algo.i_0_oospp.i_2_astar_bpmx import AStarBPMX
from f_hs.algo.u_event_normalize import normalize


def test_recording_grid_4x4_obstacle_cascade_full() -> None:
    """
    ========================================================================
     Pin the FULL event stream for `rule_bpmx='CASCADE',
     depth_bpmx=None` (30 events: AStar trace + 8
     `bpmx_iteration` markers).
    ========================================================================
    """
    algo = AStarBPMX.Factory.grid_4x4(rule_bpmx='CASCADE',
                                      depth_bpmx=None)
    algo.recorder.is_active = True
    algo.run()
    actual = [normalize(e) for e in algo.recorder.events]
    expected = [
        {'type': 'push', 'state': (0, 0), 'g': 0, 'parent': None, 'h': 3, 'f': 3},
        {'type': 'pop', 'state': (0, 0), 'g': 0, 'h': 3, 'f': 3},
        {'type': 'bpmx_iteration', 'state': (0, 0), 'iteration': 1, 'num_levels': 8, 'num_states': 14},
        {'type': 'push', 'state': (0, 1), 'g': 1, 'parent': (0, 0), 'h': 2, 'f': 3},
        {'type': 'push', 'state': (1, 0), 'g': 1, 'parent': (0, 0), 'h': 4, 'f': 5},
        {'type': 'pop', 'state': (0, 1), 'g': 1, 'h': 2, 'f': 3},
        {'type': 'bpmx_iteration', 'state': (0, 1), 'iteration': 1, 'num_levels': 7, 'num_states': 14},
        {'type': 'push', 'state': (1, 1), 'g': 2, 'parent': (0, 1), 'h': 3, 'f': 5},
        {'type': 'pop', 'state': (1, 1), 'g': 2, 'h': 3, 'f': 5},
        {'type': 'bpmx_iteration', 'state': (1, 1), 'iteration': 1, 'num_levels': 6, 'num_states': 14},
        {'type': 'push', 'state': (2, 1), 'g': 3, 'parent': (1, 1), 'h': 4, 'f': 7},
        {'type': 'pop', 'state': (1, 0), 'g': 1, 'h': 4, 'f': 5},
        {'type': 'bpmx_iteration', 'state': (1, 0), 'iteration': 1, 'num_levels': 7, 'num_states': 14},
        {'type': 'push', 'state': (2, 0), 'g': 2, 'parent': (1, 0), 'h': 5, 'f': 7},
        {'type': 'pop', 'state': (2, 1), 'g': 3, 'h': 4, 'f': 7},
        {'type': 'bpmx_iteration', 'state': (2, 1), 'iteration': 1, 'num_levels': 5, 'num_states': 14},
        {'type': 'push', 'state': (2, 2), 'g': 4, 'parent': (2, 1), 'h': 3, 'f': 7},
        {'type': 'push', 'state': (3, 1), 'g': 4, 'parent': (2, 1), 'h': 5, 'f': 9},
        {'type': 'pop', 'state': (2, 2), 'g': 4, 'h': 3, 'f': 7},
        {'type': 'bpmx_iteration', 'state': (2, 2), 'iteration': 1, 'num_levels': 5, 'num_states': 14},
        {'type': 'push', 'state': (2, 3), 'g': 5, 'parent': (2, 2), 'h': 2, 'f': 7},
        {'type': 'push', 'state': (3, 2), 'g': 5, 'parent': (2, 2), 'h': 4, 'f': 9},
        {'type': 'pop', 'state': (2, 3), 'g': 5, 'h': 2, 'f': 7},
        {'type': 'bpmx_iteration', 'state': (2, 3), 'iteration': 1, 'num_levels': 6, 'num_states': 14},
        {'type': 'push', 'state': (1, 3), 'g': 6, 'parent': (2, 3), 'h': 1, 'f': 7},
        {'type': 'push', 'state': (3, 3), 'g': 6, 'parent': (2, 3), 'h': 3, 'f': 9},
        {'type': 'pop', 'state': (1, 3), 'g': 6, 'h': 1, 'f': 7},
        {'type': 'bpmx_iteration', 'state': (1, 3), 'iteration': 1, 'num_levels': 7, 'num_states': 14},
        {'type': 'push', 'state': (0, 3), 'g': 7, 'parent': (1, 3), 'h': 0, 'f': 7},
        {'type': 'pop', 'state': (0, 3), 'g': 7, 'h': 0, 'f': 7},
    ]
    assert actual == expected


def test_recording_grid_4x4_obstacle_rule_1_isolated() -> None:
    """
    ========================================================================
     Pin the FULL event stream for `rule_bpmx='1',
     depth_bpmx=1`. Rule 1 attempts but never lifts under
     consistent Manhattan h — same 22-event sequence as plain
     AStar.
    ========================================================================
    """
    algo = AStarBPMX.Factory.grid_4x4(rule_bpmx='1', depth_bpmx=1)
    algo.recorder.is_active = True
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


def test_recording_grid_4x4_obstacle_rule_2_isolated() -> None:
    """
    ========================================================================
     Pin the FULL event stream for `rule_bpmx='2',
     depth_bpmx=1`. Rule 2 fires `pathmax_apply` lifts at two
     "local minimum" cells where the obstacle blocks every
     h-decreasing successor — `(0, 1)` and `(1, 1)`. 24
     events.
    ========================================================================
    """
    algo = AStarBPMX.Factory.grid_4x4(rule_bpmx='2', depth_bpmx=1)
    algo.recorder.is_active = True
    algo.run()
    actual = [normalize(e) for e in algo.recorder.events]
    expected = [
        {'type': 'push', 'state': (0, 0), 'g': 0, 'parent': None, 'h': 3, 'f': 3},
        {'type': 'pop', 'state': (0, 0), 'g': 0, 'h': 3, 'f': 3},
        {'type': 'push', 'state': (0, 1), 'g': 1, 'parent': (0, 0), 'h': 2, 'f': 3},
        {'type': 'push', 'state': (1, 0), 'g': 1, 'parent': (0, 0), 'h': 4, 'f': 5},
        {'type': 'pop', 'state': (0, 1), 'g': 1, 'h': 2, 'f': 3},
        {'type': 'pathmax_apply', 'state': (0, 1), 'h_old': 2, 'h_new': 4, 'rule': 2, 'via_children': ((1, 1), (0, 0))},
        {'type': 'push', 'state': (1, 1), 'g': 2, 'parent': (0, 1), 'h': 3, 'f': 5},
        {'type': 'pop', 'state': (1, 1), 'g': 2, 'h': 3, 'f': 5},
        {'type': 'pathmax_apply', 'state': (1, 1), 'h_old': 3, 'h_new': 5, 'rule': 2, 'via_children': ((0, 1), (2, 1), (1, 0))},
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


def test_recording_grid_4x4_obstacle_rule_3_isolated() -> None:
    """
    ========================================================================
     Pin the FULL event stream for `rule_bpmx='3',
     depth_bpmx=1`. Rule 3 attempts but never lifts under
     consistent Manhattan h — same 22-event sequence as plain
     AStar.
    ========================================================================
    """
    algo = AStarBPMX.Factory.grid_4x4(rule_bpmx='3', depth_bpmx=1)
    algo.recorder.is_active = True
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
