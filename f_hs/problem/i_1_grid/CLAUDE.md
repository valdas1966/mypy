# ProblemGrid

## Purpose
Shortest-Path-Problem on a 2D GridMap. Successors are valid
grid neighbors. Caches StateCell objects for efficiency.

## Public API

### Constructor
```python
def __init__(self, grid: GridMap, start: CellMap,
             goal: CellMap, name: str = 'ProblemGrid') -> None
```

### Properties
| Property | Type | Description |
|----------|------|-------------|
| `grid` | `GridMap` | The underlying grid |

### Methods
| Method | Description |
|--------|-------------|
| `successors(state)` | Valid grid neighbors |

## Factory
| Method | Description |
|--------|-------------|
| `grid_3x3()` | Open 3x3, (0,0)->(2,2), cost 4 |
| `grid_3x3_obstacle()` | Obstacle at (1,1) |
| `grid_3x3_no_path()` | Wall across middle row |
| `grid_3x3_start_is_goal()` | Start == Goal |

## Dependencies
- `f_hs.problem.i_0_base.ProblemSPP`
- `f_hs.state.i_1_cell.StateCell`
- `f_ds.grids.grid.map.GridMap`
