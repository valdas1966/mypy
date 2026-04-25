# ClusterDiamond

## Purpose
Diamond-shaped (Manhattan-ball) cluster of valid cells on a `GridMap`.
Built via BFS from a center cell to depth `steps`, skipping walls —
returns only the connected component containing the center.

Inherits `Cluster` (light: holds `map: str`, not the grid) and
`Hashable` (eq + hash via `key`).

## Public API

### Constructor

```python
def __init__(self,
             grid: GridMap,
             center: CellMap,
             steps: int,
             name: str = 'ClusterDiamond') -> None
```
The `grid` is consumed by `_build` and **not** retained on `self`.

### Properties

| Property | Type | Meaning |
|----------|------|---------|
| `center` | `CellMap` | center of the diamond (overrides `Cluster.center: None` default) |
| `steps` | `int` | Manhattan radius |
| `key` | `tuple[str, tuple[int,int], int]` | `(map, center.key, steps)` — drives `__eq__` / `__hash__` |
| `map`, `name`, `cells` | — | inherited from `Cluster` |

### Identity (via `Hashable`)
`__eq__` and `__hash__` come from `f_core.mixins.hashable.Hashable`,
both delegating to `key = (map, center.key, steps)`. Two diamonds with
the same `(map, center, steps)` are equal and hash the same; differing
on any field (including map name) makes them distinct. Usable in
`set` / `dict`.

### Collection behavior (inherited from `Collectionable`)

```python
len(cluster)      # number of valid cells
cell in cluster   # membership test
list(cluster)     # iteration
bool(cluster)     # True iff non-empty
```

## Factory

```python
ClusterDiamond.Factory.at_center(grid, center, steps) -> ClusterDiamond
ClusterDiamond.Factory.random(grid, min_cells, steps,
                              max_tries=100) -> ClusterDiamond
ClusterDiamond.Factory.a() -> ClusterDiamond
```

- `random(...)` samples a center via `grid.random.cells(size=1)` and retries
  until `|cluster| >= min_cells`. Raises `ValueError` after `max_tries`.
- `a()` returns the canonical 5-cell test instance on
  `GridMap.Factory.four_without_obstacles()` centered at `(1,1)` with
  `steps=1`.

## BFS Construction

Wall-free reference count: `|D(s)| = 2s² + 2s + 1`
(s=1→5, s=2→13, s=3→25, s=4→41, s=5→61).

With walls, the BFS skips invalid cells automatically via
`grid.neighbors(cell)`, which already filters to valid neighbors. The
result is the connected component containing the center, which may be
strictly smaller than the geometric Manhattan ball if walls bisect it.

## Pickle

Light — only `map` (str), `name`, `_center` (CellMap), `_steps`, `_cells`
(list of CellMap) are persisted. The grid is **not** embedded. To
reconstruct from metadata downstream, rebuild via
`ClusterDiamond(grid=g, center=g[r][c], steps=s)` once the grid is
available.

## Usage

```python
from f_ds.grids import GridMap, ClusterDiamond

grid = GridMap(rows=10, cols=10)

# Deterministic, at a specific cell
c = ClusterDiamond.Factory.at_center(
    grid=grid, center=grid[5][5], steps=2)
print(len(c))    # 13
print(c)         # ClusterDiamond(center=(5, 5), steps=2, cells=13)

# Random, with a size floor
c = ClusterDiamond.Factory.random(
    grid=grid, min_cells=8, steps=2)
assert len(c) >= 8

# Walls are honored
grid.invalidate([grid[5][6]])
c = ClusterDiamond.Factory.at_center(
    grid=grid, center=grid[5][5], steps=1)
assert len(c) == 4   # one neighbor missing

# Hashable identity
c1 = ClusterDiamond.Factory.at_center(grid=grid, center=grid[5][5], steps=2)
c2 = ClusterDiamond.Factory.at_center(grid=grid, center=grid[5][5], steps=2)
assert c1 == c2
assert {c1, c2} == {c1}
```
