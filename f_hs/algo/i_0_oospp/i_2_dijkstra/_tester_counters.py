"""
============================================================================
 Dijkstra — counter pin on the canonical OOSPP problem
 (`grid_4x4_obstacle`: start (0,0), goal (0,3), cost 7).

 Dijkstra is `AStar` with `h ≡ 0`. Unlike Manhattan-h AStar
 (which expands 9 states), Dijkstra explores by `g` alone —
 it expands every state with `g ≤ goal_cost` before
 terminating. Pin matches BFS exactly on a unit-cost grid:
 14 push / 14 pop / 0 decrease.
============================================================================
"""

from f_hs.algo.i_0_oospp.i_2_dijkstra import Dijkstra
from f_hs.problem.i_1_grid import ProblemGrid


def test_counters_canonical_oospp() -> None:
    """
    ========================================================================
     Pin Dijkstra counters on the canonical OOSPP problem.
     14 push / 14 pop / 0 decrease — Dijkstra explores by g
     alone; on a unit-cost grid it pops every reachable state
     with g ≤ 7 before terminating at the goal.
    ========================================================================
    """
    p = ProblemGrid.Factory.grid_4x4_obstacle()
    algo = Dijkstra(problem=p)
    algo.run()
    assert dict(algo.counters) == {
        'cnt_push': 14,
        'cnt_pop': 14,
        'cnt_decrease': 0,
        'mem_open': 280,
        'mem_closed': 2328,
    }
