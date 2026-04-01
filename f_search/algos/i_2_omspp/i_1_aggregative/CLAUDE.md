# AStarAggregative - Eager kA* Algorithm

## Purpose
Implements the Eager kA* algorithm for OMSPP (One-to-Many Shortest Path Problem). Performs a single unified search toward all k goals using a heuristic aggregation function (Phi) to combine per-goal heuristic values. When a goal is found, eagerly recomputes F values for all frontier states. Based on Stern et al., "Heuristic Search for One-to-Many Shortest Path Queries."

## Public API

### `__init__(self, problem: ProblemOMSPP, phi: PhiFunc = UPhi.min, name: str = 'AStarAggregative', need_path: bool = False, is_analytics: bool = False) -> None`
Initialize with an OMSPP problem and an aggregation function. Default Phi is min (admissible with consistent heuristics).

### `run() -> SolutionOMSPP`
Execute the algorithm and return solution with paths to all goals.

### Inherited from `AlgoSearch`:
- `name -> str`
- `problem -> ProblemOMSPP`

## Key Design: Vector Heuristics

Each state stores a heuristic vector `h_vec` of size k (one h per goal), computed once at discovery time. The aggregated scalar h is recomputed from the vector via Phi whenever needed:
- `F(n) = g(n) + Phi(h_vec(n), active_indices)`

When a goal is found:
1. Goal removed from `_goals_active` and `_active_indices`
2. `_update_h()` re-aggregates all frontier states from stored vectors (no distance recomputation)

## Inheritance (Hierarchy)

```
AlgoSearch
  └── AlgoBestFirst[ProblemOMSPP, SolutionOMSPP, State, Data]
        └── AlgoOMSPP[State, Data]
              └── AStarAggregative[State]
```

| Base | Responsibility |
|------|----------------|
| `AlgoSearch` | Lifecycle, stats |
| `AlgoBestFirst` | Frontier pop, explore, successor filtering |
| `AlgoOMSPP` | Goals tracking, sub-solutions, analytics |
| `AStarAggregative` | Vector heuristics, Phi aggregation, eager F updates |

## Dependencies

| Import | Used For |
|--------|----------|
| `DataHeuristicsVector` | Stores h vectors per state |
| `UPhi` / `PhiFunc` | Aggregation function (min, max, mean) |
| `FrontierPriority` | Priority queue (OPEN list) |
| `PriorityGH` | f = g + h ordering |
| `ProblemOMSPP` | Problem definition |
| `SolutionOMSPP` / `SolutionSPP` | Solution containers |

## Usage Example

```python
from f_search.algos.i_2_omspp.i_1_aggregative import AStarAggregative
from f_search.heuristics.phi import UPhi

# Default (min aggregation)
algo = AStarAggregative.Factory.without_obstacles()
solution = algo.run()

# With max aggregation
algo = AStarAggregative.Factory.without_obstacles(phi=UPhi.max)
solution = algo.run()

# Custom problem
algo = AStarAggregative(problem=problem, phi=UPhi.mean)
solution = algo.run()

# Node-categories problem (asymmetric detours)
algo = AStarAggregative.Factory.for_node_categories()
solution = algo.run()
```
