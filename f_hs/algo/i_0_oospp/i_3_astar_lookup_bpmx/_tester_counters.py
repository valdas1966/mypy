"""
============================================================================
 AStarLookupBPMX — counter pin on the canonical OOSPP problem
 (`ProblemGrid.Factory.grid_4x4_obstacle()`: start (0,0),
 goal (0,3), cost 7; no cache; CASCADE depth=None).

 The combined class composes `AStarLookup` (cache + bounds)
 with `BPMXMixin` (rule_bpmx-driven mechanism). On the canonical
 OOSPP problem with no cache and CASCADE, behavior reduces to
 vanilla AStar pop-order plus the cascade (which tightens
 nothing under consistent Manhattan h).

 Cache- and bounds-driven scenarios live in
 `_tester_counters_others.py`.
============================================================================
"""

from f_hs.algo.i_0_oospp.i_3_astar_lookup_bpmx import AStarLookupBPMX


def test_counters_canonical_oospp() -> None:
    """
    ========================================================================
     Pin the full counter dict for AStarLookupBPMX on the
     canonical OOSPP problem with rule_bpmx='CASCADE',
     depth_bpmx=None. 8 cascade attempts (one per non-goal
     expansion); 0 successes (consistent h); 0 depth (no
     lifts); frontier 13/9/0; expanded 8 / generated 13;
     prop counters 0 (propagate_pathmax not called).
    ========================================================================
    """
    algo = AStarLookupBPMX.Factory.grid_4x4_no_cache(
        rule_bpmx='CASCADE', depth_bpmx=None)
    algo.run()
    counters = {k: v for k, v in algo.counters.items()
                if not k.startswith('mem_')}
    assert counters == {
        'cnt_prop_waves': 0,
        'cnt_prop_attempts': 0,
        'cnt_prop_lifts': 0,
        'cnt_bpmx_attempts': 8,
        'cnt_bpmx_successes': 0,
        'cnt_bpmx_depth': 0,
        'cnt_push': 13,
        'cnt_pop': 9,
        'cnt_decrease': 0,
        'cnt_expanded': 8,
        'cnt_generated': 13,
    }
