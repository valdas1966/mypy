"""
============================================================================
 AStarBPMX — counter pin tests, one per rule_bpmx value on
 the canonical OOSPP problem (`grid_4x4_obstacle`).

 Manhattan h on grid_4x4_obstacle is consistent (1-Lipschitz),
 so Rules 1 / 3 / CASCADE attempt on every non-goal expansion
 but never strictly tighten → cnt_bpmx_successes = 0,
 cnt_bpmx_depth = 0.

 Rule 2 IS counted (since the rename: pathmax_attempts /
 pathmax_successes → bpmx_attempts / bpmx_successes — Rule 2
 contributes uniformly). It fires twice at the "local minimum"
 cells (0,1) and (1,1) where the obstacle blocks every
 h-decreasing successor → cnt_bpmx_successes == 2.
 cnt_bpmx_depth stays 0 because Rule 2 lifts the root state
 itself (level 0).

 Heap-op counters (cnt_push / cnt_pop / cnt_decrease) are
 byte-identical across all rule values: 13 / 9 / 0
 (lifts under Rule 2 don't re-heap the frontier — stale-
 priority policy).
============================================================================
"""

from f_hs.algo.i_0_oospp.i_3_astar_bpmx import AStarBPMX


# ─────────────────────────────────────────────────────────────
#  Per-rule counter pins on grid_4x4_obstacle
# ─────────────────────────────────────────────────────────────

def test_counters_grid_4x4_obstacle_off() -> None:
    """
    ========================================================================
     rule_bpmx=None — mechanism off. All BPMX counters 0;
     frontier 13/9/0; expanded=8, generated=13.
    ========================================================================
    """
    algo = AStarBPMX.Factory.grid_4x4()
    algo.run()
    counters = {k: v for k, v in algo.counters.items()
                if not k.startswith('mem_')}
    assert counters == {
        'cnt_prop_waves': 0,
        'cnt_prop_attempts': 0,
        'cnt_prop_lifts': 0,
        'cnt_bpmx_attempts': 0,
        'cnt_bpmx_successes': 0,
        'cnt_bpmx_depth': 0,
        'cnt_push': 13,
        'cnt_pop': 9,
        'cnt_decrease': 0,
        'cnt_expanded': 8,
        'cnt_generated': 13,
    }


def test_counters_grid_4x4_obstacle_rule_1() -> None:
    """
    ========================================================================
     rule_bpmx='1' (depth=1). Rule 1 attempts on every non-goal
     expansion (cnt_bpmx_attempts == 8) but cannot strictly
     tighten under consistent h → 0 successes, 0 depth.
    ========================================================================
    """
    algo = AStarBPMX.Factory.grid_4x4(rule_bpmx='1', depth_bpmx=1)
    algo.run()
    counters = {k: v for k, v in algo.counters.items()
                if not k.startswith('mem_')}
    assert counters == {
        'cnt_prop_waves': 0,
        'cnt_prop_attempts': 0,
        'cnt_prop_lifts': 0,
        'cnt_bpmx_attempts': 8,
        'cnt_bpmx_successes': 0,
        'cnt_bpmx_depth': 0,
        'cnt_push': 13,
        'cnt_pop': 9,
        'cnt_decrease': 0,
        'cnt_expanded': 8,
        'cnt_generated': 13,
    }


def test_counters_grid_4x4_obstacle_rule_2() -> None:
    """
    ========================================================================
     rule_bpmx='2' (depth=1). Rule 2 fires twice — at the two
     "local minimum" cells (0,1) and (1,1) where the obstacle
     blocks every h-decreasing successor. cnt_bpmx_successes
     == 2. cnt_bpmx_depth stays 0 (Rule 2 lifts the root state
     itself, level 0). Frontier counters identical to other
     rules (13/9/0) because stale-priority policy absorbs the
     lifts.
    ========================================================================
    """
    algo = AStarBPMX.Factory.grid_4x4(rule_bpmx='2', depth_bpmx=1)
    algo.run()
    counters = {k: v for k, v in algo.counters.items()
                if not k.startswith('mem_')}
    assert counters == {
        'cnt_prop_waves': 0,
        'cnt_prop_attempts': 0,
        'cnt_prop_lifts': 0,
        'cnt_bpmx_attempts': 8,
        'cnt_bpmx_successes': 2,
        'cnt_bpmx_depth': 0,
        'cnt_push': 13,
        'cnt_pop': 9,
        'cnt_decrease': 0,
        'cnt_expanded': 8,
        'cnt_generated': 13,
    }


def test_counters_grid_4x4_obstacle_rule_3() -> None:
    """
    ========================================================================
     rule_bpmx='3' (depth=1). Symmetric to Rule 1 — the
     reverse-pathmax bound never exceeds the parent's existing
     h when h is 1-Lipschitz. 8 attempts, 0 successes, 0 depth.
    ========================================================================
    """
    algo = AStarBPMX.Factory.grid_4x4(rule_bpmx='3', depth_bpmx=1)
    algo.run()
    counters = {k: v for k, v in algo.counters.items()
                if not k.startswith('mem_')}
    assert counters == {
        'cnt_prop_waves': 0,
        'cnt_prop_attempts': 0,
        'cnt_prop_lifts': 0,
        'cnt_bpmx_attempts': 8,
        'cnt_bpmx_successes': 0,
        'cnt_bpmx_depth': 0,
        'cnt_push': 13,
        'cnt_pop': 9,
        'cnt_decrease': 0,
        'cnt_expanded': 8,
        'cnt_generated': 13,
    }


def test_counters_grid_4x4_obstacle_cascade_full() -> None:
    """
    ========================================================================
     rule_bpmx='CASCADE', depth_bpmx=None (full reach).
     Cascade runs once per non-goal expansion (8 times) with
     no tightenings under consistent h. 8 attempts, 0
     successes, 0 depth.
    ========================================================================
    """
    algo = AStarBPMX.Factory.grid_4x4(rule_bpmx='CASCADE',
                                      depth_bpmx=None)
    algo.run()
    counters = {k: v for k, v in algo.counters.items()
                if not k.startswith('mem_')}
    assert counters == {
        'cnt_prop_waves': 0,
        'cnt_prop_attempts': 0,
        'cnt_prop_lifts': 0,
        'cnt_bpmx_attempts': 8,
        'cnt_bpmx_successes': 0,
        'cnt_bpmx_depth': 0,
        'cnt_push': 13,
        'cnt_pop': 9,
        'cnt_decrease': 0,
        'cnt_expanded': 8,
        'cnt_generated': 13,
    }
