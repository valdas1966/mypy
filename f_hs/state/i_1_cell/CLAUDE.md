# StateCell

## Purpose
Search state wrapping a CellMap for 2D grid-based pathfinding.
Pure identity over the cell key, plus a `to_tuple()` convenience.
State-to-state **distance is not here** — it lives on `ProblemGrid`
(`ProblemGrid.distance`, the move-model-aware home), built on the
`CellMap` geometric primitive (`cell.distance`). A `StateCell` carries
no metric.

## Public API

### Constructor
```python
def __init__(self, key: CellMap) -> None
```

### Methods
| Method | Signature | Description |
|--------|-----------|-------------|
| `to_tuple` | `() -> tuple[int, int]` | (row, col) of the underlying cell |

State-to-state distance moved to `ProblemGrid.distance(a, b)`
(2026-06-27) — the space owns the metric choice; `StateCell` is pure
identity.

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
