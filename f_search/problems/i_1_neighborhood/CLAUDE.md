# ProblemNeighborhood - Neighborhood Search Problem

## Purpose
Defines a grid-based search problem that explores all reachable states within a maximum number of steps from a start state. Composes `ProblemSearch` (grid + successors) with `HasStart` (start state) and adds a `steps_max` constraint.

## Public API

### `__init__(self, grid: Grid, start: State, steps_max: int, name: str = 'ProblemNeighborhood') -> None`
Initialize with a grid, start state, and maximum step count.
- `grid`: `GridMap` - The 2D grid search space.
- `start`: `StateCell` - The initial state.
- `steps_max`: `int` - Maximum number of steps from start.
- Calls `ProblemSearch.__init__` and `HasStart.__init__` explicitly.

### `steps_max -> int` (property)
Returns the maximum number of steps allowed from start.

### Inherited from `ProblemSearch`
- `grid -> Grid` (property): Returns the grid (raises `ValueError` if not loaded).
- `name_grid -> str` (property): Returns the grid's name.
- `successors(state: State) -> list[State]`: Returns valid neighbor states.
- `load_grid(grids: dict[str, Grid]) -> None`: Reloads grid after deserialization.
- `__getstate__() -> dict`: Excludes grid from pickle (lightweight serialization).

### Inherited from `HasStart`
- `start -> State` (property): Returns the start state.

### Inherited from `ProblemAlgo` (via `ProblemSearch`)
- `name -> str` (property): Returns the problem's name.
- `key -> SupportsEquality` (property): Abstract equality key.
- `__eq__`, `__ne__`, `__hash__`: Equality based on `key`.

## Inheritance (Hierarchy)

```
HasName + Equatable
        |
    ProblemAlgo
        |
    ProblemSearch   HasStart
        \            /
     ProblemNeighborhood
```

| Base | Responsibility |
|------|---------------|
| `ProblemAlgo` | Named, equatable problem identity |
| `ProblemSearch` | Grid storage, successor generation, pickle support |
| `HasStart` | Single start state property |

## Dependencies

| Import | Used For |
|--------|----------|
| `f_search.problems.i_0_base.main.ProblemSearch` | Base class for grid problems |
| `f_search.ds.state.StateCell` (as `State`) | State representation |
| `f_ds.grids.GridMap` (as `Grid`) | 2D grid search space |
| `f_search.problems.mixins.HasStart` | Start state mixin |

## Usage Example

### Via Factory
```python
from f_search.problems.i_1_neighborhood import ProblemNeighborhood

problem = ProblemNeighborhood.Factory.without_obstacles()
print(problem.start)       # StateCell at grid[0][0]
print(problem.steps_max)   # 1
print(problem.grid)        # 4x4 grid without obstacles
```

### Direct Construction
```python
from f_ds.grids import GridMap as Grid
from f_search.ds.state import StateCell as State
from f_search.problems.i_1_neighborhood import ProblemNeighborhood

grid = Grid.Factory.four_without_obstacles()
start = State(key=grid[0][0])
problem = ProblemNeighborhood(grid=grid, start=start, steps_max=3)

successors = problem.successors(start)
```
