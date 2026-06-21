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
| `distance` | `(other: Self) -> int` | Manhattan distance |

`__str__` / `__repr__` / `__eq__` / `__lt__` / `__hash__` come from
`HasKey` (all delegate to `key`); `StateCell` adds no overrides.

Canonical `(row, col)` identity for recording tests is now
produced by `f_core.canonize.canonize` (descends
`StateCell → CellMap → (row, col)` via the `HasKey` /
`HasRowCol` chain). The old `event_key()` override was
deleted 2026-06-20.

## Factory
| Method | Returns | Description |
|--------|---------|-------------|
| `at(row, col=None)` | `StateCell` | At `(row, col)`; `col` defaults to `row` |

## Inheritance
```
StateBase[CellMap]
    └── StateCell
```

## Dependencies
- `f_hs.state.StateBase` (aggregator)
- `f_ds.grids.CellMap` (aggregator, aliased `Cell`)
