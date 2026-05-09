"""
============================================================================
 AStarLookup — counter pins on the canonical OOSPP problem
 (`grid_4x4_obstacle`: start (0,0), goal (0,3), wall at
 (0,2)/(1,2), Manhattan h, optimal cost 7).

 Four scenarios pin the lookup-side counter scaffold (12-name:
 propagate 3 + frontier 3 + search 2 + memory 4) along the
 AStarLookup informativity axis:

   - test_counters_baseline — no cache, no bounds. AStarLookup
     reduces to plain AStar over Manhattan h; pins the
     comparison anchor against which `cached` / `bounded` /
     `bounded_propagated` deltas read off (9 pops / 13 pushes /
     8 expansions).

   - test_counters_cached  — single best cache node = (1,1) at
     h_perfect=5. Cache-hit early-term fires when (1,1) pops
     (cost = g + h_perfect = 2 + 5 = 7); cache_rank=0 ensures
     (1,1) wins the f=7 tiebreak. Significantly shrinks the
     search vs the no-cache baseline (4 pops vs 9, 5 pushes
     vs 13).

   - test_counters_bounded — single best bound node = (1,0) at
     h=6. h_base((1,0))=4, h*((1,0))=6; bound at h*=6 is the
     tightest admissible value but is NOT 'perfect' in the
     HCached sense — HBounded never sets is_perfect, so no
     early-exit fires. Raises f((1,0)) from 5 to 7, pruning
     (1,0) from the pop set entirely. Saves 1 pop and 1
     expansion vs no-bound baseline.

   - test_counters_bounded_propagated — bound (0,0) at h=7
     (= h*(0,0)) plus pre-search `propagate_pathmax(depth=None)`
     run to convergence. The bound on the start state is a
     no-op by itself (start always pops first regardless of
     f), but propagation lifts the three wall-blind cells to
     their h* values: wave 0 lifts (0,1)→6, (1,0)→6; wave 1
     lifts (1,1)→5; wave 2 finds no tightenings and exits.
     The strictly tighter h on those three cells prunes one
     pop / one expansion vs the bound-only run (8 vs 9 pops;
     7 vs 8 expansions). This is the only single-seed bound
     on the canonical where pre-search propagation strictly
     improves the search — see the rationale in the test
     docstring. Pins the propagate counter group surviving
     `_init_search`'s reset (via AStarLookup's
     `_PRESEARCH_COUNTER_NAMES` hook on AlgoSPP).

 The four pins together drive the param-sensitivity table in
 `COUNTERS.html`. BPMX-side counters (`cnt_bpmx_*`) live on
 `AStarBPMX` (`i_3_astar_bpmx/`).
============================================================================
"""

from f_ds.grids.cell.i_1_map import CellMap

from f_hs.algo.i_0_oospp.i_2_astar_lookup import AStarLookup
from f_hs.heuristic.i_0_base._cache_entry import CacheEntry
from f_hs.problem.i_1_grid import ProblemGrid
from f_hs.state.i_1_cell.main import StateCell


def test_counters_baseline() -> None:
    """
    ========================================================================
     Canonical OOSPP, no cache, no bounds — AStarLookup
     degenerates to plain AStar over Manhattan h. Pins the
     comparison anchor: 13 pushes / 9 pops / 8 expansions /
     13 generated. The propagate group stays at 0 because
     `propagate_pathmax()` is never called.
    ========================================================================
    """
    problem = ProblemGrid.Factory.grid_4x4_obstacle()
    goal = problem.goal
    algo = AStarLookup(
        problem=problem,
        h=lambda s: float(s.distance(goal)),
    )
    sol = algo.run()
    assert sol.cost == 7
    assert algo.search_state.goal_reached is not None
    assert algo.search_state.cache_hit is None
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


def test_counters_cached() -> None:
    """
    ========================================================================
     Canonical OOSPP + single best cache node = (1,1) at
     h_perfect=5 (true h*; h_base = Manhattan = 3). (1,1) is
     the convergence point of the column-0 and column-1 routes;
     once popped, cache-hit early-term fires (cost = 2 + 5 = 7)
     and cache_rank=0 ensures (1,1) pops first within the f=7
     group. Significantly informs: 4 pops / 5 pushes / 3
     expansions vs the canonical no-cache baseline of 9 / 13 /
     8.
    ========================================================================
    """
    problem = ProblemGrid.Factory.grid_4x4_obstacle()
    goal = problem.goal
    s11 = StateCell(key=CellMap(row=1, col=1))
    cache = {s11: CacheEntry(h_perfect=5, suffix_next=None)}
    algo = AStarLookup(
        problem=problem,
        h=lambda s: float(s.distance(goal)),
        cache=cache,
        goal=goal,
    )
    sol = algo.run()
    assert sol.cost == 7
    assert algo.search_state.cache_hit is not None
    assert algo.search_state.cache_hit.rc == (1, 1)
    counters = {k: v for k, v in algo.counters.items()
                if not k.startswith('mem_')}
    assert counters == {
        'cnt_prop_waves': 0,
        'cnt_prop_attempts': 0,
        'cnt_prop_lifts': 0,
        'cnt_push': 5,
        'cnt_pop': 4,
        'cnt_decrease': 0,
        'cnt_expanded': 3,
        'cnt_generated': 5,
    }


