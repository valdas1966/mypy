# f_hs — Heuristic Search Framework

## Purpose
Framework for heuristic search algorithms on various domains
(grids, puzzles, graphs, planning). Built on top of f_cs
(Problem → Algorithm → Solution).

## Package Exports
```python
from f_hs import StateBase, StateCell, StateResource, NodeResource
from f_hs import ProblemSPP, ProblemGrid
from f_hs import SolutionSPP
from f_hs import AlgoSPP, BFS, AStar, AStarLookup, AStarBPMX, Dijkstra
from f_hs import HBase, HCallable, HCached, HBounded, CacheEntry
from f_hs.frontier import (
    FrontierBase, FrontierFIFO, FrontierPriority,
)
```

Three A* tiers, picked explicitly by the caller:
- `AStar` — simple, hot path; raw callable / HBase only.
  Rejects HCached / HBounded with a redirect TypeError.
- `AStarLookup` — adds `cache=` / `bounds=` kwargs,
  `propagate_pathmax`, `to_cache`, suffix-stitching.
- `AStarBPMX` — extends `AStarLookup` with in-search BPMX
  (`rule_bpmx=` / `depth_bpmx=` kwargs).

## Architecture
```
f_cs (generic)              f_hs (search-specific)
─────────────               ──────────────────────
ProblemAlgo          ←──    ProblemSPP[State]
                              └── ProblemGrid
Algo[Problem, Sol]   ←──    AlgoSPP[State]         (holds a SearchState)
                              ├── BFS              (FrontierFIFO)
                              └── AStar            (FrontierPriority)
                                    ├── AStarLookup   (HCached + HBounded + pathmax)
                                    │     └── AStarBPMX (+ in-search BPMX cascade)
                                    └── Dijkstra   (h = 0)
SolutionAlgo         ←──    SolutionSPP (cost)

                            StateBase[Key]   (the only State class)
                              StateCell     = StateBase[CellMap]  (alias)
                              StateResource = StateBase[
                                                NodeResource[Node]] (alias)
                                    (V×R state for RCSPP; NodeResource
                                     = (node, resource) Tupleable key class)

                            FrontierBase[State]
                              ├── FrontierFIFO
                              └── FrontierPriority

                            HBase[State]           (heuristic source)
                              ├── HCallable        (wraps a function)
                              ├── HCached          (frozen dict + goal;
                              │                     drives cache_hit
                              │                     early termination)
                              └── HBounded         (frozen admissible
                                                    lower bounds;
                                                    max-combines with
                                                    base)
```

## Module Structure
```
f_hs/
├── __init__.py           All public exports
├── state/
│   ├── i_0_base/         StateBase[Key] — the only State class
│   ├── i_1_cell/         StateCell = StateBase[CellMap]  (alias)
│   └── i_1_resource/     StateResource = StateBase[NodeResource]  (alias)
│                         (+ NodeResource (node, resource) key class)
├── problem/
│   ├── i_0_base/         ProblemSPP — abstract SPP base
│   └── i_1_grid/         ProblemGrid — 2D grid domain
├── solution/             SolutionSPP — cost + validity
├── frontier/
│   ├── i_0_base/         FrontierBase — abstract
│   ├── i_1_fifo/         FrontierFIFO — BFS frontier
│   └── i_1_priority/     FrontierPriority — A*/Dijkstra frontier
├── algo/
│   ├── i_0_base/            AlgoSPP — abstract search loop
│   ├── i_1_bfs/             BFS — breadth-first search
│   ├── i_1_astar/           AStar — simple A*
│   ├── i_2_astar_lookup/    AStarLookup — cache + bounds + pathmax + to_cache
│   ├── i_2_dijkstra/        Dijkstra — A* with h=0
│   └── i_3_astar_bpmx/      AStarBPMX — AStarLookup + in-search BPMX
└── heuristic/
    ├── i_0_base/         HBase + CacheEntry
    ├── i_1_callable/     HCallable — wraps a Callable
    ├── i_1_cached/       HCached — frozen cache + goal
    └── i_1_bounded/      HBounded — frozen admissible bounds
```

## Running Tests
A `_run_tests.py` exists at three levels for scoped runs via
`f_test.TestRunner` (which uses pattern `_tester*.py` by default,
so split files like `_tester_grid.py` are auto-picked-up):
```
python -m f_hs._run_tests           # whole package
python -m f_hs.algo._run_tests      # just algo tests
python -m f_hs.frontier._run_tests  # just frontier tests
```

## Design Decisions
- **Solution holds cost only** — path reconstruction via
  `algo.reconstruct_path()`.
- **Frontier as a first-class class.** `AlgoSPP` composes a
  `FrontierBase` via constructor injection. BFS passes
  `FrontierFIFO`, A* passes `FrontierPriority`. The algo
  computes priority via `_priority(state)` and passes it in;
  the frontier stays priority-agnostic.
- **Heuristic as a first-class class.** AStar accepts
  `HBase | Callable`. Raw callables are auto-wrapped in
  `HCallable`. `HCached` enables O(1) termination on popped
  states whose `h*` is cached (via `AlgoSPP._early_exit` hook),
  with suffix-stitching in `reconstruct_path`. Static-cache
  semantics per 2026-04-20 decisions; harvest via
  `AStar.to_cache()` (works after goal-pop OR cache-hit
  termination, per the OMSPP / MOSPP / MMSPP incremental-reuse
  use case).
- **Dijkstra extends AStar** — Dijkstra is A* with h=0.
- **i_X_ convention** — inheritance depth encoded in folder names.
- **StateCell caches in ProblemGrid** — one StateCell per
  valid cell, no object creation during search.
