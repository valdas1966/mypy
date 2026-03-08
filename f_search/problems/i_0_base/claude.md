# ProblemSearch - Base Class for Grid Search Problems

## Purpose
Base class for all search problems operating on 2D grid maps. Stores a grid
reference and grid name, generates successor states via grid neighbors, and
supports lightweight pickling by excluding the heavy grid object.

## Public API

### `__init__(self, grid: Grid, name: str = 'ProblemSearch') -> None`
Initialize with a grid. Stores both `_grid` and `_name_grid` (grid's name).

### `grid -> Grid` (property)
Return the problem's grid. Raises `ValueError` if grid is `None` (not loaded after unpickling).

### `name_grid -> str` (property)
Return the grid's name. Survives pickle (stored independently from the grid object).

### `successors(self, state: State) -> list[State]`
Return successor states by querying `grid.neighbors(cell=state.key)` and wrapping each neighbor cell as a `StateCell`.

### `to_analytics(self) -> dict`
Delegates to `self.grid.to_analytics()` and returns the resulting dict. Subclasses extend this dict with additional keys.

### `load_grid(self, grids: dict[str, Grid]) -> None`
Restore the grid reference after unpickling. Looks up `_name_grid` in the provided dict.

### `__getstate__(self) -> dict`
Custom pickle support. Returns a copy of `__dict__` with `_grid` set to `None`, excluding the heavy grid from serialization.

### Inherited from `ProblemAlgo`
- `name -> str` (property): the problem's name.
- `__eq__`, `__ne__`, `__hash__`: equality via `key`.

### Class Attribute
```python
Factory: type | None = None
```

## Inheritance (Hierarchy)

```
HasName
    \
     ProblemAlgo (Equatable)
    /
Equatable
    \
     ProblemSearch
```

| Base | Responsibility |
|------|---------------|
| `HasName` | `name` property and `__str__`/`__repr__` |
| `Equatable` | `__eq__`, `__ne__`, `__hash__` via `key` |
| `ProblemAlgo` | Abstract problem interface for algorithms |

## Dependencies

| Import | Used For |
|--------|----------|
| `f_ds.grids.GridMap` (aliased `Grid`) | 2D grid search space |
| `f_cs.problem.main.ProblemAlgo` | Base class for algorithm problems |
| `f_search.ds.state.StateCell` (aliased `State`) | State wrapper for grid cells |

## Usage Examples

### Creating and querying a problem
```python
from f_search.problems.i_0_base import ProblemSearch

problem = ProblemSearch.Factory.grid_3x3()
cell_00 = problem.grid[0][0]
state = StateBase(key=cell_00)
successors = problem.successors(state=state)
# Returns neighbors of (0,0) as StateCell objects
```

### Pickle round-trip with grid restoration
```python
import pickle

problem = ProblemSearch.Factory.grid_3x3()
grid = problem.grid

# Pickle excludes grid
data = pickle.dumps(problem)
loaded = pickle.loads(data)
assert loaded._grid is None
assert loaded.name_grid == '3x3'

# Restore grid from dict
loaded.load_grid(grids={grid.name: grid})
assert loaded.grid == grid
```
