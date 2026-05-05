# f_hs/algo/i_1_omspp — One-to-Many SPP algorithms

## Purpose

Algorithms for the One-to-Many Shortest Path Problem (OMSPP):
find `k` shortest paths from a shared start `s` to each of
`k` goal states `[t₁, ..., tₖ]`.

This sub-scope is a **sibling** of the SPP algorithms
(`i_1_astar/`, `i_2_astar_lookup/`, etc.) under `f_hs/algo/`.
It doesn't extend `AlgoSPP` directly — OMSPP algorithms here
orchestrate multiple SPP sub-searches, reusing AStar /
AStarLookup via composition. Both concrete OMSPP algorithms
inherit from a shared base (`AlgoOMSPP`) which itself extends
`f_cs.algo.Algo`, providing the standard lifecycle (`run()`,
`elapsed`, `recorder`, `name`, `problem`) plus a unified
8-counter scaffold for cross-algorithm benchmark comparison.

## Module Structure

```
omspp/
├── __init__.py             Lazy aggregator
├── _single_goal_view.py    ProblemSPP wrapper (one goal at a time)
│                           — shared by INC/BFS/Dijkstra orchestrators
├── i_0_base/               AlgoOMSPP — abstract base (Algo lifecycle
│                             + 8-counter scaffold + SolutionOMSPP)
├── i_1_kastar_inc/         KAStarInc — Incremental kA*
├── i_1_kastar_agg/         KAStarAgg — Aggregative kA*
│   └── _aggregations.py    AGG-only Φ resolver (MIN/MAX/AVG/...)
├── i_1_kbfs/               KBFS — Incremental k-BFS (no h, FIFO)
└── i_2_kdijkstra/          KDijkstra — Incremental k-Dijkstra
                              (KAStarInc with h≡0, inner=Dijkstra)
```

## Package Exports

```python
from f_hs.algo.i_1_omspp import (
    KAStarInc, KAStarAgg, KBFS, KDijkstra,
)
# also re-exported as:
from f_hs import KAStarInc          # convenience
from f_hs.algo import KAStarInc
```

## Test Helpers

Recording-test normalization is shared framework-wide via
`f_hs.algo.u_event_normalize.normalize(event)` — drops
`duration` and unwraps any `StateBase`-typed value through
`state.event_key()` (recursively for tuples / lists). The
polymorphism that used to live in a per-package `_utils.py`
(unwrapping `CellMap → (row, col)` for grid states,
pass-through for graph states) is now a method on `StateBase`
itself: `StateBase.event_key()` (default: `self.key`),
overridden on `StateCell` to return the `(row, col)` tuple.

## Design Principles

1. **Composition over `AlgoSPP`, inheritance from `Algo`.**
   OMSPP orchestrators use AStar instances internally — they
   don't extend `AlgoSPP`. They DO inherit from a shared
   `AlgoOMSPP` base in `i_0_base/`, which itself extends
   `f_cs.algo.Algo[ProblemSPP, SolutionOMSPP]`. This brings
   the standard lifecycle (`run` / `_run_pre` / `_run` /
   `_run_post`), `elapsed` wall-clock, and `recorder`
   plumbing for free, eliminating ~25 lines of boilerplate
   per algorithm.
2. **Shared SearchStateSPP** passed between sub-searches.
   The bundle (OPEN, CLOSED, g, parent) survives from one
   sub-search to the next — the core kA*_inc insight.
3. **Recorder sharing.** One Recorder per orchestrator;
   internal AStar instances have their `_recorder` attribute
   reassigned after construction to point at the shared
   Recorder.
4. **Meta-events** (`on_goal`, `update_frontier`,
   `update_heuristic`) document the orchestration phase,
   distinct from AStar's per-node events.
