"""
============================================================================
 AStarLookup — counter pins on the canonical OOSPP problem
 (`grid_4x4_obstacle`: start (0,0), goal (0,3), wall at
 (0,2)/(1,2), Manhattan h, optimal cost 7).

 Seven scenarios pin the lookup-side counter scaffold (12-name:
 propagate 3 + frontier 3 + search 2 + memory 4) along the
 AStarLookup informativity axis:

   - test_counters_baseline — no cache, no bounds. AStarLookup
     reduces to plain AStar over Manhattan h; pins the
     comparison anchor against which `cached` / `bounded` /
     `bounded_propagated_depth_*` deltas read off (9 pops /
     13 pushes / 8 expansions).

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

   - test_counters_bounded_propagated_depth_{0,1,2,3} — bound
     (0,0) at h=7 (= h*(0,0)) plus `propagate_pathmax(depth=N)`
     parametrized in [0,1,2,3]. The bound on the start state
     is a no-op by itself (start always pops first regardless
     of f); propagation is what walks the bound outward and
     lifts the wall-blind cells (0,1)/(1,0)/(1,1) to their h*.
     The four sub-scenarios isolate the wave-by-wave cost /
     benefit:

       depth=0  cap-before-wave-0      0w / 0a / 0l   9 pops
       depth=1  wave 0 only            1w / 2a / 2l   8 pops
       depth=2  waves 0+1              2w / 5a / 3l   8 pops
       depth=3  waves 0+1+2 (≡None)    3w / 7a / 3l   8 pops

     Two informative deltas:
       - depth-0 ↔ depth-1: marginal value of the first wave
         (+1w / +2a / +2l, −1 pop / −1 expansion). The lift
         on (1,0) alone matches the explicit-bound scenario
         at the search side.
       - depth-2 ↔ depth-3: cost of the convergence-detection
         wave (+1w / +2a / 0 extra lifts, search unchanged).

     The propagate group survives `_init_search`'s reset via
     AStarLookup's `_PRESEARCH_COUNTER_NAMES` hook on AlgoSPP;
     depth_0 is the trivial-zero pin, depth_3 the canonical
     positive-signal pin for that retention contract.

     Why (0,0) is the unique seed: of the four gap-positive
     cells on the canonical grid ((0,0), (0,1), (1,0), (1,1)),
     only (0,0) is upstream of all others. Bounding (0,0)=h*=7
     then propagating lifts (0,1)→6, (1,0)→6, (1,1)→5 — all to
     their h*. Other seeds ((1,1)=5, (1,0)=6, (0,1)=6)
     propagate but never lift (0,1) to h*=6, so the cheap-
     Manhattan f=3 still dominates the pop order — same 9 pops
     as baseline.

 The seven pins together drive the param-sensitivity table in
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
        h=lambda s: float(s.key.distance(goal.key)),
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
        h=lambda s: float(s.key.distance(goal.key)),
        cache=cache,
        goal=goal,
    )
    sol = algo.run()
    assert sol.cost == 7
    assert algo.search_state.cache_hit is not None
    assert algo.search_state.cache_hit.to_tuple() == (1, 1)
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
        h=lambda s: float(s.key.distance(goal.key)),
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


def test_counters_bounded_propagated_depth_0() -> None:
    """
    ========================================================================
     Canonical OOSPP + bound (0,0)=7 + `propagate_pathmax(
     depth=0)`.

     Cap-before-wave-0: the loop's `iteration >= depth` guard
     fires immediately on entry (0 >= 0), so no wave runs.
     No `propagate_wave` events, no `propagate` events, no
     lifts; `updates` returns empty. The bound on (0,0) is
     set but is a no-op for the search (start always pops
     first regardless of f).

     Search side: identical to the no-bound, no-propagate
     baseline (9 pops / 13 pushes / 8 expansions). Trivial-
     zero pin for the `_PRESEARCH_COUNTER_NAMES` retention
     contract — the propagate group reads zero post-`run()`,
     and that zero must come from the pre-search call, not
     from `_init_search`'s reset.
    ========================================================================
    """
    problem = ProblemGrid.Factory.grid_4x4_obstacle()
    goal = problem.goal
    s00 = StateCell(key=CellMap(row=0, col=0))
    bounds = {s00: 7}
    algo = AStarLookup(
        problem=problem,
        h=lambda s: float(s.key.distance(goal.key)),
        bounds=bounds,
    )

    # depth=0 — cap fires on the first iteration check; no
    # wave runs.
    updates = algo.propagate_pathmax(depth=0)
    assert updates == {}

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


def test_counters_bounded_propagated_depth_1() -> None:
    """
    ========================================================================
     Canonical OOSPP + bound (0,0)=7 + `propagate_pathmax(
     depth=1)`.

     Wave 0 only: from seed (0,0)=7, the two attempts
     (0,0)→(0,1) and (0,0)→(1,0) both lift (h_base 2/4 →
     cand 6 in each case). 2 attempts / 2 lifts. Cap stops
     before wave 1 — (1,1) is NOT lifted, retains cheap
     Manhattan h=3.

     Search side: the lift on (1,0) alone is enough to
     prune (1,0) from the pop set (f((1,0)) = 1 + 6 = 7
     vs 1 + 4 = 5 baseline) — same effect as the explicit-
     bound scenario in `test_counters_bounded`. 8 pops /
     13 pushes / 7 expansions; strict 1-pop / 1-expand
     improvement vs depth-0.

     Pinned to isolate the marginal value of the first
     wave (depth-0 ↔ depth-1 delta: +1w / +2a / +2l,
     −1 pop / −1 expansion).
    ========================================================================
    """
    problem = ProblemGrid.Factory.grid_4x4_obstacle()
    goal = problem.goal
    s00 = StateCell(key=CellMap(row=0, col=0))
    bounds = {s00: 7}
    algo = AStarLookup(
        problem=problem,
        h=lambda s: float(s.key.distance(goal.key)),
        bounds=bounds,
    )

    # depth=1 — wave 0 only; cap stops before wave 1.
    updates = algo.propagate_pathmax(depth=1)
    assert {s.to_tuple(): int(v) for s, v in updates.items()} == {
        (0, 1): 6,
        (1, 0): 6,
    }

    sol = algo.run()
    assert sol.cost == 7
    assert algo.search_state.goal_reached is not None
    assert algo.search_state.cache_hit is None

    counters = {k: v for k, v in algo.counters.items()
                if not k.startswith('mem_')}
    assert counters == {
        'cnt_prop_waves': 1,
        'cnt_prop_attempts': 2,
        'cnt_prop_lifts': 2,
        'cnt_push': 13,
        'cnt_pop': 8,
        'cnt_decrease': 0,
        'cnt_expanded': 7,
        'cnt_generated': 13,
    }


def test_counters_bounded_propagated_depth_2() -> None:
    """
    ========================================================================
     Canonical OOSPP + bound (0,0)=7 + `propagate_pathmax(
     depth=2)`.

     Waves 0 + 1 run. Wave 0 lifts (0,1)→6 and (1,0)→6
     (2 atts / 2 lifts). Wave 1 from sources {(0,1)=6,
     (1,0)=6} attempts (0,1)→(1,1) [LIFT to 5],
     (1,0)→(1,1) [no-op, already 5], (1,0)→(2,0) [no-op,
     h_base=5 = cand=5] — 3 atts / 1 lift. Cap stops
     before wave 2 — the no-tighten convergence wave never
     fires.

     All three wall-blind cells lifted to h*: (0,1)=6,
     (1,0)=6, (1,1)=5. Search side identical to depth-3
     (8 pops / 13 pushes / 7 expansions).

     Pinned to anchor depth-2; together with depth-3
     isolates the cost of the convergence-detection wave
     (+1w / +2a / 0 extra lifts, search unchanged).
    ========================================================================
    """
    problem = ProblemGrid.Factory.grid_4x4_obstacle()
    goal = problem.goal
    s00 = StateCell(key=CellMap(row=0, col=0))
    bounds = {s00: 7}
    algo = AStarLookup(
        problem=problem,
        h=lambda s: float(s.key.distance(goal.key)),
        bounds=bounds,
    )

    # depth=2 — waves 0 + 1; cap stops before wave 2.
    updates = algo.propagate_pathmax(depth=2)
    assert {s.to_tuple(): int(v) for s, v in updates.items()} == {
        (0, 1): 6,
        (1, 0): 6,
        (1, 1): 5,
    }

    sol = algo.run()
    assert sol.cost == 7
    assert algo.search_state.goal_reached is not None
    assert algo.search_state.cache_hit is None

    counters = {k: v for k, v in algo.counters.items()
                if not k.startswith('mem_')}
    assert counters == {
        'cnt_prop_waves': 2,
        'cnt_prop_attempts': 5,
        'cnt_prop_lifts': 3,
        'cnt_push': 13,
        'cnt_pop': 8,
        'cnt_decrease': 0,
        'cnt_expanded': 7,
        'cnt_generated': 13,
    }


def test_counters_bounded_propagated_depth_3() -> None:
    """
    ========================================================================
     Canonical OOSPP + bound (0,0)=7 + `propagate_pathmax(
     depth=3)`.

     Waves 0 + 1 + 2 run; wave 2 is the no-tighten
     convergence signal (next_sources empties; the loop
     exits via the `while sources` guard at iter=3, NOT via
     the depth cap). For this problem depth=3 ≡ depth=None
     — same lifts, same waves, same counters.

     Wave 2 from source {(1,1)=5} attempts (1,1)→(2,1)
     [no-op, h_base=4 = cand=4] and (1,1)→(1,0) [no-op,
     already 6 > cand=4] — 2 atts / 0 lifts. The (0,1)
     back-edge is skipped (last-tightener of (1,1)).

     Counter narrative:
       - propagate group: 3 waves / 7 attempts / 3 lifts.
         Canonical positive-signal pin for `_PRESEARCH_
         COUNTER_NAMES` retention — survives `_init_search`'s
         reset, mirroring the recorder's retention of pre-
         search `propagate` / `propagate_wave` events.
       - search side: 8 pops / 13 pushes / 7 expansions vs
         9 / 13 / 8 baseline. Strict 1-pop / 1-expand
         improvement, attributable entirely to the
         propagated lifts (the bound itself is a no-op).

     Pinned as the explicit-cap mirror of the convergence
     default; together with depth-2 it isolates the
     convergence wave as a separate observable.
    ========================================================================
    """
    problem = ProblemGrid.Factory.grid_4x4_obstacle()
    goal = problem.goal
    s00 = StateCell(key=CellMap(row=0, col=0))
    bounds = {s00: 7}
    algo = AStarLookup(
        problem=problem,
        h=lambda s: float(s.key.distance(goal.key)),
        bounds=bounds,
    )

    # depth=3 — waves 0 + 1 + 2; loop exits via empty
    # sources (NOT the depth cap) before iter=3.
    updates = algo.propagate_pathmax(depth=3)
    assert {s.to_tuple(): int(v) for s, v in updates.items()} == {
        (0, 1): 6,
        (1, 0): 6,
        (1, 1): 5,
    }

    sol = algo.run()
    assert sol.cost == 7
    assert algo.search_state.goal_reached is not None
    assert algo.search_state.cache_hit is None

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
