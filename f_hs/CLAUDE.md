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
```

## Architecture
```
f_cs (generic)              f_hs (search-specific)
─────────────               ──────────────────────
ProblemAlgo          ←──    ProblemSPP[State]
                              └── ProblemGrid
Algo[Problem, Sol]   ←──    AlgoSPP[State]
                              ├── BFS
                              └── AStar → Dijkstra
SolutionAlgo         ←──    SolutionSPP (cost)

                            StateBase[Key]
                              └── StateCell (Key=CellMap)
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
└── algo/
    ├── i_0_base/         AlgoSPP — abstract search loop
    ├── i_1_bfs/          BFS — breadth-first search
    ├── i_1_astar/        AStar — A* with heuristic
    └── i_2_dijkstra/     Dijkstra — A* with h=0
```

## Design Decisions
- **Solution holds cost only** — path reconstruction via
  `algo.reconstruct_path()`.
- **No Frontier/Data classes** — plain Python structures.
- **Dijkstra extends AStar** — Dijkstra is A* with h=0.
- **i_X_ convention** — inheritance depth encoded in folder names.
- **StateCell caches in ProblemGrid** — one StateCell per
  valid cell, no object creation during search.
