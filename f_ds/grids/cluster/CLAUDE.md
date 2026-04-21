# Cluster Package

## Purpose
Reusable cell-set clusters on a `GridMap`. The package houses an abstract
`Cluster` and one concrete shape so far (`ClusterDiamond` — Manhattan ball).
Designed so new shapes (rect, disk, BFS-from-seed, custom) plug in without
refactor.

## Package Exports

```python
from f_ds.grids.cluster import (
    Cluster, ClusterDiamond, PairCluster)
```

Also re-exported from `f_ds.grids` for convenience:

```python
from f_ds.grids import Cluster, ClusterDiamond, PairCluster
```

## Module Hierarchy

```
f_ds/grids/cluster/
├── __init__.py          lazy re-exports
├── i_0_base/            abstract Cluster
│   ├── main.py
│   └── __init__.py
├── i_1_diamond/         ClusterDiamond (Manhattan ball)
│   ├── main.py
│   ├── _factory.py
│   ├── _tester.py
│   └── __init__.py
└── pair/                PairCluster[T]
    ├── main.py
    ├── _factory.py
    ├── _tester.py
    └── __init__.py
```

## Design Notes

- Clusters compose `Collectionable[CellMap]` from `f_ds.mixins.collectionable`,
  so `len()`, `in`, iteration, `bool()` all come for free from `to_iterable()`.
- `ClusterDiamond` is built via BFS from the center (connected-component
  semantics): walls split the geometric ball into disconnected regions; only
  the component containing the center is retained.
- `Cluster` is abstract and has no `Factory`; concrete subclasses have their
  own.

## Quick Usage

```python
from f_ds.grids import GridMap, ClusterDiamond

grid = GridMap(rows=10, cols=10)

# Deterministic
cluster = ClusterDiamond.Factory.at_center(
    grid=grid, center=grid[5][5], steps=2)
print(len(cluster))   # 13

# Random with a floor on size
cluster = ClusterDiamond.Factory.random(
    grid=grid, min_cells=8, steps=2)
```
