# DataHeuristicsVector - Vector-based Heuristic Data Structure

## Purpose
Stores per-state heuristic vectors (one h-value per goal) for OMSPP algorithms. Unlike `DataHeuristics` which stores a single scalar h per state, this stores `list[int]` of size k (number of goals). The aggregated scalar h is computed on-the-fly via a Phi function.

## Public API

### `__init__(self, frontier: FrontierPriority[State, PriorityGH], explored: set[StateBase] = None, dict_parent: dict[State, State] = None, dict_g: dict[State, int] = None, dict_h: dict[State, list[int]] = None) -> None`
Initialize with frontier and optional pre-populated dicts. `dict_h` maps each state to a vector of heuristic values (one per goal).

### `dict_h: dict[State, list[int]]`
Maps each state to its heuristic vector. Vector is size k (total goals), computed once at state discovery, and never modified.

### `data_state(self, state: State, h_agg: int = None) -> dict[str, any]`
Return a dict of state data. Includes `h_vec` (the full vector), `h` (aggregated scalar, passed in), `g`, and `f = g + h`.

### Inherited from `DataBestFirst`:
- `frontier`, `explored`, `dict_g`, `dict_parent`, `best`
- `set_best_to_be_parent_of(state) -> None`
- `path_to(state) -> Path`
- `list_explored() -> list[dict]`

## Inheritance (Hierarchy)

```
HasDataState[State]
  └── DataBestFirst[State]  (frontier, explored, dict_g, dict_parent)
        └── DataHeuristicsVector[State]  (dict_h: list[int] per state)
```

| Base | Responsibility |
|------|----------------|
| `HasDataState` | `data_state()` protocol |
| `DataBestFirst` | Frontier, explored set, g-values, parent pointers, path reconstruction |
| `DataHeuristicsVector` | Vector h-values per state |

## Dependencies

| Import | Used For |
|--------|----------|
| `DataBestFirst` | Base class |
| `FrontierPriority` | Priority queue type for frontier |
| `PriorityGH` | Priority type parameter |
| `StateBase` | State type bound |

## Usage Example

```python
from f_search.ds.data import DataHeuristicsVector as Data
from f_search.ds.frontier import FrontierPriority as Frontier
from f_search.ds.priority import PriorityGH as Priority

frontier = Frontier[State, Priority]()
data = Data(frontier=frontier)

# Store vector h for a state (one h per goal)
data.dict_h[state] = [3, 5, 7]  # distances to 3 goals

# Aggregate via Phi when computing priority
h_agg = min(data.dict_h[state][i] for i in active_indices)
```
