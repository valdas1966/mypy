# ClusterGrid (Abstract Base)

## Purpose
Root of the cluster hierarchy: a named set of valid `CellMap`s on a
`GridMap`. Subclasses define the shape (Manhattan ball, rectangle, disk,
arbitrary seed-BFS, …) by filling `_cells` and exposing them through
`to_iterable()`. Composes `Collectionable[CellMap]` (collection behaviour)
and `HasName` (identity); adds the `members`/`cells` accessors.

**Holds only the grid's NAME (`map: str`), not the grid object.** The
grid is required at construction time by the subclass `_build()` (BFS,
neighbor lookup, …) and released as soon as `__init__` returns. This
keeps clusters light: pickle small, can outlive the in-memory grid,
and don't pin large grids in caller scopes that have already moved on.

## Public API

### Constructor

```python
def __init__(self, grid: GridMap) -> None
```
Snapshots `grid.name` into `self._map`, sets `name` to the concrete
class name, and discards the grid reference. Concrete subclasses must
consume `grid` inside their own `__init__` (typically by passing it to
`_build(grid=grid)`); the base does not retain it.

### Properties

| Property | Type | Source |
|----------|------|--------|
| `map` | `str` | this class — the grid's name (grid-local provenance) |
| `name` | `str` | `HasName` |
| `cells` | `list[CellMap]` | this class — a list copy of the members |
| `members` | `list[CellMap]` | this class — `list(to_iterable())` |

### `to_iterable`

```python
def to_iterable(self) -> list[CellMap]
```
Returns the underlying `_cells`. Drives `len()`, `in`, `iter()`,
`bool()` via `Collectionable`. Subclasses fill `_cells` in their own
`__init__`.

### String forms
- `__str__` → `'name(size=n)'`.
- `__repr__` → `<ClusterGrid: map=X, cells=N>`; concrete shapes override.

## The distinguished cell lives on the shape, not the base
The base is just a named cell collection; it defines no
center/representative. Shapes that have a natural distinguished cell
expose it themselves (e.g. `ClusterDiamond.center`).

## Inheritance

```
Collectionable[CellMap]   HasName
        └────────┬────────┘
            ClusterGrid (abstract)        ← this class — root of the hierarchy
              └── ClusterDiamond, …       (concrete shapes)
```

`ClusterGrid` was previously a grid specialisation of a separate generic
`f_ds.clusters.ClusterBase`; that generic layer was removed (no non-grid
consumer) and its machinery folded in here.

## Notes
- `ClusterGrid` is abstract by intent (lives in `i_0_base/`, declared
  `ABC`) and has no `Factory`; concrete shapes provide their own.
- No `to_analytics()` — for structured CSV export, callers build the
  row dict from cluster + grid attributes inline (the script that owns
  the grid already has it in scope).
