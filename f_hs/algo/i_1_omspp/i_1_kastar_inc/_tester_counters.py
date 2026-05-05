"""
============================================================================
 KAStarInc — counter pin on the canonical OMSPP problem
 (`grid_4x4_obstacle_omspp`: start (0,0), goals (0,3) / (3,0)
 / (3,3); per-goal optimal costs 7 / 3 / 6; Manhattan h to
 the active goal).

 KAStarInc reuses the SearchStateSPP bundle across k=3
 sub-searches under the lazy re-push design — non-last
 reached goals re-enter OPEN with their optimal g; the last
 goal does not. Counter scaffold is the per-class
 `_COUNTER_NAMES` (no Φ counters, no `cnt_pop_stale`).
============================================================================
"""

from f_hs.algo.i_1_omspp.i_1_kastar_inc import KAStarInc
from f_hs.problem.i_1_grid import ProblemGrid


def test_counters_canonical_omspp() -> None:
    """
    ========================================================================
     Pin KAStarInc counters on the canonical OMSPP problem.

     Decomposition (no recording):

       cnt_push = 26
         = 14 search-driven pushes (start seed + first-time
           successor pushes during the 3 sub-searches)
         + 2 lazy re-push events for the non-last goals
           ((0,3) re-pushed after sub-search 0; (3,0)
           re-pushed after sub-search 1; (3,3) NOT re-pushed
           since it's the last goal)
         + 10 silent `refresh_priorities()` re-pushes
           (5 frontier states × 2 transitions; the re-pushed
           goals participate in subsequent refreshes).

       cnt_pop = 12 — total pops across the 3 sub-searches.

       cnt_decrease = 0 — consistent Manhattan h on a
         uniform-cost grid never tightens g via a back-edge.

       cnt_h_search = 16
         = 14 priority-computation h-calls during the
           sub-searches' pushes (no recording, so no
           per-event enrichment)
         + 2 h-calls for the lazy re-push priority
           computation under PHASE_SEARCH.

       cnt_h_update = 10
         = 5 frontier states × 2 transitions × 1 h-call per
           state (the explicit refresh_priorities() drain and
           rebuild). The legacy `update_heuristic` event
           cluster (which would have added 2 prev_h+new_h
           calls per frontier state) was removed — the per-
           state heuristic re-keying is observable through
           `refresh_priorities` and the `push` events it
           emits during drain-and-rebuild.

     `cnt_phi_*` and `cnt_pop_stale` are NOT in
     KAStarInc's scaffold (per-class `_COUNTER_NAMES`).

     This pin is RECORDING-OFF. With recording on,
     `cnt_h_search` inflates because AStar's `_enrich_event`
     calls h once per push/pop event.
    ========================================================================
    """
    p = ProblemGrid.Factory.grid_4x4_obstacle_omspp()
    algo = KAStarInc(problem=p,
                     h=lambda s, g: float(s.distance(g)))
    algo.run()
    counters = {k: v for k, v in algo.counters.items()
                if not k.startswith('mem_')}
    assert counters == {
        'cnt_h_search': 16,
        'cnt_h_update': 10,
        'cnt_push': 26,
        'cnt_pop': 12,
        'cnt_decrease': 0,
        'cnt_expanded': 9,
        'cnt_generated': 14,
    }


def test_per_goal_costs_canonical_omspp() -> None:
    """
    ========================================================================
     Pin per-goal optimal costs on the canonical OMSPP
     problem: (0,3)=7, (3,0)=3, (3,3)=6.
    ========================================================================
    """
    p = ProblemGrid.Factory.grid_4x4_obstacle_omspp()
    algo = KAStarInc(problem=p,
                     h=lambda s, g: float(s.distance(g)))
    sol = algo.run()
    costs = {(g.key.row, g.key.col): s.cost
             for g, s in sol.per_goal.items()}
    assert costs == {(0, 3): 7.0, (3, 0): 3.0, (3, 3): 6.0}
