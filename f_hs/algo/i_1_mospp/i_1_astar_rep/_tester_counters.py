"""
============================================================================
 AStarRepMOSPP — counter pin on the canonical MOSPP problem
 (`grid_4x4_obstacle_mospp`: starts (0,3) / (3,0) / (3,3);
 goal (0,0); per-start optimal costs 7 / 3 / 6; Manhattan
 h to the fixed goal).

 AStarRepMOSPP runs k INDEPENDENT A* sub-searches (no shared
 SearchStateSPP). Each sub-search begins at a different
 start, uses the SAME h(state, goal=(0,0)), and is then
 discarded. The cumulative counter dict sums work across
 sub-searches.

 Counter scaffold (per-class `_COUNTER_NAMES`): drops
 `cnt_h_update` (no PHASE_UPDATE flips — kxA*-MOSPP has no
 between-sub-search refresh). Honest minimal set.
============================================================================
"""

from f_hs.algo.i_1_mospp.i_1_astar_rep import AStarRepMOSPP
from f_hs.problem.i_1_grid import ProblemGrid


def test_counters_canonical_mospp() -> None:
    """
    ========================================================================
     Pin AStarRepMOSPP counters on the canonical MOSPP problem.

     Decomposition (recording OFF):

       cnt_push = 33      = 12 + 9 + 12 across the 3 starts
       cnt_pop  = 21      = 8 + 6 + 7 (each minus 1 goal-pop)
       cnt_decrease = 0
       cnt_h_search = 33  = 1 per push (priority computation;
                            recording OFF, no enrichment h-calls)
       cnt_expanded = 18  = cnt_pop − 3 goal-pops
       cnt_generated = 33 = cnt_push (no decrease-key, no re-pushes)

     `cnt_h_update`, `cnt_phi_*`, `cnt_pop_stale` are NOT
     in this scaffold (per-class `_COUNTER_NAMES`).

     Pin is RECORDING-OFF, matching the OMSPP convention.
    ========================================================================
    """
    p = ProblemGrid.Factory.grid_4x4_obstacle_mospp()
    algo = AStarRepMOSPP(problem=p,
                        h=lambda s, g: float(s.key.distance(g.key)))
    algo.run()
    counters = {k: v for k, v in algo.counters.items()
                if not k.startswith('mem_')}
    assert counters == {
        'cnt_h_search': 33,
        'cnt_push': 33,
        'cnt_pop': 21,
        'cnt_decrease': 0,
        'cnt_expanded': 18,
        'cnt_generated': 33,
    }


def test_per_start_costs_canonical_mospp() -> None:
    """
    ========================================================================
     Pin per-start optimal costs on the canonical MOSPP
     problem: (0,3)=7, (3,0)=3, (3,3)=6. Matches the OMSPP
     twin's per-goal costs by graph symmetry (undirected
     grid).
    ========================================================================
    """
    p = ProblemGrid.Factory.grid_4x4_obstacle_mospp()
    algo = AStarRepMOSPP(problem=p,
                        h=lambda s, g: float(s.key.distance(g.key)))
    sol = algo.run()
    costs = {(s.key.row, s.key.col): v.cost
             for s, v in sol.per_start.items()}
    assert costs == {(0, 3): 7.0, (3, 0): 3.0, (3, 3): 6.0}
