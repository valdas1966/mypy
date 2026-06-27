"""
============================================================================
 KAStarInc — opt-in survival instrument (`is_tracing=True`).

 survival[n] = number of inter-sub-search transitions at which
 n was in OPEN = the node's number of `cnt_h_update` h-calls
 (the transition refresh re-prices every OPEN node once). The
 instrument exists to visualize WHY INC's `cnt_h_update` stays
 small: the survival histogram's tail (survive ~k → ~k h-calls
 per node, the AGG-like worst case) is essentially empty.

 Core invariant pinned here:
   sum(survival.values())
     == sum(s * n for s, n in survival_histogram.items())
     == counters['cnt_h_update'].

 Canonical OMSPP (`grid_4x4_obstacle_omspp`): start (0,0),
 goals (0,3)/(3,0)/(3,3); 2 transitions; cnt_h_update = 10.
============================================================================
"""

from f_hs.algo.i_1_omspp.i_1_kastar_inc import KAStarInc
from f_hs.problem.i_1_grid import ProblemGrid


def _h(s, g) -> float:
    return float(s.key.distance(g.key))


def test_survival_off_by_default() -> None:
    """
    ========================================================================
     `is_tracing` defaults to False: the instrument is inert,
     `survival` / `survival_histogram` are empty, and no
     observable counter (e.g. `cnt_h_update`) is perturbed.
    ========================================================================
    """
    p = ProblemGrid.Factory.grid_4x4_obstacle_omspp()
    algo = KAStarInc(problem=p, h=_h)
    algo.run()
    assert algo.is_tracing is False
    assert algo.survival == {}
    assert algo.survival_histogram == {}
    assert algo.counters['cnt_h_update'] == 10


def test_survival_histogram_canonical() -> None:
    """
    ========================================================================
     Pin the survival histogram on the canonical OMSPP:
     2 nodes survive 1 transition, 4 survive 2 transitions.
    ========================================================================
    """
    p = ProblemGrid.Factory.grid_4x4_obstacle_omspp()
    algo = KAStarInc(problem=p, h=_h, is_tracing=True)
    algo.run()
    assert algo.survival_histogram == {1: 2, 2: 4}


def test_survival_sums_to_cnt_h_update() -> None:
    """
    ========================================================================
     The defining invariant: total survival equals
     `cnt_h_update`, both directly and via the histogram.
    ========================================================================
    """
    p = ProblemGrid.Factory.grid_4x4_obstacle_omspp()
    algo = KAStarInc(problem=p, h=_h, is_tracing=True)
    algo.run()
    hist = algo.survival_histogram
    total = sum(algo.survival.values())
    via_hist = sum(s * n for s, n in hist.items())
    assert total == via_hist == algo.counters['cnt_h_update']


def test_survival_accumulates_across_extend() -> None:
    """
    ========================================================================
     Survival follows the counter lifecycle: reset on run(),
     accumulated across extend(). The invariant holds on the
     cumulative state after run() + 2 extend() calls.
    ========================================================================
    """
    p = ProblemGrid.Factory.grid_4x4_obstacle_omspp()
    g1, g2 = p._goals[1], p._goals[2]
    p._goals = p._goals[:1]
    algo = KAStarInc(problem=p, h=_h, is_tracing=True)
    algo.run()
    algo.extend([g1])
    algo.extend([g2])
    assert (sum(algo.survival.values())
            == algo.counters['cnt_h_update'])
