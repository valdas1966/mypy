# CellMap

## Purpose
Cell for 2D-grid maps. Extends `CellBase` with a mutable validity
flag (`ValidatableMutable`) marking the cell as passable/blocked.

## Public API

### Constructor
```python
def __init__(self,
             row: int,
             col: int,
             is_valid: bool = True,
             name: str = 'CellMap') -> None
```

### Inherited from `CellBase`
| Member | Description |
|--------|-------------|
| `key` | `(row, col)` — equality/ordering/hash |
| `row`, `col`, `to_tuple()` | Position |
| `distance`, `neighbors`, `is_within` | Grid geometry |
| `name`, `__str__`, `__repr__` | Naming / rendering |

### Inherited from `ValidatableMutable`
| Member | Description |
|--------|-------------|
| `is_valid` | `bool` — whether the cell is passable |
| `set_valid()` | Mark valid |
| `set_invalid()` | Mark invalid |

## Factory
| Method | Returns | Description |
|--------|---------|-------------|
| `at(row, col=None)` | `CellMap` | At `(row, col)`; `col` defaults to `row` |
| `zero()` | `CellMap` | At `(0, 0)` |
| `one()` | `CellMap` | At `(1, 1)` |
| `million()` | `CellMap` | At `(1_000_000, 1_000_000)` |

## Inheritance
```
CellBase, ValidatableMutable
    └── CellMap
```

## Dependencies
- `f_ds.grids.cell.i_0_base.CellBase`
- `f_core.mixins.validatable_mutable.ValidatableMutable`

## Usage
```python
from f_ds.grids.cell.i_1_map import CellMap

cell = CellMap(row=5, col=3, is_valid=True, name='MyCell')
cell.set_invalid()                 # block it
diag = CellMap.Factory.at(2)       # CellMap(2, 2)
```
