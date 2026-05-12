"""
============================================================================
 AStarBPMX — full recording pins on the canonical OOSPP problem
 with a CACHED INCONSISTENCY BEACON, one test per representative
 (rule_bpmx, depth_bpmx) configuration.

 Single fixture: `AStarBPMX.Factory.grid_4x4_beacon(rule, depth,
 is_recording=True)` — canonical 4x4 obstacle grid + cached
 beacon at (0,1) with h*=6 (vs. Manhattan=2; gap=4).

 Coverage strategy: pin the full event stream for FOUR
 representative configs that exercise distinct BPMX event
 vocabularies:

   - rule=None         baseline: only push / pop / decrease_g
   - rule='1' depth=None   Rule 1 emits `bpmx_forward` events
   - rule='3' depth=1      Rule 3 emits `bpmx_lift` events
   - rule='CASCADE' depth=None   CASCADE emits all three
                                  (`bpmx_iteration`, `bpmx_lift`,
                                  `bpmx_forward`)

 The push / pop subsequence is identical across configs on this
 fixture (BPMX lifts modify h-values stored in HBounded but do
 not re-heap the frontier — the priority order is preserved).
 Differences live in the interleaved bpmx_* events.
============================================================================
"""

from f_hs.algo.i_0_oospp.i_3_astar_bpmx import AStarBPMX
from f_hs.algo.u_event_normalize import normalize


# ─────────────────────────────────────────────────────────────
#  Baseline — rule_bpmx=None (no BPMX events)
# ─────────────────────────────────────────────────────────────


