# Cluster (Abstract Base)

## Purpose
Abstract root of the cluster hierarchy. Represents a set of valid
`CellMap`s on a `GridMap`. Subclasses define the shape (Manhattan ball,
rectangle, disk, arbitrary seed-BFS, …) by implementing `to_iterable()`.

**Holds only the grid's NAME (`map: str`), not the grid object.** The
grid is required at construction time by the subclass `_build()` (BFS,
neighbor lookup, …) and released as soon as `__init__` returns. This
keeps clusters light: pickle small, can outlive the in-memory grid,
and don't pin large grids in caller scopes that have already moved on.

## Public API

### Constructor

```python
def __init__(self,
             grid: GridMap,
             name: str = 'Cluster') -> None
```
Snapshots `grid.name` into `self._map` and discards the grid reference.
Concrete subclasses must consume `grid` inside their own `__init__`
(typically by passing it to `_build(grid=grid)`); the base does not
retain it.

### Properties

| Property | Type | Source |
|----------|------|--------|
| `map` | `str` | this class — the grid's name (only grid identity retained) |
| `name` | `str` | this class |
| `cells` | `list[CellMap]` | `list(to_iterable())` |
| `center` | `CellMap \| None` | this class — default `None`; concrete shapes with a natural center override |

### Abstract

```python
def to_iterable(self) -> list[CellMap]
```
Inherited (abstract) from `Collectionable`. Subclasses must implement —
returns the cells that make up the cluster.

### Free from `Collectionable`

`len()`, `in`, `iter()`, `bool()`, default `__str__` — all dispatched
through `to_iterable()`.

## `center` is optional, not abstract
Not every shape has a meaningful center (rectangle, multi-seed BFS,
arbitrary cell-set). The base returns `None`; concrete shapes with a
natural center (e.g. `ClusterDiamond`) override. `PairCluster.distance`
requires both sides to have non-None centers.

## Inheritance

```
Collection[CellMap], Sizable
 └── Collectionable[CellMap]
      └── Cluster (abstract)
           └── ClusterDiamond, …
```

## Notes
- `Cluster` itself has no `Factory`; concrete shapes provide their own.
- `__repr__` is `<Cluster: map=X, name=Y, cells=N>`; concrete shapes
  override.
- No `to_analytics()` — for structured CSV export, callers build the
  row dict from cluster + grid attributes inline (the script that owns
  the grid already has it in scope).
