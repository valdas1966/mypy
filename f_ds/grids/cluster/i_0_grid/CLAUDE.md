# ClusterGrid (Abstract Base)

## Purpose
Root of the cluster hierarchy: a named set of valid `CellMap`s on a
`GridMap`. Subclasses define the shape (Manhattan ball, rectangle, disk,
arbitrary seed-BFS, …) by filling `_cells` and exposing them through
`to_iterable()`. Composes `Collectionable[CellMap]` (collection behaviour)
and `HasName` (identity); adds the `map`/`cells` accessors.

**Holds only the grid's NAME (`map: str`), not the grid object.** The
grid is required at construction time by the subclass `_build()` (BFS,
neighbor lookup, …) and released as soon as `__init__` returns. This
keeps clusters light: pickle small, can outlive the in-memory grid,
and don't pin large grids in caller scopes that have already moved on.

## Public API

### Constructor

```python
def __init__(self, grid: GridMap, name: str = 'ClusterGrid') -> None
```
Snapshots `grid.name` into `self._map`, sets the cluster's `name` (a
constructor argument, default `'ClusterGrid'`), initialises an empty
`_cells`, and discards the grid reference. Concrete subclasses must
consume `grid` inside their own `__init__` (typically by passing it to
`_build(grid=grid)`); the base does not retain it. (Subclasses pass
their own `name` through — e.g. `ClusterDiamond` defaults it to
`'ClusterDiamond'`.)

### Properties

| Property | Type | Source |
|----------|------|--------|
| `map` | `str` | this class — the grid's name (grid-local provenance) |
| `name` | `str` | `HasName` |
| `cells` | `list[CellMap]` | this class — a list copy of `_cells` |

### `to_iterable`

```python
def to_iterable(self) -> list[CellMap]
```
Returns the underlying `_cells`. Drives `len()`, `in`, `iter()`,
`bool()` via `Collectionable`. Subclasses fill `_cells` in their own
`__init__`.

(`members` was removed — read the cells via `cells` or iterate the
cluster directly, e.g. `list(cluster)`.)

### String forms
`ClusterGrid` defines neither — both come from `HasName` / `HasRepr`:
- `__str__` → the `name` (e.g. `'ClusterGrid'`).
- `__repr__` → `<ClassName: name>` (via `HasRepr`).

Concrete shapes may override (e.g. `ClusterDiamond.__str__`).

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
- `ClusterGrid` is abstract by intent (lives in `i_0_grid/`, declared
  `ABC`) and has no `Factory`; concrete shapes provide their own.
- No `to_analytics()` — for structured CSV export, callers build the
  row dict from cluster + grid attributes inline (the script that owns
  the grid already has it in scope).
