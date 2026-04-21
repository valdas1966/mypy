# Cluster (Abstract Base)

## Purpose
Abstract root of the cluster hierarchy. Represents a set of valid
`CellMap`s on a `GridMap`. Subclasses define the shape (Manhattan ball,
rectangle, disk, arbitrary seed-BFS, …) by implementing `to_iterable()`.

## Public API

### Constructor

```python
def __init__(self,
             grid: GridMap,
             name: str = 'Cluster') -> None
```

### Properties

| Property | Type | Source |
|----------|------|--------|
| `grid` | `GridMap` | this class |
| `name` | `str` | this class |
| `cells` | `list[CellMap]` | `list(to_iterable())` |

### Abstract

```python
def to_iterable(self) -> list[CellMap]
```
Inherited (abstract) from `Collectionable`. Subclasses must implement —
returns the cells that make up the cluster.

```python
@property
def center(self) -> CellMap
```
Abstract — every concrete cluster must expose a representative center
cell. Required by `PairCluster.distance`, which measures Manhattan
distance between two clusters' centers.

### Free from `Collectionable`

`len()`, `in`, `iter()`, `bool()`, default `__str__` — all dispatched
through `to_iterable()`.

## Inheritance

```
Collection[CellMap], Sizable
 └── Collectionable[CellMap]
      └── Cluster (abstract)
           └── ClusterDiamond, …
```

## Notes
- `Cluster` itself has no `Factory`; concrete shapes provide their own.
- `__repr__` is overridden here; `__str__` is left to concrete subclasses
  so each shape can show its identifying parameters.
