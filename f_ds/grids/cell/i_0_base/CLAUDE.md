# CellBase

## Purpose
Base class for a cell in a 2D grid. Identity is its `(row, col)`
position (via `HasRowCol`); also carries a display `name` (via
`HasName`).

## Public API

### Constructor
```python
def __init__(self, row: int, col: int, name: str = 'CellBase') -> None
```

### Properties
| Property | Type | Description |
|----------|------|-------------|
| `key` | `tuple[int, int]` | `(row, col)` — drives equality/ordering/hash |

### Methods
| Method | Signature | Description |
|--------|-----------|-------------|
| `__str__` | `() -> str` | `'Name(row,col)'` |
| `__repr__` | `() -> str` | `'<CellBase: Name=…, Row=…, Col=…>'` |

### Inherited from `HasRowCol`
| Member | Description |
|--------|-------------|
| `row`, `col` | Position components |
| `rc` | `(row, col)` tuple |
| `distance` | `(other: Self) -> int` — Manhattan distance |
| `neighbors` | `() -> list[Self]` — adjacent cells |
| `is_within` | bounds check |
| `__eq__`, `__lt__`, `__hash__` | Via `key` (`Comparable`, `Hashable`) |

### Inherited from `HasName`
| Member | Description |
|--------|-------------|
| `name` | Display name |

## Factory
| Method | Returns | Description |
|--------|---------|-------------|
| `zero()` | `CellBase` | Name `'Zero'` at `(0, 0)` |

## Inheritance
```
HasRowCol, HasName
    └── CellBase
```

## Dependencies
- `f_core.mixins.has.row_col.HasRowCol`
- `f_core.mixins.has.name.HasName`

## Usage
```python
from f_ds.grids.cell.i_0_base import CellBase

cell = CellBase(row=2, col=3, name='A')   # A(2,3)
origin = CellBase.Factory.zero()          # Zero(0,0)
d = cell.distance(origin)                  # 5
```
