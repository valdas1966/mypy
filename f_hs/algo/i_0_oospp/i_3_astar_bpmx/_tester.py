"""
============================================================================
 AStarBPMX — lifecycle tests on the canonical OOSPP problem with a
 CACHED INCONSISTENCY BEACON, parametrized over all valid
 (rule_bpmx, depth_bpmx) configurations.

 Single fixture: `AStarBPMX.Factory.grid_4x4_beacon(rule, depth)`
 — the canonical 4x4 obstacle grid (start (0,0), goal (0,3),
 optimal cost 7) with a cached beacon at (0,1) holding its
 perfect heuristic value h*=6 (vs. Manhattan=2; gap=4). The
 beacon is the inconsistency engine — without it Rules 1/3/
 CASCADE never lift on consistent Manhattan h, so the test
 matrix would not differentiate configurations.

 Scope (per the cleanup directive):
   - Only methods that test the canonical OOSPP with different
     BPMX configs are kept. Validation tests, toy-graph tests,
     no-cache tests, and feature tests (to_cache, suffix-stitch,
     etc.) have been moved out of this file.
============================================================================
"""

import pytest

from f_hs.algo.i_0_oospp.i_3_astar_bpmx import AStarBPMX


# ─────────────────────────────────────────────────────────────
#  All valid (rule_bpmx, depth_bpmx) configurations.
#  - Rule 2 only at depth=1 (constructor enforces).
#  - Other rules at depth ∈ {1, 2, 3, None}.
# ─────────────────────────────────────────────────────────────

_ALL_CONFIGS = [
    (None, 1),
    ('1', 1), ('1', 2), ('1', 3), ('1', None),
    ('2', 1),
    ('3', 1), ('3', 2), ('3', 3), ('3', None),
    ('CASCADE', 1), ('CASCADE', 2), ('CASCADE', 3),
    ('CASCADE', None),
]


# ─────────────────────────────────────────────────────────────
#  Optimality across configurations
# ─────────────────────────────────────────────────────────────


@pytest.mark.parametrize('rule_bpmx,depth_bpmx', _ALL_CONFIGS)
def test_optimality_grid_4x4_beacon(rule_bpmx: str | None,
                                    depth_bpmx: int | None
                                    ) -> None:
    """
    ========================================================================
     Optimal cost (7) recovered on the canonical 4x4 beacon
     fixture for every valid (rule_bpmx, depth_bpmx) config.
     BPMX lifts (when they fire) must not break admissibility.
    ========================================================================
    """
    algo = AStarBPMX.Factory.grid_4x4_beacon(
        rule_bpmx=rule_bpmx, depth_bpmx=depth_bpmx)
    assert algo.run().cost == 7.0
