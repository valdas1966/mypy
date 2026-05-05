"""
============================================================================
 AStar — counter pin on the canonical OOSPP problem
 (`grid_4x4_obstacle`: start (0,0), goal (0,3), cost 7,
 Manhattan h).

 AStar inherits the 5-counter scaffold from `AlgoSPP.counters`
 — heap-op group (cnt_push / cnt_pop / cnt_decrease, mirrored
 from `FrontierPriority`) and search-semantic group
 (cnt_expanded / cnt_generated, incremented inline by
 `_search_loop` and `_handle_child`). With Manhattan h
 (consistent on a 4-connected unit-cost grid), `cnt_decrease`
 is structurally 0 — re-discovery never improves g.
============================================================================
"""

from f_hs.algo.i_0_oospp.i_1_astar import AStar
from f_hs.problem.i_1_grid import ProblemGrid


def test_counters_canonical_oospp() -> None:
    """
    ========================================================================
     Pin AStar counters on the canonical OOSPP problem.
     13 push / 9 pop — AStar expands 8 states + the goal pop;
     `cnt_decrease=0` under consistent Manhattan h.
    ========================================================================
    """
    p = ProblemGrid.Factory.grid_4x4_obstacle()
    goal = p.goal
    algo = AStar(problem=p, h=lambda s: float(s.distance(goal)))
    algo.run()
    counters = {k: v for k, v in algo.counters.items()
                if not k.startswith('mem_')}
    assert counters == {
        'cnt_push': 13,
        'cnt_pop': 9,
        'cnt_decrease': 0,
        'cnt_expanded': 8,
        'cnt_generated': 13,
    }


def test_counters_graph_decrease() -> None:
    """
    ========================================================================
     Pin AStar counters on the graph_decrease scenario — the
     only canonical case that exercises a `decrease_g` call
     (`cnt_decrease == 1`).
    ========================================================================
    """
    algo = AStar.Factory.graph_decrease()
    algo.run()
    counters = {k: v for k, v in algo.counters.items()
                if not k.startswith('mem_')}
    assert counters == {
        'cnt_push': 4, 'cnt_pop': 4, 'cnt_decrease': 1,
        'cnt_expanded': 3, 'cnt_generated': 4,
    }
