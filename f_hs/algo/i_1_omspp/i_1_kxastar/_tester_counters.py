"""
============================================================================
 KxAStarOMSPP — counter pin on the canonical OMSPP problem
 (`grid_4x4_obstacle_omspp`: start (0,0), goals (0,3) / (3,0)
 / (3,3); per-goal optimal costs 7 / 3 / 6; Manhattan h to
 the active goal).

 KxAStarOMSPP runs k INDEPENDENT A* sub-searches (no shared
 SearchStateSPP across sub-searches). Each sub-search expands
 the relevant subset of the grid from scratch under its OWN
 heuristic h(·, goal_i). The cumulative counter dict is the
 sum across the three sub-searches.

 Counter scaffold (per-class `_COUNTER_NAMES`): drops
 `cnt_h_update` (no PHASE_UPDATE flips — there is no
 between-sub-search refresh in kxA*). The honest minimal
 set is `cnt_h_search`, three heap-op counters,
 `cnt_expanded`, `cnt_generated`, plus the two memory
 counters.
============================================================================
"""

from f_hs.algo.i_1_omspp.i_1_kxastar import KxAStarOMSPP
from f_hs.problem.i_1_grid import ProblemGrid


def test_counters_canonical_omspp() -> None:
    """
    ========================================================================
     Pin KxAStarOMSPP counters on the canonical OMSPP problem.

     Decomposition (recording OFF):

       cnt_push = 32
         Sub-search 1 (goal (0,3)): 13 first-time pushes
           (start + 12 children generated along the
           south-through-row-2 detour).
         Sub-search 2 (goal (3,0)): 7 first-time pushes
           (start + 6 children, straight-south route
           plus the southward-frontier branches).
         Sub-search 3 (goal (3,3)): 12 first-time pushes
           (start + 11 children explored to reach (3,3)).
         Each sub-search builds its own frontier from
         scratch — no state sharing reuses prior pushes.

       cnt_pop = 20 — total pops across the 3 sub-searches.

       cnt_decrease = 0 — consistent Manhattan h on a
         uniform-cost grid never tightens g via a back-edge.

       cnt_h_search = 32 — one h-call per push for the
         priority computation (recording OFF, so no
         per-event enrichment h-calls; under recording ON
         this would inflate to 2·cnt_push + cnt_pop = 84).

       cnt_expanded = 17 — every pop closes its state and
         expands successors, EXCEPT for the per-sub-search
         goal-pop (3 goal-pops: (0,3), (3,0), (3,3)). So
         cnt_expanded = cnt_pop - 3 = 17.

       cnt_generated = 32 — every first-time push (no
         decrease-key, no re-pushes in kxA*); equals
         cnt_push exactly.

     `cnt_h_update`, `cnt_phi_*`, `cnt_pop_stale` are NOT
     in KxAStarOMSPP's scaffold (per-class `_COUNTER_NAMES`).

     This pin is RECORDING-OFF, matching the
     KAStarInc / KAStarAgg counter pin convention.
    ========================================================================
    """
    p = ProblemGrid.Factory.grid_4x4_obstacle_omspp()
    algo = KxAStarOMSPP(problem=p,
                   h=lambda s, g: float(s.distance(g)))
    algo.run()
    counters = {k: v for k, v in algo.counters.items()
                if not k.startswith('mem_')}
    assert counters == {
        'cnt_h_search': 32,
        'cnt_push': 32,
        'cnt_pop': 20,
        'cnt_decrease': 0,
        'cnt_expanded': 17,
        'cnt_generated': 32,
    }


def test_per_goal_costs_canonical_omspp() -> None:
    """
    ========================================================================
     Pin per-goal optimal costs on the canonical OMSPP
     problem: (0,3)=7, (3,0)=3, (3,3)=6. Identical to the
     KAStarInc / KAStarAgg pins — kxA* is also optimal under
     admissible h.
    ========================================================================
    """
    p = ProblemGrid.Factory.grid_4x4_obstacle_omspp()
    algo = KxAStarOMSPP(problem=p,
                   h=lambda s, g: float(s.distance(g)))
    sol = algo.run()
    costs = {(g.key.row, g.key.col): s.cost
             for g, s in sol.per_goal.items()}
    assert costs == {(0, 3): 7.0, (3, 0): 3.0, (3, 3): 6.0}
