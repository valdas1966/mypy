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
from f_hs import AlgoSPP, BFS, AStar, Dijkstra
from f_hs.frontier import (
    FrontierBase, FrontierFIFO, FrontierPriority,
)
```

## Architecture
```
f_cs (generic)              f_hs (search-specific)
─────────────               ──────────────────────
ProblemAlgo          ←──    ProblemSPP[State]
                              └── ProblemGrid
Algo[Problem, Sol]   ←──    AlgoSPP[State]         (holds a Frontier)
                              ├── BFS              (FrontierFIFO)
                              └── AStar → Dijkstra (FrontierPriority)
SolutionAlgo         ←──    SolutionSPP (cost)

                            StateBase[Key]
                              └── StateCell (Key=CellMap)

                            FrontierBase[State]
                              ├── FrontierFIFO
                              └── FrontierPriority
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
└── algo/
    ├── i_0_base/         AlgoSPP — abstract search loop
    ├── i_1_bfs/          BFS — breadth-first search
    ├── i_1_astar/        AStar — A* with heuristic
    └── i_2_dijkstra/     Dijkstra — A* with h=0
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
- **Dijkstra extends AStar** — Dijkstra is A* with h=0.
- **i_X_ convention** — inheritance depth encoded in folder names.
- **StateCell caches in ProblemGrid** — one StateCell per
  valid cell, no object creation during search.
