# f_hs — Heuristic Search Framework

## Purpose
Framework for heuristic search algorithms on various domains
(grids, puzzles, graphs, planning). Built on top of f_cs
(Problem → Algorithm → Solution).

## Package Exports
```python
from f_hs import StateBase, ProblemSPP
```

## Architecture
```
f_cs (generic)              f_hs (search-specific)
─────────────               ──────────────────────
ProblemAlgo          ←──    ProblemSPP[State]
Algo[Problem, Sol]          (future: AlgoSearch)
SolutionAlgo                (future: SolutionSearch)

StateBase[Key]              — search-space configuration
```

## Module Structure
```
f_hs/
├── __init__.py        StateBase, ProblemSPP
├── state/             StateBase — search-space configuration
└── problem/           ProblemSPP — shortest path problem (OO/OM/MO/MM)
```
