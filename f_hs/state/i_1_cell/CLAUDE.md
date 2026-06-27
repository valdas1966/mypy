# StateCell

## Purpose
`StateCell` is a **type alias** — `StateCell = StateBase[CellMap]` — for a
search state keyed on a `CellMap` (2D grid pathfinding). It is **not** a
subclass: it carries no behavior of its own, so by the codebase rule
(behaviorless states use `StateBase[Key]` directly) it is a name, not a
class.

```python
StateCell = StateBase[CellMap]   # main.py
```

Collapsed from a subclass to an alias on 2026-06-27. The old subclass
existed only for `.distance` (moved to `ProblemGrid.distance` earlier the
same day) and a `to_tuple()` convenience (migrated to `state.key.to_tuple()`
at every call site). With both gone it added no behavior, so it became an
alias. `Factory.at(row, col)` moved to `ProblemGrid.state_at(row, col)` —
the Problem owns the one-state-per-cell cache, so state lookup belongs there.

## API
`StateCell(key=cell)` constructs a `StateBase` (the alias is callable).
`key` / `__eq__` / `__lt__` / `__hash__` / `__str__` / `__repr__` all come
from `StateBase` via `HasKey`, delegating to the `CellMap` key.

- `(row, col)` of a state: `state.key.to_tuple()` (CellMap's `to_tuple`).
- state-to-state distance: `ProblemGrid.distance(a, b)`.
- the state for a cell: `ProblemGrid.state_at(row, col)`.

Canonical `(row, col)` identity for recording tests is produced by
`f_core.canonize.canonize`, which descends `.key → CellMap → (row, col)`
via the `HasKey` / `HasRowCol` chain (independent of the alias).

## Inheritance
```
StateBase[CellMap]   (StateCell is this exact alias — no subclass)
```

## Dependencies
- `f_hs.state.StateBase` (aggregator)
- `f_ds.grids.CellMap` (aggregator)
