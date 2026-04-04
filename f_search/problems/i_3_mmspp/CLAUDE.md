# ProblemMMSPP - Many-to-Many Shortest Path Problem

## Main Class
`ProblemMMSPP(ProblemSearch, HasStarts, HasGoals)`

## Purpose
Defines the Many-to-Many Shortest Path Problem (MMSPP): finding
optimal paths from each of m start states to each of k goal states
on a grid. Produces m × k shortest paths.

## Public API

### `__init__(self, grid: Grid, starts: list[State], goals: list[State], name: str = 'ProblemMMSPP') -> None`
Initialize with a grid, list of start states, and list of goal states.

### `starts -> list[State]` (property, from HasStarts)
Return the list of start states.

### `goals -> list[State]` (property, from HasGoals)
Return the list of goal states.

### `h_starts -> float` (property)
Avg pairwise Manhattan distance between starts. Returns 0.0 if < 2.

### `norm_h_starts -> float` (property)
Normalized h_starts [0,1] relative to max Manhattan distance.

### `h_goals -> float` (property)
Avg pairwise Manhattan distance between goals. Returns 0.0 if < 2.

### `norm_h_goals -> float` (property)
Normalized h_goals [0,1] relative to max Manhattan distance.

### `h_cross -> float` (property)
Avg Manhattan distance from each start to each goal (m×k pairs).

### `norm_h_cross -> float` (property)
Normalized h_cross [0,1] relative to max Manhattan distance.

### `to_omspps() -> list[ProblemOMSPP]`
Decompose into m OMSPP sub-problems (one per start → all goals).

### `to_mospps() -> list[ProblemOMSPP]`
Decompose into k reverse OMSPP sub-problems (one per goal → all
starts). Each OMSPP uses a goal as "start" and all starts as "goals"
(valid on undirected grids).

### `to_spps() -> list[ProblemSPP]`
Decompose into m×k SPP sub-problems (every start-goal pair).

### `to_analytics() -> dict`
Extends base dict with h_starts, h_goals, h_cross and their
normalized variants.

## Inheritance (Hierarchy)

```
ProblemAlgo (f_cs)
  └── ProblemSearch (i_0_base) + HasStarts + HasGoals
        └── ProblemMMSPP (i_3_mmspp)
```

## Dependencies

| Import | Used For |
|--------|----------|
| `ProblemSearch` | Base class for grid problems |
| `ProblemOMSPP` | Sub-problem creation in `to_omspps()` |
| `ProblemSPP` | Sub-problem creation in `to_spps()` |
| `HasStarts` | Multiple start states mixin |
| `HasGoals` | Multiple goal states mixin |
| `StateCell` (as `State`) | State representation |
| `GridMap` (as `Grid`) | Grid map |

## Usage Example

```python
from f_search.problems import ProblemMMSPP

# Via Factory
problem = ProblemMMSPP.Factory.without_obstacles()
print(problem.starts)  # [State(0,0), State(3,0)]
print(problem.goals)   # [State(0,3), State(3,3)]

# Decompose into OMSPPs
omspps = problem.to_omspps()  # 2 OMSPPs (one per start)

# Decompose into SPPs
spps = problem.to_spps()  # 4 SPPs (2 starts × 2 goals)
```

## Tests (`_tester.py`)

| Test | Description |
|------|-------------|
| `test_starts_goals` | Verify starts/goals properties |
| `test_h_starts` | h_starts == 3.0 (Manhattan between starts) |
| `test_h_goals` | h_goals == 3.0 (Manhattan between goals) |
| `test_h_cross` | h_cross == 4.5 (avg cross distances) |
| `test_to_omspps` | 2 OMSPPs with correct starts/goals/grid |
| `test_to_mospps` | 2 reverse OMSPPs (goal→starts) with correct data |
| `test_to_spps` | 4 SPPs with correct start-goal pairs |
| `test_to_analytics` | Analytics dict has all expected keys |
