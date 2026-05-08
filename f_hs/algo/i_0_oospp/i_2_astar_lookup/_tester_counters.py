"""
============================================================================
 AStarLookup — counter pin on the canonical OOSPP problem
 (`grid_4x4_obstacle`: start (0,0), goal (0,3), cost 7,
 Manhattan h, no cache, no bounds).

 AStarLookup declares a 12-name scaffold (propagate 3 +
 frontier 3 + search 2 + memory 4). Without cache or bounds,
 the chain reduces to `HCallable(h)` and the search-step
 counts match plain `AStar` exactly — the propagate group
 stays at zero (no `propagate_pathmax()` call). BPMX-side
 counters live on `AStarBPMX` (`i_3_astar_bpmx/`).
============================================================================
"""

from f_hs.algo.i_0_oospp.i_2_astar_lookup import AStarLookup
from f_hs.problem.i_1_grid import ProblemGrid


def test_counters_canonical_oospp() -> None:
    """
    ========================================================================
     Pin AStarLookup counters on the canonical OOSPP problem
     with no cache / no bounds — search-step counts match
     plain AStar; propagate counters stay at zero.
    ========================================================================
    """
    p = ProblemGrid.Factory.grid_4x4_obstacle()
    goal = p.goal
    algo = AStarLookup(problem=p,
                       h=lambda s: float(s.distance(goal)))
    algo.run()
    counters = {k: v for k, v in algo.counters.items()
                if not k.startswith('mem_')}
    assert counters == {
        'cnt_prop_waves': 0,
        'cnt_prop_attempts': 0,
        'cnt_prop_lifts': 0,
        'cnt_push': 13,
        'cnt_pop': 9,
        'cnt_decrease': 0,
        'cnt_expanded': 8,
        'cnt_generated': 13,
    }