def test_counters_bounded() -> None:
    """
    ========================================================================
     Canonical OOSPP + single best bound node = (1,0) at h=6.
     h_base((1,0)) = 4 (Manhattan), h*((1,0)) = 6 (the wall
     forces a row-2 detour). Bound at h*=6 is the tightest
     admissible bound — but NOT 'perfect' in the HCached sense:
     HBounded never sets is_perfect=True, so no early-exit
     fires and the search runs to goal-pop. The bound raises
     f((1,0)) from 5 to 7, pruning (1,0) from the pop set
     entirely. Significantly informs: 8 pops / 7 expansions vs
     the canonical no-bound baseline of 9 / 8.
    ========================================================================
    """
    problem = ProblemGrid.Factory.grid_4x4_obstacle()
    goal = problem.goal
    s10 = StateCell(key=CellMap(row=1, col=0))
    bounds = {s10: 6}
    algo = AStarLookup(
        problem=problem,
        h=lambda s: float(s.distance(goal)),
        bounds=bounds,
    )
    sol = algo.run()
    assert sol.cost == 7
    assert algo.search_state.goal_reached is not None
    assert algo.search_state.cache_hit is None
    counters = {k: v for k, v in algo.counters.items()
                if not k.startswith('mem_')}
    assert counters == {
        'cnt_prop_waves': 0,
        'cnt_prop_attempts': 0,
        'cnt_prop_lifts': 0,
        'cnt_push': 13,
        'cnt_pop': 8,
        'cnt_decrease': 0,
        'cnt_expanded': 7,
        'cnt_generated': 13,
    }


def test_counters_bounded_propagated() -> None:
    """
    ========================================================================
     Canonical OOSPP + bound (0,0) at h=7 (= h*(0,0)) + pre-
     search `propagate_pathmax(depth=None)` (run to
     convergence). The bound on the start state is a no-op
     by itself — A* always pops the start first regardless
     of its f. But propagation walks the bound outward in
     waves and lifts the wall-blind cells:

       wave 0  source (0,0)=7
                 (0,1) ← max(2, 7-1)=6   tightens (gap +4)
                 (1,0) ← max(4, 7-1)=6   tightens (gap +2)
       wave 1  sources {(0,1)=6, (1,0)=6}
                 (1,1) ← max(3, 6-1)=5   tightens (gap +2)
                 (other attempts: no tighten)
       wave 2  source {(1,1)=5}
                 (no tighten — exit signal)

     After convergence the heuristic equals h* on every
     wall-blind cell. The search now sees those cells at
     f=7 instead of the misleading f=3 / f=5 they had under
     plain Manhattan, and three of them never get popped.

     Why depth=None: the convergence default is grid-
     agnostic. depth=2 would also suffice (the wave-2 exit
     fires zero tightenings) but couples the test to the
     topology; the convergence semantics are the documented
     contract, so the test exercises that.

     Why (0,0) is the unique seed: every gap-positive cell on
     this grid lies in rows 0-1, cols 0-1; (0,0) is the only
     cell upstream of all of them. Other seed bounds
     ((1,1)=5, (1,0)=6, (0,1)=6) propagate, but none lifts
     (0,1) all the way to h*=6 — without a tight bound on
     (0,1), the cheap-Manhattan f=3 still dominates the
     pop order.

     Counter narrative:
       - propagate group: 3 waves / 7 attempts / 3 lifts.
         Survives `_init_search`'s reset via the
         `_PRESEARCH_COUNTER_NAMES` hook on AStarLookup,
         mirroring the recorder's retention of pre-search
         `propagate` / `propagate_wave` events.
       - search side: 8 pops / 7 expansions / 13 pushes vs
         9 / 8 / 13 baseline. Strict 1-pop / 1-expand
         improvement, attributable entirely to the
         propagated lifts (the bound itself is a no-op).
    ========================================================================
    """
    problem = ProblemGrid.Factory.grid_4x4_obstacle()
    goal = problem.goal
    s00 = StateCell(key=CellMap(row=0, col=0))
    bounds = {s00: 7}
    algo = AStarLookup(
        problem=problem,
        h=lambda s: float(s.distance(goal)),
        bounds=bounds,
    )

    # Pre-search pathmax — depth=None runs to convergence.
    updates = algo.propagate_pathmax()
    assert {s.rc: int(v) for s, v in updates.items()} == {
        (0, 1): 6,
        (1, 0): 6,
        (1, 1): 5,
    }

    sol = algo.run()
    assert sol.cost == 7
    assert algo.search_state.goal_reached is not None
    assert algo.search_state.cache_hit is None

    # Post-run: propagate group preserved by
    # `_PRESEARCH_COUNTER_NAMES`; search-side counters
    # reflect the lifted-h benefit.
    counters = {k: v for k, v in algo.counters.items()
                if not k.startswith('mem_')}
    assert counters == {
        'cnt_prop_waves': 3,
        'cnt_prop_attempts': 7,
        'cnt_prop_lifts': 3,
        'cnt_push': 13,
        'cnt_pop': 8,
        'cnt_decrease': 0,
        'cnt_expanded': 7,
        'cnt_generated': 13,
    }
