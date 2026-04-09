# StateCell

## Purpose
Search state wrapping a CellMap for 2D grid-based pathfinding.
Adds Manhattan distance calculation.

## Public API

### Constructor
```python
def __init__(self, key: CellMap) -> None
```

### Properties
| Property | Type | Description |
|----------|------|-------------|
| `rc` | `tuple[int, int]` | (row, col) of the underlying cell |

### Methods
| Method | Signature | Description |
|--------|-----------|-------------|
| `distance` | `(other: StateCell) -> int` | Manhattan distance |

## Factory
| Method | Returns | Description |
|--------|---------|-------------|
| `at(row, col)` | `StateCell` | At given position |
| `origin()` | `StateCell` | At (0, 0) |
| `a()` | `StateCell` | At (0, 0) |
| `b()` | `StateCell` | At (2, 2) |

## Inheritance
```
StateBase[CellMap]
    └── StateCell
```

## Dependencies
- `f_hs.state.i_0_base.StateBase`
- `f_ds.grids.cell.i_1_map.CellMap`
