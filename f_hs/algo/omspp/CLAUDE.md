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
5. **Unified 8-counter scaffold** on `AlgoOMSPP` enables a
   uniform benchmark table across `KAStarAgg` / `KAStarInc`.
   Each algorithm increments whichever subset it supports;
   unsupported counters stay at 0 with a documented reason
   (see `i_0_base/CLAUDE.md` for the per-algorithm support
   matrix).
6. **`SolutionOMSPP` Mapping return.** `run()` returns a
   `SolutionOMSPP` (a `Mapping[State, SolutionSPP]` plus
   `SolutionAlgo` validity), not a plain dict. Indexing,
   iteration, and `.items()` work transparently for clients
   that expect a dict view; `.is_valid` / `.is_all_reached`
   / `.costs` provide the f_cs-aligned solution surface.

## Future contents (Phase 4+)

| Name | Status | Notes |
|---|---|---|
| `KAStarInc` | shipped | Incremental kA* |
| `KAStarAgg` | shipped | Aggregative kA* (MIN/MAX/AVG/RND/PROJECTION) |
| `KDijkstra` | planned | k-Dijkstra (no heuristic, Φ=0) fallback |

## Dependencies

- `f_cs.algo.Algo` (lifecycle parent of `AlgoOMSPP`)
- `f_hs.algo.i_1_astar.AStar` (used by orchestrators)
- `f_hs.algo.i_0_base.SearchStateSPP` (shared bundle)
- `f_hs.problem.i_0_base.ProblemSPP` (problem with multiple goals)
- `f_hs.solution.SolutionOMSPP` (per-goal solution wrapper)
