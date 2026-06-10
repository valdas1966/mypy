"""
============================================================================
 DijkstraFlipMOSPP — counter pin on the canonical MOSPP problem
 (`grid_4x4_obstacle_mospp`: starts (0,3) / (3,0) / (3,3); goal
 (0,0); per-start optimal costs 7 / 3 / 6).

 DijkstraFlipMOSPP delegates to OMSPP `KDijkstra` via the flipped
 view. Counters mirror the OMSPP twin one-to-one — identical
 totals to BFSFlipMOSPP on this uniform-cost map (Dijkstra's
 `(g, -g, state)` priority under h ≡ 0 matches BFS FIFO).
============================================================================
"""

from f_hs.algo.i_1_mospp.i_1_dijkstra_flip import DijkstraFlipMOSPP
from f_hs.problem.i_1_grid import ProblemGrid


def test_counters_canonical_mospp() -> None:
    """
    ========================================================================
     Pin DijkstraFlipMOSPP counters on the canonical MOSPP problem.
     14 push / 14 pop in a single inner Dijkstra pass; six
     counters all 0 by construction (no h, no Φ, no lazy
     stale-pop; `cnt_decrease=0` under uniform weights + h≡0).
    ========================================================================
    """
    p = ProblemGrid.Factory.grid_4x4_obstacle_mospp()
    algo = DijkstraFlipMOSPP(problem=p)
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
     problem: (0,3)=7, (3,0)=3, (3,3)=6.
    ========================================================================
    """
    p = ProblemGrid.Factory.grid_4x4_obstacle_mospp()
    algo = DijkstraFlipMOSPP(problem=p)
    sol = algo.run()
    costs = {(s.key.row, s.key.col): v.cost
             for s, v in sol.per_start.items()}
    assert costs == {(0, 3): 7.0, (3, 0): 3.0, (3, 3): 6.0}
