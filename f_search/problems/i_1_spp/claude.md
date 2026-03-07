# ProblemSPP - One-to-One Shortest Path Problem

## Purpose
Defines a one-to-one shortest path problem on a grid: find the optimal path from a single start state to a single goal state. Composes grid search functionality with start and goal mixins. Supports pickling (grid excluded) and reversing (start/goal swap).

## Public API

### Constructor
```python
def __init__(self,
             grid: Grid,
             start: State,
             goal: State,
             name: str = 'ProblemSPP') -> None:
```
Initializes grid (via ProblemSearch), start (via HasStart), and goal (via HasGoal).

### `h_start -> int` (property)
Returns the Manhattan distance between start and goal states. Delegates to `self.start.distance(other=self.goal)`.

### `norm_h_start -> float` (property)
Returns the normalized distance in [0, 100]. Formula: `h_start / (rows + cols - 2) * 100`. Returns 0.0 for trivial grids.

### `to_analytics(self) -> dict` (overrides ProblemSearch)
Extends base dict with `h_start` (int) and `norm_h_start` (float). Inherited keys: `domain`, `map`, `rows`, `cols`, `cells`.

### `reverse(name: str = None) -> Self`
Returns a new ProblemSPP with start and goal swapped. Same grid reference. Uses `name` if provided, otherwise keeps the current name.

### Inherited from ProblemSearch
```python
@property
def grid(self) -> Grid:
```
Returns the grid. Raises `ValueError` if grid was excluded during pickling and not yet reloaded.

```python
@property
def name_grid(self) -> str:
```
Returns the grid's name string.

```python
def successors(self, state: State) -> list[State]:
```
Returns valid neighbor states from the grid.

```python
def load_grid(self, grids: dict[str, Grid]) -> None:
```
Reloads the grid from a name-keyed dictionary after unpickling.

```python
def __getstate__(self) -> dict:
```
Excludes the heavy grid from pickle serialization.

### Inherited from HasStart
```python
@property
def start(self) -> State:
```
Returns the start state.

### Inherited from HasGoal
```python
@property
def goal(self) -> State:
```
Returns the goal state.

### Class Attribute
```python
Factory: type = None
```
Wired to the Factory class in `__init__.py`.

## Inheritance (Hierarchy)

```
ProblemAlgo
  └── ProblemSearch          (grid, successors, __getstate__, load_grid)
        └── ProblemSPP       (+ HasStart + HasGoal, reverse)
```

| Base | Responsibility |
|------|----------------|
| `ProblemAlgo` | Generic algorithm problem interface |
| `ProblemSearch` | Grid storage, successor generation, pickle support |
| `HasStart` | Single start state property |
| `HasGoal` | Single goal state property |

## Dependencies

| Import | Purpose |
|--------|---------|
| `f_search.problems.ProblemSearch` | Base class for grid search problems |
| `f_search.ds.state.StateCell` (as `State`) | State representation wrapping grid cells |
| `f_ds.grids.GridMap` (as `Grid`) | 2D grid map defining the search space |
| `f_search.problems.mixins.HasStart` | Mixin providing start state |
| `f_search.problems.mixins.HasGoal` | Mixin providing goal state |
| `typing.Self` | Return type for reverse() |

## Usage Examples

### Create via Factory
```python
from f_search.problems.i_1_spp import ProblemSPP

problem = ProblemSPP.Factory.without_obstacles()
print(problem.start)   # State at grid[0][0]
print(problem.goal)    # State at grid[0][3]
print(problem.grid)    # 4x4 GridMap
```

### Reverse a Problem
```python
problem = ProblemSPP.Factory.without_obstacles()
reversed_problem = problem.reverse(name='Reversed')
assert reversed_problem.start == problem.goal
assert reversed_problem.goal == problem.start
assert reversed_problem.grid is problem.grid
```

### Manual Construction
```python
from f_ds.grids import GridMap as Grid
from f_search.ds.state import StateCell as State
from f_search.problems.i_1_spp import ProblemSPP

grid = Grid.Factory.four_without_obstacles()
start = State(key=grid[0][0])
goal = State(key=grid[0][3])
problem = ProblemSPP(grid=grid, start=start, goal=goal)
```
