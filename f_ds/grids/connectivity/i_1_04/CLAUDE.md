# Connectivity_4

## Purpose
4-connectivity (von Neumann): the 4 cardinal neighbors, uniform edge
cost `1`, Manhattan heuristic. Reproduces the legacy 2D-grid behavior —
the default policy, so existing grids are byte-for-byte unchanged.

## Public API

### Properties
| Property | Value | Description |
|----------|-------|-------------|
| `offsets` | `((-1,0),(0,1),(1,0),(0,-1))` | Cardinal deltas, clockwise (N, E, S, W) |
| `unit` | `1` | Inherited; true distance = `cost` |

### Methods
| Method | Returns | Description |
|--------|---------|-------------|
| `cost(a, b)` | `1` | Uniform edge cost |
| `heuristic(a, b)` | `int` | Manhattan distance (delegates to `HasRowCol.distance`) |
| `is_legal_move(a, b, grid)` | `True` | Inherited — cardinals never cut a corner |

## Internal Constants
| Name | Scope | Value | Meaning |
|------|-------|-------|---------|
| `_OFFSETS` | class (private) | 4 cardinal deltas | Clockwise N, E, S, W (matches legacy `HasRowCol.neighbors` order); read via the `offsets` property |

## Inheritance
```
ConnectivityBase
 └── Connectivity_4
```

## Dependencies
- `f_ds.grids.connectivity.i_0_base.ConnectivityBase`
- `f_core.mixins.has.row_col.HasRowCol`

## Usage
```python
from f_ds.grids.connectivity import Connectivity_4

c = Connectivity_4()
c.cost(a=cell_0, b=cell_1)        # 1
c.heuristic(a=cell_0, b=cell_1)   # Manhattan
```
