"""
============================================================================
 KDijkstra — counter pin on the canonical OMSPP problem
 (`grid_4x4_obstacle_omspp`: start (0,0), goals (0,3) / (3,0)
 / (3,3); per-goal optimal costs 7 / 3 / 6).

 KDijkstra runs a SINGLE inner Dijkstra pass with multi-goal
 early-exit (no per-goal sub-search restarts). Four of the
 eight counters are structurally zero (cnt_h_*, cnt_phi_*,
 cnt_pop_stale); cnt_decrease is heap-op (would fire on a
 mid-search g-tightening, but stays at 0 here under uniform
 weights and h ≡ 0).
============================================================================
"""

from f_hs.algo.i_1_omspp.i_2_kdijkstra import KDijkstra
from f_hs.problem.i_1_grid import ProblemGrid


def test_counters_canonical_omspp() -> None:
    """
    ========================================================================
     Pin KDijkstra counters on the canonical OMSPP problem.
     14 push / 14 pop in a single inner Dijkstra pass —
     identical totals to KBFS on this uniform-cost map (BFS
     FIFO order ≡ Dijkstra `(g, -g, state)` order under h≡0).
     Verifies the single-pass design does NOT inflate cnt_push
     (no priority refresh, no force-expand pushes).
    ========================================================================
    """
    p = ProblemGrid.Factory.grid_4x4_obstacle_omspp()
    algo = KDijkstra(problem=p)
    algo.run()
    assert dict(algo.counters) == {
        'cnt_h_search': 0,
        'cnt_h_update': 0,
        'cnt_phi_search': 0,
        'cnt_phi_update': 0,
        'cnt_push': 14,
        'cnt_pop': 14,
        'cnt_pop_stale': 0,
        'cnt_decrease': 0,
        'mem_open': 280,
        'mem_closed': 2328,
    }


def test_per_goal_costs_canonical_omspp() -> None:
    """
    ========================================================================
     Pin per-goal optimal costs (KDijkstra) on the canonical
     OMSPP problem: (0,3)=7, (3,0)=3, (3,3)=6.
    ========================================================================
    """
    p = ProblemGrid.Factory.grid_4x4_obstacle_omspp()
    algo = KDijkstra(problem=p)
    sol = algo.run()
    costs = {(g.key.row, g.key.col): s.cost
             for g, s in sol.per_goal.items()}
    assert costs == {(0, 3): 7.0, (3, 0): 3.0, (3, 3): 6.0}
