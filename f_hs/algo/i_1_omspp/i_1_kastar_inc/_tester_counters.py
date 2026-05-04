"""
============================================================================
 KAStarInc — counter pin on the canonical OMSPP problem
 (`grid_4x4_obstacle_omspp`: start (0,0), goals (0,3) / (3,0)
 / (3,3); per-goal optimal costs 7 / 3 / 6; Manhattan h to
 the active goal).

 KAStarInc reuses the SearchStateSPP bundle across k=3
 sub-searches. The 8-counter scaffold inherits from
 `AlgoOMSPP`. Φ-counters stay 0 (Inc has no aggregation).
============================================================================
"""

from f_hs.algo.i_1_omspp.i_1_kastar_inc import KAStarInc
from f_hs.problem.i_1_grid import ProblemGrid


def test_counters_canonical_omspp() -> None:
    """
    ========================================================================
     Pin KAStarInc counters on the canonical OMSPP problem.
     21 push / 12 pop across 3 sub-searches; cnt_decrease=0
     under consistent Manhattan h; cnt_h_search=14 reflects
     priority computations during sub-search (one h call per
     push, total 14 pushes minus the start that uses g=0);
     cnt_h_update=21 reflects priority refresh between
     sub-searches (full frontier re-priced when the goal
     changes).

     Counters are identical with `is_recording` on or off
     for KAStarAgg; for KAStarInc, `cnt_h_search` is
     RECORDING-DEPENDENT — event enrichment calls h once per
     push/pop event, inflating it. This pin is for the
     no-recording case (which is what this tester runs).
    ========================================================================
    """
    p = ProblemGrid.Factory.grid_4x4_obstacle_omspp()
    algo = KAStarInc(problem=p,
                     h=lambda s, g: float(s.distance(g)))
    algo.run()
    assert dict(algo.counters) == {
        'cnt_h_search': 14,
        'cnt_h_update': 21,
        'cnt_phi_search': 0,
        'cnt_phi_update': 0,
        'cnt_push': 21,
        'cnt_pop': 12,
        'cnt_pop_stale': 0,
        'cnt_decrease': 0,
        'mem_open': 685,
        'mem_closed': 2099,
    }


def test_per_goal_costs_canonical_omspp() -> None:
    """
    ========================================================================
     Pin per-goal optimal costs on the canonical OMSPP
     problem: (0,3)=7, (3,0)=3, (3,3)=6.
    ========================================================================
    """
    p = ProblemGrid.Factory.grid_4x4_obstacle_omspp()
    algo = KAStarInc(problem=p,
                     h=lambda s, g: float(s.distance(g)))
    sol = algo.run()
    costs = {(g.key.row, g.key.col): s.cost
             for g, s in sol.per_goal.items()}
    assert costs == {(0, 3): 7.0, (3, 0): 3.0, (3, 3): 6.0}
