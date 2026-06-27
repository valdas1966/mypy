"""
============================================================================
 BFSFlipMOSPP — counter pin on the canonical MOSPP problem
 (`grid_4x4_obstacle_mospp`: starts (0,3) / (3,0) / (3,3); goal
 (0,0); per-start optimal costs 7 / 3 / 6).

 BFSFlipMOSPP delegates to OMSPP `KBFS` via a flipped view (the
 MOSPP goal becomes the OMSPP shared start, the MOSPP starts
 become the OMSPP goals). On this canonical, the flipped view
 is structurally identical to `grid_4x4_obstacle_omspp`, so the
 inner OMSPP `KBFS` does exactly the same work — counters
 match the OMSPP twin one-to-one.
============================================================================
"""

from f_hs.algo.i_1_mospp.i_1_bfs_flip import BFSFlipMOSPP
from f_hs.problem.i_1_grid import ProblemGrid


def test_counters_canonical_mospp() -> None:
    """
    ========================================================================
     Pin BFSFlipMOSPP counters on the canonical MOSPP problem.

     Single inner BFS pass from the shared goal (0,0). 14
     push / 14 pop in BFS layer order; six counters all 0 by
     construction (no h, no Φ, no lazy stale-pop, FIFO has no
     decrease op → synthesized 0). `cnt_expanded = 13` (one pop is
     the final start-pop that terminates the inner search).
    ========================================================================
    """
    p = ProblemGrid.Factory.grid_4x4_obstacle_mospp()
    algo = BFSFlipMOSPP(problem=p)
    algo.run()
    counters = {k: v for k, v in algo.counters.items()
                if not k.startswith('mem_')}
    assert counters == {
        'cnt_push': 14,
        'cnt_pop': 14,
        'cnt_decrease': 0,
        'cnt_expanded': 13,
        'cnt_generated': 14,
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
    algo = BFSFlipMOSPP(problem=p)
    sol = algo.run()
    costs = {(s.key.row, s.key.col): v.cost
             for s, v in sol.per_start.items()}
    assert costs == {(0, 3): 7.0, (3, 0): 3.0, (3, 3): 6.0}
