# f_hs/algo/omspp — One-to-Many SPP algorithms

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
├── __init__.py          Lazy aggregator
├── _utils.py            Shared test helpers (key_of, normalize)
├── _internal/
│   └── _single_goal_view.py   ProblemSPP wrapper (one goal at a time)
├── i_0_base/            AlgoOMSPP — abstract base (Algo lifecycle
│                          + 8-counter scaffold + SolutionOMSPP)
├── i_1_kastar_inc/      KAStarInc — Incremental kA*
└── i_1_kastar_agg/      KAStarAgg — Aggregative kA*
```

## Package Exports

```python
from f_hs.algo.omspp import KAStarInc, KAStarAgg
# also re-exported as:
from f_hs import KAStarInc          # convenience
from f_hs.algo import KAStarInc
```

## Test Helpers (`_utils.py`)

Private to the package; mirrors `f_hs/algo/i_2_astar_lookup/_utils.py`:

- `key_of(state)` — unwraps `CellMap → (row, col)` for grids;
  pass-through for string-keyed graph states.
- `normalize(event)` — drops `duration`; unwraps `state` and
  `parent` to keys. State-less meta-events
  (`update_frontier`) pass through unchanged. Used by
  recording tests that pin the full event stream as a golden
  reference (e.g., the `grid_4x4_obstacle` tests in Inc and
  Agg testers).

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
5. **Unified 8-counter scaffold** on `AlgoOMSPP`, composed
   via `f_core.counters.Counters`, enables a uniform
   benchmark table across `KAStarAgg` / `KAStarInc`. Each
   algorithm increments whichever subset it supports;
   unsupported counters stay at 0 with a documented reason
   (see `i_0_base/CLAUDE.md` for the per-algorithm support
   matrix). The `Counters` instance is a Mapping, so callers
   that did `algo.counters == {...}` or `algo.counters['cnt_pop']`
   keep working unchanged.
   **Heap-op counters** (`cnt_push` / `cnt_pop` / `cnt_decrease`)
   are owned by `FrontierPriority` (single source of truth),
   not duplicated on the algos. `AlgoOMSPP._run_post` calls a
   `_sync_frontier_counters` hook on each subclass that
   mirrors the frontier's tally into the 8-counter scaffold
   via `Counters.assign`. Both Inc and Agg now expose all
   heap-op counts honestly — no more "deferred" gaps.
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

## Future contents (Phase 4+)

| Name | Status | Notes |
|---|---|---|
| `KAStarInc` | shipped | Incremental kA* |
| `KAStarAgg` | shipped | Aggregative kA* (MIN/MAX/AVG/RND/PROJECTION) |
| `KDijkstra` | planned | k-Dijkstra (no heuristic, Φ=0) fallback |

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
