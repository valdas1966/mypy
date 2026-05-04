"""
============================================================================
 AStarLookup — counter pin on the canonical OOSPP problem
 (`grid_4x4_obstacle`: start (0,0), goal (0,3), cost 7,
 Manhattan h, no cache, no bounds).

 AStarLookup inherits the 3-counter scaffold from
 `AlgoSPP.counters` via `AStar`. Without cache or bounds, the
 chain reduces to `HCallable(h)` and behavior matches plain
 `AStar` exactly — the pin matches AStar's. Cache- /
 bounds-driven counter behavior lives in `_tester_cached.py`
 / `_tester_bounded.py`.
============================================================================
"""

from f_hs.algo.i_0_oospp.i_2_astar_lookup import AStarLookup
from f_hs.problem.i_1_grid import ProblemGrid


def test_counters_canonical_oospp() -> None:
    """
    ========================================================================
     Pin AStarLookup counters on the canonical OOSPP problem
     with no cache / no bounds — matches plain AStar exactly.
    ========================================================================
    """
    p = ProblemGrid.Factory.grid_4x4_obstacle()
    goal = p.goal
    algo = AStarLookup(problem=p,
                       h=lambda s: float(s.distance(goal)))
    algo.run()
    assert dict(algo.counters) == {
        'cnt_push': 13,
        'cnt_pop': 9,
        'cnt_decrease': 0,
        'mem_open': 1245,
        'mem_closed': 1819,
        'mem_cache': 0,
        'mem_bounds': 0,
    }
