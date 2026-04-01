# ProblemOMSPP - One-to-Many Shortest Path Problem

## Purpose
Defines the One-to-Many Shortest Path Problem (OMSPP): finding optimal paths from a single start state to multiple goal states on a grid. Composes `ProblemSearch`, `HasStart`, and `HasGoals` mixins. Provides `to_spps()` decomposition into individual SPP sub-problems.

## Public API

### `__init__(self, grid: Grid, start: State, goals: list[State], name: str = 'ProblemOMSPP') -> None`
Initialize with a grid, a start state, and a list of goal states. Delegates to `ProblemSearch.__init__`, `HasStart.__init__`, and `HasGoals.__init__`.

### `grid -> Grid` (property, inherited from ProblemSearch)
Return the problem's GridMap. Raises `ValueError` if the grid was excluded via pickle and not reloaded.

### `name_grid -> str` (property, inherited from ProblemSearch)
Return the grid's name string.

### `start -> State` (property, inherited from HasStart)
Return the start state.

### `goals -> list[State]` (property, inherited from HasGoals)
Return the list of goal states.

### `successors(self, state: State) -> list[State]` (inherited from ProblemSearch)
Return valid neighbor states from the grid for the given state.

### `h_start -> float` (property)
Returns average Manhattan distance from start to all goals.

### `norm_h_start -> float` (property)
Returns normalized h_start in [0, 100]. Formula: `h_start / (rows + cols - 2) * 100`.

### `h_goals -> float` (property)
Returns average pairwise Manhattan distance between goals. Returns 0.0 if fewer than 2 goals.

### `norm_h_goals -> float` (property)
Returns normalized h_goals in [0, 100]. Formula: `h_goals / (rows + cols - 2) * 100`.

### `to_analytics(self) -> dict` (overrides ProblemSearch)
Extends base dict with `h_start`, `norm_h_start`, `h_goals`, `norm_h_goals`. Inherited keys: `domain`, `map`, `rows`, `cols`, `cells`.

### `to_spps(self) -> list[ProblemSPP]`
Convert this OMSPP into a list of ProblemSPP sub-problems, one per goal. Each sub-problem shares the same grid and start.

### `load_grid(self, grids: dict[str, Grid]) -> None` (inherited from ProblemSearch)
Reload the grid from a name-keyed dictionary after pickling.

### `__getstate__(self) -> dict` (inherited from ProblemSearch)
Exclude the heavy grid object from pickle serialization.

## Inheritance (Hierarchy)

```
ProblemAlgo (f_cs)
  └── ProblemSearch (i_0_base) + HasStart (mixin) + HasGoals (mixin)
        └── ProblemOMSPP (i_2_omspp)
```

| Base | Responsibility |
|------|----------------|
| `ProblemAlgo` | Generic algorithm problem interface |
| `ProblemSearch` | Grid storage, successor generation, pickle support |
| `HasStart` | Single start state property |
| `HasGoals` | Multiple goal states (list) property |

## Dependencies

| Import | Used For |
|--------|----------|
| `f_search.problems.ProblemSearch` | Base class for grid problems |
| `f_search.problems.i_1_spp.main.ProblemSPP` | SPP sub-problem creation in `to_spps()` |
| `f_search.problems.mixins.HasStart` | Start state mixin |
| `f_search.problems.mixins.HasGoals` | Goals list mixin |
| `f_search.ds.state.StateCell` (as `State`) | State representation |
| `f_ds.grids.GridMap` (as `Grid`) | Grid map for the search space |

## Usage Examples

### Create and solve an OMSPP
```python
from f_search.problems import ProblemOMSPP

# Via Factory
problem = ProblemOMSPP.Factory.without_obstacles()

# Access properties
print(problem.start)   # State at (0,0)
print(problem.goals)   # [State at (0,3), State at (3,3)]
print(problem.grid)    # 4x4 GridMap
```

### Decompose into SPP sub-problems
```python
problem = ProblemOMSPP.Factory.with_obstacles()
spps = problem.to_spps()
# spps[0] = ProblemSPP(grid, start, goal_a)
# spps[1] = ProblemSPP(grid, start, goal_b)
```

### Node-categories toy problem
```python
problem = ProblemOMSPP.Factory.for_node_categories()
# 5x5 grid, obstacles at (0,1),(0,3),(1,1)
# Start: (0,2), Goals: [(0,0), (0,4)]
# C*_1 = 6, C*_2 = 4 — asymmetric detours
```

### Custom construction
```python
from f_ds.grids import GridMap as Grid
from f_search.ds.state import StateCell as State
from f_search.problems import ProblemOMSPP

grid = Grid(rows=10)
start = State(key=grid[0][0])
goals = [State(key=grid[0][9]), State(key=grid[9][9])]
problem = ProblemOMSPP(grid=grid, start=start, goals=goals)
```
