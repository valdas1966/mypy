"""
============================================================================
 KAStarInc -- nested-extend manual counter pins on canonical OMSPP.

 Canonical OMSPP problem (`grid_4x4_obstacle_omspp`: start
 (0,0), goals (0,3) / (3,0) / (3,3); Manhattan h to the
 active goal).

 The nested-extend chain
 `run([g0]) -> extend([g1]) -> extend([g2])` is run once, and
 at each stage the cumulative non-mem counter dict is asserted
 against hardcoded manual values. Drift in either the nested-
 extend logic or the underlying single-shot algorithm will
 surface here -- the all-at-once 3-goal pin lives separately
 in `_tester_counters.py`.
============================================================================
"""

from f_hs.algo.i_1_omspp.i_1_kastar_inc import KAStarInc
from f_hs.problem.i_1_grid import ProblemGrid


def _h(s, g) -> float:
    return float(s.distance(g))


def _strip_mem(counters) -> dict:
    return {k: v for k, v in counters.items()
            if not k.startswith('mem_')}


def test_extend_counters_manual_pins() -> None:
    """
    ========================================================================
     Pin cumulative non-mem counters at each stage of the
     nested-extend chain on the canonical 3-goal OMSPP problem.
     Values are hardcoded; any change in nested-extend logic or
     in the underlying single-shot algorithm surfaces here.
    ========================================================================
    """
    # Hardcoded counter pins -- grid_4x4_obstacle_omspp
    # (start (0,0); goals (0,3)/(3,0)/(3,3); Manhattan h).
    target_k1 = \
        {
            'cnt_h_search': 13,
            'cnt_h_update': 0,
            'cnt_push': 13,
            'cnt_pop': 9,
            'cnt_decrease': 0,
            'cnt_expanded': 8,
            'cnt_generated': 13,
        }
    target_k2 =\
        {
            'cnt_h_search': 14,
            'cnt_h_update': 5,
            'cnt_push': 20,
            'cnt_pop': 11,
            'cnt_decrease': 0,
            'cnt_expanded': 9,
            'cnt_generated': 14,
        }
    target_k3 =\
        {
            'cnt_h_search': 14,
            'cnt_h_update': 10,
            'cnt_push': 26,
            'cnt_pop': 12,
            'cnt_decrease': 0,
            'cnt_expanded': 9,
            'cnt_generated': 14,
        }

    # Nested -- start with goal 0, extend to goal 1, then goal 2.
    p = ProblemGrid.Factory.grid_4x4_obstacle_omspp()
    g1, g2 = p._goals[1], p._goals[2]
    p._goals = p._goals[:1]
    algo = KAStarInc(problem=p, h=_h)

    # Stage k=1: run([g0]).
    algo.run()
    assert _strip_mem(algo.counters) == target_k1

    # Stage k=2: extend([g1]).
    algo.extend([g1])
    assert _strip_mem(algo.counters) == target_k2

    # Stage k=3: extend([g2]).
    algo.extend([g2])
    assert _strip_mem(algo.counters) == target_k3
