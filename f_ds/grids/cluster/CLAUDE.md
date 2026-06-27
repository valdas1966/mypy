# Cluster Package

## Purpose
Reusable cell-set clusters on a `GridMap`. The package houses an abstract
`ClusterGrid` and one concrete shape so far (`ClusterDiamond` — Manhattan ball).
Designed so new shapes (rect, disk, BFS-from-seed, custom) plug in without
refactor.

## Package Exports

```python
from f_ds.grids.cluster import ClusterGrid, ClusterDiamond, PairCluster
```

Also re-exported from `f_ds.grids` for convenience:

```python
from f_ds.grids import ClusterGrid, ClusterDiamond, PairCluster
```

## Module Hierarchy

```
f_ds/grids/cluster/
├── __init__.py          lazy re-exports
├── i_0_grid/            abstract ClusterGrid
│   ├── main.py
│   └── __init__.py
├── i_1_diamond/         ClusterDiamond (Manhattan ball)
│   ├── main.py
│   ├── _factory.py
│   ├── _tester.py
│   └── __init__.py
└── i_2_pair/            PairCluster (ordered value-record of 2 diamonds)
    ├── main.py
    ├── _factory.py
    ├── _tester.py
    └── __init__.py
```

`i_2_pair/` holds `PairCluster(Tupleable)` (`to_tuple() = (a, b)`).
**Caveat on the prefix:** unlike `i_0_`/`i_1_`, which mark *inheritance
depth* in the `ClusterGrid` hierarchy, `PairCluster` does **not** inherit
`ClusterGrid` — it *composes* two `ClusterDiamond`s. The `i_2_` prefix
is used (by project choice) to mark it as the layer built directly on top
of `i_1_diamond`, not as a `ClusterGrid` subclass.

## Design Notes

- `ClusterGrid` is the abstract root of the hierarchy. It composes
  `Collectionable[CellMap]` (collection behaviour) and `HasName`
  (identity), and adds the `map`/`cells` accessors. Its `__init__` takes
  an optional `name` (default `'ClusterGrid'`). (It was once a
  specialisation of a separate
  generic `f_ds.clusters.ClusterBase`; that layer was removed and folded
  in — no non-grid consumer existed.)
- `map: str` (the grid's NAME) is grid-local provenance — the grid
  object is never retained. It is part of `ClusterDiamond.key`.
- Clusters compose `Collectionable[CellMap]`, so `len()`, `in`,
  iteration, `bool()` all come for free from `to_iterable()`.
- `ClusterDiamond` is built via BFS from the center (connected-component
  semantics): walls split the geometric ball into disconnected regions; only
  the component containing the center is retained.
- `ClusterGrid` is abstract and has no `Factory`; concrete subclasses have their
  own.

## Quick Usage

```python
from f_ds.grids import GridMap, ClusterDiamond

grid = GridMap(rows=10, cols=10)

# Deterministic — call the constructor directly
cluster = ClusterDiamond(grid=grid, center=grid[5][5], steps=2)
print(len(cluster))   # 13

# Random with a floor on size
cluster = ClusterDiamond.Factory.random(
    grid=grid, min_cells=8, steps=2)
```
