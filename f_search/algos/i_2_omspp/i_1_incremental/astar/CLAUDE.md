# AStarIncremental - Incremental kA* Algorithm

## Purpose
Implements the Incremental kA* algorithm for OMSPP. Decomposes OMSPP into k SPP sub-problems and solves them sequentially using a shared, reusable A* data structure. Frontier states are re-heuristicized between sub-problems. Based on Stern et al., "Heuristic Search for One-to-Many Shortest Path Queries."

## Public API

### `__init__(self, problem: ProblemOMSPP, data: Data[State] = None, heuristics: HeuristicsProtocol[State] = None, name: str = 'AStarIncremental', need_path: bool = False, is_analytics: bool = False) -> None`
Initialize with an OMSPP problem. Optionally provide custom data structure or heuristics. Defaults to `DataHeuristics` with `FrontierPriority` and Manhattan distance heuristic.

### `run() -> SolutionOMSPP`
Execute the algorithm and return solution with paths to all goals.

### Inherited from `AlgoOMSPP`:
- `closed_categories() -> dict[str, list]` — OMSPP node categories (Surely/Borderline/Surplus)

### Inherited from `AlgoSearch`:
- `name -> str`
- `problem -> ProblemOMSPP`

## Inheritance (Hierarchy)

```
AlgoSearch
  └── AlgoOMSPP[State, Data]
        └── AStarIncremental[State]
```

| Base | Responsibility |
|------|----------------|
| `AlgoSearch` | Lifecycle, stats |
| `AlgoOMSPP` | Goals tracking, sub-solutions, analytics |
| `AStarIncremental` | Sequential sub-searches with shared data, frontier re-heuristicization |

## Dependencies

| Import | Used For |
|--------|----------|
| `AStarReusable` | Reusable A* solver for each sub-problem |
| `DataHeuristics` | Shared data structure (g, h, frontier, explored) |
| `FrontierPriority` | Priority queue (OPEN list) |
| `PriorityGH` | f = g + h ordering |
| `HeuristicsManhattan` | Default heuristic |
| `ProblemOMSPP` / `ProblemSPP` | Problem definitions |
| `SolutionOMSPP` / `SolutionSPP` | Solution containers |

## Usage Example

```python
from f_search.algos.i_2_omspp.i_1_incremental.astar import AStarIncremental

# Via Factory
algo = AStarIncremental.Factory.without_obstacles()
solution = algo.run()

# Node-categories problem (asymmetric detours)
algo = AStarIncremental.Factory.for_node_categories()
solution = algo.run()

# Custom problem
algo = AStarIncremental(problem=problem, need_path=True)
solution = algo.run()
```