def test_recording_grid_4x4_beacon_off() -> None:
    """
    ========================================================================
     Pin the FULL event stream on the canonical 4x4 beacon
     fixture with rule_bpmx=None. Only push / pop events; the
     beacon's `is_cached=True` flag appears on its push.
    ========================================================================
    """
    algo = AStarBPMX.Factory.grid_4x4_beacon(
        rule_bpmx=None, depth_bpmx=1, is_recording=True)
    algo.run()
    actual = [normalize(e) for e in algo.recorder.events]
    expected = [
        {'type': 'push', 'state': (0, 0), 'g': 0, 'parent': None, 'h': 3, 'f': 3},
        {'type': 'pop',  'state': (0, 0), 'g': 0, 'h': 3, 'f': 3},
        {'type': 'push', 'state': (0, 1), 'g': 1, 'parent': (0, 0), 'h': 6, 'f': 7, 'is_cached': True},
        {'type': 'push', 'state': (1, 0), 'g': 1, 'parent': (0, 0), 'h': 4, 'f': 5},
        {'type': 'pop',  'state': (1, 0), 'g': 1, 'h': 4, 'f': 5},
        {'type': 'push', 'state': (1, 1), 'g': 2, 'parent': (1, 0), 'h': 3, 'f': 5},
        {'type': 'push', 'state': (2, 0), 'g': 2, 'parent': (1, 0), 'h': 5, 'f': 7},
        {'type': 'pop',  'state': (1, 1), 'g': 2, 'h': 3, 'f': 5},
        {'type': 'push', 'state': (2, 1), 'g': 3, 'parent': (1, 1), 'h': 4, 'f': 7},
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


# ─────────────────────────────────────────────────────────────
#  Rule 1, depth=None — emits bpmx_forward
# ─────────────────────────────────────────────────────────────


def test_recording_grid_4x4_beacon_rule_1_depth_none() -> None:
    """
    ========================================================================
     Pin the FULL event stream for Rule 1 at unbounded depth.
     Rule 1 lifts via parent-to-child forward pathmax; two
     `bpmx_forward` events fire — one when (0,0)'s subtree
     reaches (1,1) via the beacon at (0,1), and one when
     (1,0)'s subtree forwards back to (0,0) via the beacon.
    ========================================================================
    """
    algo = AStarBPMX.Factory.grid_4x4_beacon(
        rule_bpmx='1', depth_bpmx=None, is_recording=True)
    algo.run()
    actual = [normalize(e) for e in algo.recorder.events]
    expected = [
        {'type': 'push', 'state': (0, 0), 'g': 0, 'parent': None, 'h': 3, 'f': 3},
        {'type': 'pop',  'state': (0, 0), 'g': 0, 'h': 3, 'f': 3},
        {'type': 'bpmx_forward', 'state': (1, 1), 'h_old': 3, 'h_new': 5, 'via_parent': (0, 1)},
        {'type': 'push', 'state': (0, 1), 'g': 1, 'parent': (0, 0), 'h': 6, 'f': 7, 'is_cached': True},
        {'type': 'push', 'state': (1, 0), 'g': 1, 'parent': (0, 0), 'h': 4, 'f': 5},
        {'type': 'pop',  'state': (1, 0), 'g': 1, 'h': 4, 'f': 5},
        {'type': 'push', 'state': (1, 1), 'g': 2, 'parent': (1, 0), 'h': 5, 'f': 7},
        {'type': 'push', 'state': (2, 0), 'g': 2, 'parent': (1, 0), 'h': 5, 'f': 7},
        {'type': 'pop',  'state': (1, 1), 'g': 2, 'h': 5, 'f': 7},
        {'type': 'bpmx_forward', 'state': (0, 0), 'h_old': 3, 'h_new': 5, 'via_parent': (0, 1)},
        {'type': 'push', 'state': (2, 1), 'g': 3, 'parent': (1, 1), 'h': 4, 'f': 7},
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


# ─────────────────────────────────────────────────────────────
#  Rule 3, depth=1 — emits bpmx_lift
# ─────────────────────────────────────────────────────────────


def test_recording_grid_4x4_beacon_rule_3_depth_1() -> None:
    """
    ========================================================================
     Pin the FULL event stream for Rule 3 at depth=1. Rule 3
     lifts via child-to-parent reverse pathmax; two `bpmx_lift`
     events fire — (0,0) is lifted via (0,1), and (1,1) is
     lifted via (0,1).
    ========================================================================
    """
    algo = AStarBPMX.Factory.grid_4x4_beacon(
        rule_bpmx='3', depth_bpmx=1, is_recording=True)
    algo.run()
    actual = [normalize(e) for e in algo.recorder.events]
    expected = [
        {'type': 'push', 'state': (0, 0), 'g': 0, 'parent': None, 'h': 3, 'f': 3},
        {'type': 'pop',  'state': (0, 0), 'g': 0, 'h': 3, 'f': 3},
        {'type': 'bpmx_lift', 'state': (0, 0), 'h_old': 3, 'h_new': 5, 'via_child': (0, 1)},
        {'type': 'push', 'state': (0, 1), 'g': 1, 'parent': (0, 0), 'h': 6, 'f': 7, 'is_cached': True},
        {'type': 'push', 'state': (1, 0), 'g': 1, 'parent': (0, 0), 'h': 4, 'f': 5},
        {'type': 'pop',  'state': (1, 0), 'g': 1, 'h': 4, 'f': 5},
        {'type': 'push', 'state': (1, 1), 'g': 2, 'parent': (1, 0), 'h': 3, 'f': 5},
        {'type': 'push', 'state': (2, 0), 'g': 2, 'parent': (1, 0), 'h': 5, 'f': 7},
        {'type': 'pop',  'state': (1, 1), 'g': 2, 'h': 3, 'f': 5},
        {'type': 'bpmx_lift', 'state': (1, 1), 'h_old': 3, 'h_new': 5, 'via_child': (0, 1)},
        {'type': 'push', 'state': (2, 1), 'g': 3, 'parent': (1, 1), 'h': 4, 'f': 7},
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


# ─────────────────────────────────────────────────────────────
#  CASCADE, depth=None — emits iteration + lift + forward
# ─────────────────────────────────────────────────────────────


def test_recording_grid_4x4_beacon_cascade_depth_none() -> None:
    """
    ========================================================================
     Pin the FULL event stream for CASCADE at unbounded depth
     — the most complex BPMX configuration. Each expansion
     emits a `bpmx_iteration` marker; (0,0)'s expansion runs
     two iterations (one lift + one forward, then a settling
     pass with no changes). All three BPMX event types
     (`bpmx_iteration`, `bpmx_lift`, `bpmx_forward`) appear.
    ========================================================================
    """
    algo = AStarBPMX.Factory.grid_4x4_beacon(
        rule_bpmx='CASCADE', depth_bpmx=None, is_recording=True)
    algo.run()
    actual = [normalize(e) for e in algo.recorder.events]
    expected = [
        {'type': 'push', 'state': (0, 0), 'g': 0, 'parent': None, 'h': 3, 'f': 3},
        {'type': 'pop',  'state': (0, 0), 'g': 0, 'h': 3, 'f': 3},
        {'type': 'bpmx_iteration', 'state': (0, 0), 'iteration': 1, 'num_levels': 8, 'num_states': 14},
        {'type': 'bpmx_lift', 'state': (0, 0), 'h_old': 3, 'h_new': 5, 'via_child': (0, 1)},
        {'type': 'bpmx_forward', 'state': (1, 1), 'h_old': 3, 'h_new': 5, 'via_parent': (0, 1)},
        {'type': 'bpmx_iteration', 'state': (0, 0), 'iteration': 2, 'num_levels': 8, 'num_states': 14},
        {'type': 'push', 'state': (0, 1), 'g': 1, 'parent': (0, 0), 'h': 6, 'f': 7, 'is_cached': True},
        {'type': 'push', 'state': (1, 0), 'g': 1, 'parent': (0, 0), 'h': 4, 'f': 5},
        {'type': 'pop',  'state': (1, 0), 'g': 1, 'h': 4, 'f': 5},
        {'type': 'bpmx_iteration', 'state': (1, 0), 'iteration': 1, 'num_levels': 7, 'num_states': 14},
        {'type': 'push', 'state': (1, 1), 'g': 2, 'parent': (1, 0), 'h': 5, 'f': 7},
        {'type': 'push', 'state': (2, 0), 'g': 2, 'parent': (1, 0), 'h': 5, 'f': 7},
        {'type': 'pop',  'state': (1, 1), 'g': 2, 'h': 5, 'f': 7},
        {'type': 'bpmx_iteration', 'state': (1, 1), 'iteration': 1, 'num_levels': 6, 'num_states': 14},
        {'type': 'push', 'state': (2, 1), 'g': 3, 'parent': (1, 1), 'h': 4, 'f': 7},
        {'type': 'pop',  'state': (2, 1), 'g': 3, 'h': 4, 'f': 7},
        {'type': 'bpmx_iteration', 'state': (2, 1), 'iteration': 1, 'num_levels': 5, 'num_states': 14},
        {'type': 'push', 'state': (2, 2), 'g': 4, 'parent': (2, 1), 'h': 3, 'f': 7},
        {'type': 'push', 'state': (3, 1), 'g': 4, 'parent': (2, 1), 'h': 5, 'f': 9},
        {'type': 'pop',  'state': (2, 2), 'g': 4, 'h': 3, 'f': 7},
        {'type': 'bpmx_iteration', 'state': (2, 2), 'iteration': 1, 'num_levels': 5, 'num_states': 14},
        {'type': 'push', 'state': (2, 3), 'g': 5, 'parent': (2, 2), 'h': 2, 'f': 7},
        {'type': 'push', 'state': (3, 2), 'g': 5, 'parent': (2, 2), 'h': 4, 'f': 9},
        {'type': 'pop',  'state': (2, 3), 'g': 5, 'h': 2, 'f': 7},
        {'type': 'bpmx_iteration', 'state': (2, 3), 'iteration': 1, 'num_levels': 6, 'num_states': 14},
        {'type': 'push', 'state': (1, 3), 'g': 6, 'parent': (2, 3), 'h': 1, 'f': 7},
        {'type': 'push', 'state': (3, 3), 'g': 6, 'parent': (2, 3), 'h': 3, 'f': 9},
        {'type': 'pop',  'state': (1, 3), 'g': 6, 'h': 1, 'f': 7},
        {'type': 'bpmx_iteration', 'state': (1, 3), 'iteration': 1, 'num_levels': 7, 'num_states': 14},
        {'type': 'push', 'state': (0, 3), 'g': 7, 'parent': (1, 3), 'h': 0, 'f': 7},
        {'type': 'pop',  'state': (0, 3), 'g': 7, 'h': 0, 'f': 7},
    ]
    assert actual == expected
