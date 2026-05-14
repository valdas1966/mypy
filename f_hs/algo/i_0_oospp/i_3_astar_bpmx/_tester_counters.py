"""
============================================================================
 AStarBPMX --- counter pin matrix on the 6x6 zigzag OOSPP problem
 with a CACHED INCONSISTENCY BEACON, parametrized over all
 valid (rule_bpmx, depth_bpmx) configurations.

 Single fixture: `AStarBPMX.Factory.grid_6x6_zigzag_beacon(rule, depth)`
 --- 6x6 snake-detour grid + cached beacon at (1,0) with h*=14
 (vs. Manhattan=4; gap=10). Optimal cost = 15. The beacon and
 the long-detour topology together create multi-cell, multi-
 depth lift opportunities, so the counters genuinely
 differentiate across (rule, depth):

   - Rule 1 depth axis ({1, 2, 3, None}): successes {0, 1, 2, 5}
     and cnt_expanded {20, 19, 18, 15} --- strict monotone.
   - Rule 3 depth axis: successes {5, 6, 7, 9}, expanded
     {20, 19, 18, 15} --- strict monotone.
   - CASCADE depth axis: successes {6, 9, 9, 9}, expanded
     {20, 18, 16, 15} --- saturates on lifts but continues to
     prune expansions through depth=3.
   - Rule 2 (depth=1 only): 6 lifts at parent (depth_max=0).
   - CASCADE vs. Rule 3 at depth=1: 6 vs. 5 (CASCADE's
     fixed-point iteration finds one extra lift).

 Across ALL configs, these counters are CONSTANT:
   cnt_prop_*   = 0   (no pre-search propagate_pathmax called)
   cnt_decrease = 0   (no re-relaxation on this fixture)

 The 4x4 beacon fixture --- previously used here --- yields
 only binary signals on this matrix (successes 0 or 2,
 depth_max 0 or 2, cnt_expanded constant at 7), so it cannot
 demonstrate depth monotonicity, search pruning, or
 CASCADE > Rule 1 separation. See session 2026-05-14, Q2.
============================================================================
"""

import pytest

from f_hs.algo.i_0_oospp.i_3_astar_bpmx import AStarBPMX


# ─────────────────────────────────────────────────────────────
#  Per-config counter expectations on grid_6x6_zigzag_beacon
#  (rule, depth, att, suc, depth_max, exp, gen)
#
#  cnt_push and cnt_pop are dropped from the pin --- they are
#  derivable from gen and exp on this fixture (push = gen,
#  pop = exp + 1, since the start is pushed and the goal is
#  popped without expansion) and carry no extra signal.
# ─────────────────────────────────────────────────────────────

_BPMX_COUNTER_MATRIX = [
    # rule,      depth, att, suc, dmax, exp, gen
    (None,        1,    0,   0,   0,    20,  27),
    ('1',         1,    20,  0,   0,    20,  27),
    ('1',         2,    19,  1,   2,    19,  27),
    ('1',         3,    18,  2,   3,    18,  26),
    ('1',         None, 15,  5,   6,    15,  23),
    ('2',         1,    20,  6,   0,    20,  27),
    ('3',         1,    20,  5,   0,    20,  27),
    ('3',         2,    19,  6,   1,    19,  27),
    ('3',         3,    18,  7,   2,    18,  26),
    ('3',         None, 15,  9,   5,    15,  23),
    ('CASCADE',   1,    20,  6,   1,    20,  27),
    ('CASCADE',   2,    18,  9,   2,    18,  26),
    ('CASCADE',   3,    16,  9,   3,    16,  24),
    ('CASCADE',   None, 15,  9,   6,    15,  23),
]


# ─────────────────────────────────────────────────────────────
#  Full counter pin per configuration
# ─────────────────────────────────────────────────────────────


_DROP_KEYS = frozenset({'cnt_push', 'cnt_pop'})


@pytest.mark.parametrize(
    'rule_bpmx,depth_bpmx,att,suc,depth_max,exp,gen',
    _BPMX_COUNTER_MATRIX,
)
def test_counters_grid_6x6_zigzag_beacon(rule_bpmx: str | None,
                                         depth_bpmx: int | None,
                                         att: int,
                                         suc: int,
                                         depth_max: int,
                                         exp: int,
                                         gen: int) -> None:
    """
    ========================================================================
     Pin the full counter dict (modulo memory + frontier-op
     snapshots) for every valid (rule_bpmx, depth_bpmx)
     configuration on the 6x6 zigzag beacon fixture. Optimal
     cost is always 15; cnt_prop_* and cnt_decrease are
     constant 0; the BPMX trio (att/suc/depth_max) and the
     search trio (exp/gen) are the discriminating signal.
    ========================================================================
    """
    algo = AStarBPMX.Factory.grid_6x6_zigzag_beacon(
        rule_bpmx=rule_bpmx, depth_bpmx=depth_bpmx)
    algo.run()
    counters = {k: v for k, v in algo.counters.items()
                if not k.startswith('mem_') and k not in _DROP_KEYS}
    assert counters == {
        'cnt_prop_waves':     0,
        'cnt_prop_attempts':  0,
        'cnt_prop_lifts':     0,
        'cnt_bpmx_attempts':  att,
        'cnt_bpmx_successes': suc,
        'cnt_bpmx_depth':     depth_max,
        'cnt_decrease':       0,
        'cnt_expanded':       exp,
        'cnt_generated':      gen,
    }
