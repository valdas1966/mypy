# f_hs/algo/omspp — One-to-Many SPP algorithms

## Purpose

Algorithms for the One-to-Many Shortest Path Problem (OMSPP):
find `k` shortest paths from a shared start `s` to each of
`k` goal states `[t₁, ..., tₖ]`.

This sub-scope is a **sibling** of the SPP algorithms
(`i_1_astar/`, `i_2_astar_lookup/`, etc.) under `f_hs/algo/`.
It doesn't extend `AlgoSPP` directly — OMSPP algorithms here
orchestrate multiple SPP sub-searches, reusing AStar / AStarLookup
via composition.

## Module Structure

```
omspp/
├── __init__.py          Lazy aggregator
├── _internal/
│   └── _single_goal_view.py   ProblemSPP wrapper (one goal at a time)
└── i_1_kastar_inc/      KAStarInc — Incremental kA*
```

## Package Exports

```python
from f_hs.algo.omspp import KAStarInc
# also re-exported as:
from f_hs import KAStarInc          # convenience
from f_hs.algo import KAStarInc
```

## Design Principles

1. **Composition over inheritance.** OMSPP orchestrators use
   AStar instances internally. They don't extend `AlgoSPP`.
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

## Future contents (Phase 4+)

| Name | Status | Notes |
|---|---|---|
| `KAStarInc` | shipped | Incremental kA* (this module) |
| `KAStarMin` | planned | Single-search kA* with Φ=min aggregation |
| `KAStarLazy` | planned | Lazy kA* — defer F-recomputation |
| `KDijkstra` | planned | k-Dijkstra (no heuristic, Φ=0) fallback |

## Dependencies

- `f_hs.algo.i_1_astar.AStar` (used by orchestrators)
- `f_hs.algo.i_0_base.SearchStateSPP` (shared bundle)
- `f_hs.problem.i_0_base.ProblemSPP` (problem with multiple goals)
