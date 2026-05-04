"""
============================================================================
 BFS — counter pin on the canonical OOSPP problem
 (`grid_4x4_obstacle`: start (0,0), goal (0,3), cost 7).

 BFS inherits the 3-counter scaffold from `AlgoSPP.counters`
 (frontier-mirrored from `FrontierFIFO`). FIFO never decreases
 — `cnt_decrease` is structurally 0 for BFS.
============================================================================
"""

from f_hs.algo.i_0_oospp.i_1_bfs import BFS
from f_hs.problem.i_1_grid import ProblemGrid


def test_counters_canonical_oospp() -> None:
    """
    ========================================================================
     Pin BFS counters on the canonical OOSPP problem.
     14 push / 14 pop — BFS expands every reachable state at
     depth ≤ goal-depth before terminating; `cnt_decrease=0`
     since FIFO has no decrease op.
    ========================================================================
    """
    p = ProblemGrid.Factory.grid_4x4_obstacle()
    algo = BFS(problem=p)
    algo.run()
    assert dict(algo.counters) == {
        'cnt_push': 14,
        'cnt_pop': 14,
        'cnt_decrease': 0,
        'mem_open': 760,
        'mem_closed': 2328,
    }
