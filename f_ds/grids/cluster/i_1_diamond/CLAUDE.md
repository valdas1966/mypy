# ClusterDiamond

## Purpose
Diamond-shaped (Manhattan-ball) cluster of valid cells on a `GridMap`.
Built via BFS from a center cell to depth `steps`, skipping walls —
returns only the connected component containing the center.

Inherits `ClusterGrid` (light: holds `map: str`, not the grid),
`Comparable` (total order via `key`) and `Hashable` (eq + hash via
`key`).

## Public API

### Constructor

```python
def __init__(self,
             grid: GridMap,
             center: CellMap,
             steps: int,
             name: str = 'ClusterDiamond') -> None
```
The `grid` is consumed by `_build` and **not** retained on `self`. The
`name` (default `'ClusterDiamond'`) is passed through to `ClusterGrid`
and feeds `__str__` / the inherited `HasName` string forms.

### Properties

| Property | Type | Meaning |
|----------|------|---------|
| `center` | `CellMap` | center of the diamond |
| `steps` | `int` | Manhattan radius |
| `key` | `tuple[str, tuple[int,int], int]` | `(map, center.key, steps)` — drives `__eq__` / `__lt__…` / `__hash__` |
| `map`, `name`, `cells` | — | inherited from `ClusterGrid` |

### String forms
- `__str__` → `name(center=(r,c), steps=s, cells=n)` (defined here; uses
  the instance `name`, default `'ClusterDiamond'`)
- `__repr__` → from `HasRepr`: `<ClusterDiamond: …>` wrapping the custom
  `__str__` (`ClusterGrid` no longer defines `__repr__`)

### Identity & ordering (via `Comparable` + `Hashable`)
`__eq__` / `__hash__` and the ordering operators (`__lt__` / `__le__` /
`__gt__` / `__ge__`) all come from `f_core.mixins` (`Comparable`,
`Hashable`), every one delegating to `key = (map, center.key, steps)`.
Two diamonds with the same `(map, center, steps)` are equal and hash the
same; differing on any field (including map name) makes them distinct.
`key` is a totally-ordered tuple, so diamonds **sort** (lexicographically
by map name, then center, then steps). Usable in `set` / `dict` and as
sort keys — which is what lets a `PairCluster` of diamonds order.

### Collection behavior (inherited from `Collectionable`)

```python
len(cluster)      # number of valid cells
cell in cluster   # membership test
list(cluster)     # iteration
bool(cluster)     # True iff non-empty
```

## Factory

The Factory holds the random samplers (`random`, `random_many`). For a
deterministic diamond at a known cell, call the constructor directly —
`ClusterDiamond(grid=..., center=..., steps=...)` — there is no
`at_center` wrapper.

```python
ClusterDiamond.Factory.random(grid, min_cells, steps,
                              max_tries=100) -> ClusterDiamond
ClusterDiamond.Factory.random_many(grid, many, steps,
                                   min_cells=1,
                                   max_tries=100) -> list[ClusterDiamond]
```

- `random(...)` samples a center via `grid.random.cells(size=1)` and retries
  until `|cluster| >= min_cells`. Raises `ValueError` after `max_tries`.
- `random_many(...)` accumulates `random(...)` draws into a `set` until
  `many` **distinct** diamonds are collected, then returns them as a
  `list`. De-duplication is by Hashable identity (same center, since
  `grid` and `steps` are fixed), so clusters may overlap but none
  repeats; order is unspecified (set-derived). Bounded to `many *
  max_tries` draws — raises `ValueError` if that many distinct diamonds
  can't be collected (e.g. `many` exceeds the valid cells yielding
  `>= min_cells`).

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

# Deterministic, at a specific cell — call the constructor directly
c = ClusterDiamond(grid=grid, center=grid[5][5], steps=2)
print(len(c))    # 13
print(c)         # ClusterDiamond(center=(5, 5), steps=2, cells=13)

# Random, with a size floor
c = ClusterDiamond.Factory.random(
    grid=grid, min_cells=8, steps=2)
assert len(c) >= 8

# Walls are honored
grid.invalidate([grid[5][6]])
c = ClusterDiamond(grid=grid, center=grid[5][5], steps=1)
assert len(c) == 4   # one neighbor missing

# Hashable identity
c1 = ClusterDiamond(grid=grid, center=grid[5][5], steps=2)
c2 = ClusterDiamond(grid=grid, center=grid[5][5], steps=2)
assert c1 == c2
assert {c1, c2} == {c1}
```
