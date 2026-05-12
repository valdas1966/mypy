"""
============================================================================
 AStarBPMX — counter pin matrix on the canonical OOSPP problem
 with a CACHED INCONSISTENCY BEACON, parametrized over all
 valid (rule_bpmx, depth_bpmx) configurations.

 Single fixture: `AStarBPMX.Factory.grid_4x4_beacon(rule, depth)`
 — canonical 4x4 obstacle grid + cached beacon at (0,1) with
 h*=6 (vs. Manhattan=2; gap=4). The beacon is the inconsistency
 engine.

 Across ALL valid configs, these counters are CONSTANT:
   cnt_prop_*    = 0  (no pre-search propagate_pathmax called)
   cnt_push      = 13
   cnt_pop       = 8
   cnt_decrease  = 0
   cnt_expanded  = 7
   cnt_generated = 13

 The BPMX-specific counters (cnt_bpmx_attempts /
 cnt_bpmx_successes / cnt_bpmx_depth) vary per config and
 are the discriminating signal.
============================================================================
"""

import pytest

from f_hs.algo.i_0_oospp.i_3_astar_bpmx import AStarBPMX


# ─────────────────────────────────────────────────────────────
#  Per-config BPMX-counter expectations
#  (rule, depth, attempts, successes, max-lift-depth)
# ─────────────────────────────────────────────────────────────

_BPMX_COUNTER_MATRIX = [
    # (rule_bpmx, depth_bpmx, att, suc, depth_max)
    (None,       1,    0, 0, 0),
    ('1',        1,    7, 0, 0),
    ('1',        2,    7, 2, 2),
    ('1',        3,    7, 2, 2),
    ('1',        None, 7, 2, 2),
    ('2',        1,    7, 2, 0),
    ('3',        1,    7, 2, 0),
    ('3',        2,    7, 2, 0),
    ('3',        3,    7, 2, 0),
    ('3',        None, 7, 2, 0),
    ('CASCADE',  1,    7, 2, 0),
    ('CASCADE',  2,    7, 2, 2),
    ('CASCADE',  3,    7, 2, 2),
    ('CASCADE',  None, 7, 2, 2),
]


# ─────────────────────────────────────────────────────────────
#  Full counter pin per configuration
# ─────────────────────────────────────────────────────────────


@pytest.mark.parametrize(
    'rule_bpmx,depth_bpmx,att,suc,depth_max',
    _BPMX_COUNTER_MATRIX,
)
def test_counters_grid_4x4_beacon(rule_bpmx: str | None,
                                  depth_bpmx: int | None,
                                  att: int,
                                  suc: int,
                                  depth_max: int) -> None:
    """
    ========================================================================
     Pin the full counter dict (modulo memory snapshots) for
     every valid (rule_bpmx, depth_bpmx) configuration on the
     canonical 4x4 beacon fixture. The frontier / search-
     semantic counters are constant across configs; the BPMX
     trio (attempts / successes / depth) is the matrix.
    ========================================================================
    """
    algo = AStarBPMX.Factory.grid_4x4_beacon(
        rule_bpmx=rule_bpmx, depth_bpmx=depth_bpmx)
    algo.run()
    counters = {k: v for k, v in algo.counters.items()
                if not k.startswith('mem_')}
    assert counters == {
        'cnt_prop_waves': 0,
        'cnt_prop_attempts': 0,
        'cnt_prop_lifts': 0,
        'cnt_bpmx_attempts': att,
        'cnt_bpmx_successes': suc,
        'cnt_bpmx_depth': depth_max,
        'cnt_push': 13,
        'cnt_pop': 8,
        'cnt_decrease': 0,
        'cnt_expanded': 7,
        'cnt_generated': 13,
    }
