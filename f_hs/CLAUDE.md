# f_hs — Heuristic Search Framework

## Purpose
Framework for heuristic search algorithms on various domains
(grids, puzzles, graphs, planning). Built on top of f_cs
(Problem → Algorithm → Solution).

## Package Exports
```python
from f_hs import StateBase, StateCell
from f_hs import ProblemSPP, ProblemGrid
from f_hs import SolutionSPP
from f_hs import AlgoSPP, BFS, AStar, AStarLookup, Dijkstra
from f_hs import HBase, HCallable, HCached, HBounded, CacheEntry
from f_hs.frontier import (
    FrontierBase, FrontierFIFO, FrontierPriority,
)
```

Most users only need `AStar` — the advanced `AStarLookup` class is
reached transparently via `AStar.__new__` dispatch whenever the
caller supplies HCached / HBounded / search_state. Import
`AStarLookup` directly only when you need explicit typing for IDE
autocomplete of Pro-only methods (`to_cache`, `propagate_pathmax`).

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
                                    └── Dijkstra   (h = 0)
SolutionAlgo         ←──    SolutionSPP (cost)

                            StateBase[Key]
                              └── StateCell (Key=CellMap)

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
│   ├── i_0_base/         StateBase[Key] — generic base
│   └── i_1_cell/         StateCell — CellMap for 2D grids
├── problem/
│   ├── i_0_base/         ProblemSPP — abstract SPP base
│   └── i_1_grid/         ProblemGrid — 2D grid domain
├── solution/             SolutionSPP — cost + validity
├── frontier/
│   ├── i_0_base/         FrontierBase — abstract
│   ├── i_1_fifo/         FrontierFIFO — BFS frontier
│   └── i_1_priority/     FrontierPriority — A*/Dijkstra frontier
├── algo/
│   ├── i_0_base/         AlgoSPP — abstract search loop
│   ├── i_1_bfs/          BFS — breadth-first search
│   ├── i_1_astar/        AStar — simple A* + __new__ dispatcher
│   ├── i_2_astar_lookup/    AStarLookup — advanced (HCached, HBounded,
│   │                       search_state, pathmax, to_cache)
│   └── i_2_dijkstra/     Dijkstra — A* with h=0
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