5. **Per-class counter scaffolds via `_COUNTER_NAMES`
   override.** Each algorithm declares its own counter set —
   only what it actually tracks. The base `AlgoOMSPP` holds
   the minimal scaffold (`cnt_push` / `cnt_pop` /
   `cnt_decrease` + `mem_open` / `mem_closed`); subclasses
   override `_COUNTER_NAMES` with their full schema:
     - **KBFS / KDijkstra** — base scaffold only (no h, no Φ,
       no lazy stale-pop).
     - **KAStarInc** — adds `cnt_h_search`, `cnt_h_update`.
     - **KAStarAgg** — adds `cnt_h_search`, `cnt_h_update`,
       `cnt_phi_search`, `cnt_phi_update`, `cnt_pop_stale`.
   No structural zeros for unsupported mechanisms; every
   counter on `algo.counters` corresponds to actual work the
   algorithm performs. Cross-algo benchmark tables union
   counter sets when needed
   (`pd.DataFrame(rows).fillna(0)`).
   The `Counters` instance is a Mapping, so callers that did
   `algo.counters[name]` or `name in algo.counters` keep
   working — they just see a smaller, honest key set per
   algorithm.
   **Heap-op counters** (`cnt_push` / `cnt_pop` /
   `cnt_decrease`) are owned by `FrontierPriority` (single
   source of truth), not duplicated on the algos.
   `AlgoOMSPP._run_post` calls a `_sync_frontier_counters`
   hook on each subclass that mirrors the frontier's tally
   into the algo's scaffold via `Counters.assign`.
6. **`SolutionOMSPP` Mapping return.** `run()` returns a
   `SolutionOMSPP` (a `Mapping[State, SolutionSPP]` plus
   `SolutionAlgo` validity), not a plain dict. Indexing,
   iteration, and `.items()` work transparently for clients
   that expect a dict view; `.is_valid` / `.is_all_reached`
   / `.costs` provide the f_cs-aligned solution surface.
7. **Within/between time bucketing.** `AlgoOMSPP` exposes
   `elapsed_search` and `elapsed_update` (in addition to total
   `elapsed`), driven by a structural `phase` property setter
   on the base. Semantics are **structural**, not work-typed:
   `elapsed_update` measures wall-clock spent in *explicit
   between-sub-search blocks*, not all refresh-typed work.
   Consequently **AGG-lazy reports `elapsed_update == 0.0`** —
   its refresh work happens inline at pop time and is
   structurally part of search. Counters (`cnt_h_update`
   etc.) still tag the work type, so the two metrics tell
   complementary stories. The base accepts `is_timing=True`
   (default; ~150 ns per phase flip) or `is_timing=False`
   (plain field write only) for distortion-free benchmarks
   at large k. AGG-lazy has zero phase flips at any k by
   design — its overhead is always zero.

## Algorithm matrix

| Name | Status | Notes |
|---|---|---|
| `KAStarInc` | shipped | Incremental kA* (consistent h required) |
| `KAStarAgg` | shipped | Aggregative kA* (MIN/MAX/AVG/RND/PROJECTION) |
| `KBFS` | shipped | k-BFS — single-pass multi-goal BFS for uniform-weight graphs (own frame, sibling of KAStarInc) |
| `KDijkstra` | shipped | k-Dijkstra — single-pass multi-goal Dijkstra for non-negative weights (own frame, sibling of KAStarInc) |

## Dependencies

- `f_cs.algo.Algo` (lifecycle parent of `AlgoOMSPP`)
- `f_core.counters.Counters` (8-counter scaffold; also owns
  the frontier's 3 heap-op counters)
- `f_hs.algo.i_1_astar.AStar` (used by orchestrators; exposes
  `algo.counters` as a delegation property to its frontier)
- `f_hs.frontier.i_1_priority.FrontierPriority` (owns
  `cnt_push` / `cnt_pop` / `cnt_decrease`; mirrored into the
  8-counter scaffold at end-of-run)
- `f_hs.algo.i_0_base.SearchStateSPP` (shared bundle)
- `f_hs.problem.i_0_base.ProblemSPP` (problem with multiple goals)
- `f_hs.solution.SolutionOMSPP` (per-goal solution wrapper)
