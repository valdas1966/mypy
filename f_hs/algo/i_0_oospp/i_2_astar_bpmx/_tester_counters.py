"""
============================================================================
 AStarBPMX — counter tests, one method per Felner pathmax rule
 on the canonical OOSPP problem (`grid_4x4_obstacle`) with
 max BPMX cascade (`depth_bpmx=None`).

 Each test calls a Factory method directly — no in-file
 helpers. Recording is OFF here (counters are independent of
 `is_recording`); the recording-event tests live in
 `_tester_recording.py`. Generic counter invariants (scaffold
 shape, off-mode, attempts-per-expansion, subtree bound) live
 in `_tester.py`.

 Manhattan h on grid_4x4_obstacle is consistent (1-Lipschitz),
 so:
   - Rules 1 and 3 attempt on every non-goal expansion but
     never strictly tighten → cnt_pathmax_lifts = 0.
   - Rule 2 can fire at "local minimum" cells where the
     obstacle blocks every h-decreasing successor → 2 lifts.
   - The BPMX(infinity) cascade itself tightens nothing under
     consistent h → cnt_bpmx_rule3_lifts = cnt_bpmx_rule1_forwards
     = 0 across all four rule values.

 Because the lifts under Rule 2 don't re-heap the frontier
 (stale-priority policy), the heap-op counters
 (cnt_push / cnt_pop / cnt_decrease) are byte-identical across
 all four rules: 13 / 9 / 0.
============================================================================
"""

from f_hs.algo.i_0_oospp.i_2_astar_bpmx import AStarBPMX


# ─────────────────────────────────────────────────────────────
#  Per-rule counter pins on grid_4x4_obstacle, depth_bpmx=None
# ─────────────────────────────────────────────────────────────

def test_counters_grid_4x4_obstacle_rule_none_depth_full() -> None:
    """
    ========================================================================
     rule_pathmax=None, depth_bpmx=None
     (`AStarBPMX.Factory.grid_4x4_bpmx_full()`).

     Mechanism off for the isolated rule (cnt_pathmax_* = 0);
     BPMX cascade runs once per non-goal expansion (8 times),
     each cascade settling in 1 iteration with no tightenings.
     Frontier: 13 push / 9 pop / 0 decrease.
    ========================================================================
    """
    algo = AStarBPMX.Factory.grid_4x4_bpmx_full()
    algo.run()
    assert dict(algo.counters) == {
        'cnt_pathmax_attempts': 0,
        'cnt_pathmax_lifts': 0,
        'cnt_bpmx_attempts': 8,
        'cnt_bpmx_iterations': 8,
        'cnt_bpmx_rule3_lifts': 0,
        'cnt_bpmx_rule1_forwards': 0,
        'cnt_bpmx_subtree_states': 112,
        'cnt_push': 13,
        'cnt_pop': 9,
        'cnt_decrease': 0,
        'mem_open': 1245,
        'mem_closed': 1819,
        'mem_cache': 0,
        'mem_bounds': 64,
    }


def test_counters_grid_4x4_obstacle_rule_1_depth_full() -> None:
    """
    ========================================================================
     rule_pathmax=1 (Mero parent→child), depth_bpmx=None
     (`AStarBPMX.Factory.grid_4x4_rule1_bpmx_full()`).

     Isolated Rule 1 attempts on every non-goal expansion
     (cnt_pathmax_attempts == 8) but cannot strictly tighten
     under consistent Manhattan h (cnt_pathmax_lifts == 0).
     BPMX cascade also tightens nothing.
    ========================================================================
    """
    algo = AStarBPMX.Factory.grid_4x4_rule1_bpmx_full()
    algo.run()
    assert dict(algo.counters) == {
        'cnt_pathmax_attempts': 8,
        'cnt_pathmax_lifts': 0,
        'cnt_bpmx_attempts': 8,
        'cnt_bpmx_iterations': 8,
        'cnt_bpmx_rule3_lifts': 0,
        'cnt_bpmx_rule1_forwards': 0,
        'cnt_bpmx_subtree_states': 112,
        'cnt_push': 13,
        'cnt_pop': 9,
        'cnt_decrease': 0,
        'mem_open': 1245,
        'mem_closed': 1819,
        'mem_cache': 0,
        'mem_bounds': 64,
    }


def test_counters_grid_4x4_obstacle_rule_2_depth_full() -> None:
    """
    ========================================================================
     rule_pathmax=2 (Felner children→parent via min),
     depth_bpmx=None
     (`AStarBPMX.Factory.grid_4x4_rule2_bpmx_full()`).

     Rule 2 fires twice — at the two "local minimum" cells
     (0,1) and (1,1) where the obstacle blocks every
     h-decreasing successor. cnt_pathmax_lifts == 2; the rest
     of the mechanism counters match the other rules. Frontier
     counters identical to all four rules (13/9/0) because
     stale-priority policy absorbs the lifts.
    ========================================================================
    """
    algo = AStarBPMX.Factory.grid_4x4_rule2_bpmx_full()
    algo.run()
    assert dict(algo.counters) == {
        'cnt_pathmax_attempts': 8,
        'cnt_pathmax_lifts': 2,
        'cnt_bpmx_attempts': 8,
        'cnt_bpmx_iterations': 8,
        'cnt_bpmx_rule3_lifts': 0,
        'cnt_bpmx_rule1_forwards': 0,
        'cnt_bpmx_subtree_states': 112,
        'cnt_push': 13,
        'cnt_pop': 9,
        'cnt_decrease': 0,
        'mem_open': 1245,
        'mem_closed': 1819,
        'mem_cache': 0,
        'mem_bounds': 272,
    }


def test_counters_grid_4x4_obstacle_rule_3_depth_full() -> None:
    """
    ========================================================================
     rule_pathmax=3 (Felner single child→parent reverse),
     depth_bpmx=None
     (`AStarBPMX.Factory.grid_4x4_rule3_bpmx_full()`).

     Symmetric to Rule 1 in this respect — the reverse-
     pathmax bound never exceeds the parent's existing h when
     h is 1-Lipschitz. cnt_pathmax_attempts == 8, but
     cnt_pathmax_lifts == 0.
    ========================================================================
    """
    algo = AStarBPMX.Factory.grid_4x4_rule3_bpmx_full()
    algo.run()
    assert dict(algo.counters) == {
        'cnt_pathmax_attempts': 8,
        'cnt_pathmax_lifts': 0,
        'cnt_bpmx_attempts': 8,
        'cnt_bpmx_iterations': 8,
        'cnt_bpmx_rule3_lifts': 0,
        'cnt_bpmx_rule1_forwards': 0,
        'cnt_bpmx_subtree_states': 112,
        'cnt_push': 13,
        'cnt_pop': 9,
        'cnt_decrease': 0,
        'mem_open': 1245,
        'mem_closed': 1819,
        'mem_cache': 0,
        'mem_bounds': 64,
    }
