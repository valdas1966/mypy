"""
============================================================================
 AStarLookupBPMX — counter pin on the canonical OOSPP problem
 (`ProblemGrid.Factory.grid_4x4_obstacle()`: start (0,0),
 goal (0,3), cost 7; no cache; full BPMX cascade).

 The combined class composes `AStarLookup` (cache + bounds)
 with `BPMXMixin` (Felner pathmax / BPMX(d)). On the canonical
 OOSPP problem with no cache and `depth_bpmx=None`, behavior
 reduces to vanilla AStar pop-order plus the BPMX cascade
 (which tightens nothing under consistent Manhattan h). The
 10-counter scaffold reports BPMX activity (8 attempts /
 iterations, 112 subtree states); cnt_pathmax_* and lifts
 stay 0.

 Cache- and bounds-driven scenarios live in
 `_tester_counters_others.py`.
============================================================================
"""

from f_hs.algo.i_0_oospp.i_3_astar_lookup_bpmx import AStarLookupBPMX
from f_hs.problem.i_1_grid import ProblemGrid


def test_counters_canonical_oospp() -> None:
    """
    ========================================================================
     Pin the full 10-counter dict for AStarLookupBPMX on the
     canonical OOSPP problem (no cache, depth_bpmx=None).
     8 BPMX attempts (one per non-goal expansion); cascade
     subtree visits 112 states cumulatively; no lifts under
     consistent Manhattan h.
    ========================================================================
    """
    p = ProblemGrid.Factory.grid_4x4_obstacle()
    goal = p.goal
    algo = AStarLookupBPMX(
        problem=p,
        h=lambda s: float(s.distance(goal)),
        rule_pathmax=None,
        depth_bpmx=None,
    )
    algo.run()
    assert dict(algo.counters) == {
        'cnt_pathmax_attempts': 0,
        'cnt_pathmax_lifts': 0,
        'cnt_bpmx_attempts': 8,
        'cnt_bpmx_iterations': 8,
        'cnt_bpmx_rule3_lifts': 0,
        'cnt_bpmx_rule1_forwards': 0,
        'cnt_bpmx_subtree_states': 112,
        'cnt_push': 13,
        'cnt_pop': 9,
        'cnt_decrease': 0,
        'mem_open': 1245,
        'mem_closed': 1819,
        'mem_cache': 0,
        'mem_bounds': 64,
    }
