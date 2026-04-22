# PairCluster

## Purpose

Pair of `Cluster`s (A, B) on a `GridMap` with a Manhattan
distance between their centers. Designed for CC-MMSPP experimental
instance generation: sample two disjoint clusters that are a known
distance apart.

## Public API

### Class

```python
class PairCluster(Generic[T])
# where T: TypeVar(bound=Cluster)
```

Parameterised over the cluster type, so
`PairCluster[ClusterDiamond]` preserves shape information.

### Constructor

```python
def __init__(self,
             a: T,
             b: T,
             name: str = 'PairCluster') -> None
```

### Properties

| Property | Type | Meaning |
|----------|------|---------|
| `a` | `T` (Cluster) | first cluster |
| `b` | `T` (Cluster) | second cluster |
| `name` | `str` | pair label |
| `distance` | `int` | Manhattan distance `a.center` ↔ `b.center` |

### Dunder

- `__str__` — `'PairCluster(a=..., b=..., distance=d)'`.
- `__repr__` — `'<PairCluster: a=..., b=..., distance=d>'`.

## Factory

```python
PairCluster.Factory.of_diamonds(grid, center_a, center_b,
                                steps_a, steps_b)
    -> PairCluster[ClusterDiamond]

PairCluster.Factory.random(grid, min_cells_a, min_cells_b,
                           steps_a, steps_b,
                           min_distance, max_tries=100)
    -> PairCluster[ClusterDiamond]

PairCluster.Factory.a() -> PairCluster[ClusterDiamond]
```

- `of_diamonds(...)` — deterministic: two diamonds at the given
  centers with independent Manhattan radii (`steps_a`, `steps_b`).
- `random(...)` — samples two disjoint diamonds with
  `|center_a - center_b| >= min_distance`, `|A| >= min_cells_a`,
  `|B| >= min_cells_b`, and independent `steps_a` / `steps_b`;
  raises `ValueError` after `max_tries`.
- `a()` — canonical 8×8 grid, centres `(1,1)` and `(6,6)`,
  `steps_a = steps_b = 1`; distance = 10.

## Contract on `Cluster.center`

`PairCluster.distance` depends on `self._a.center.distance(other=self._b.center)`.
`Cluster.center` is declared `@abstractmethod` — every concrete cluster
(e.g. `ClusterDiamond`) must expose it. Shape-free clusters that want
to avoid a center concept cannot participate in `PairCluster`.

## Usage

```python
from f_ds.grids import GridMap, PairCluster, ClusterDiamond

grid = GridMap(rows=20, cols=20)

# Random, two disjoint diamonds
pair = PairCluster.Factory.random(
    grid=grid, min_cells=8, steps=2, min_distance=10)
print(pair.distance)     # >= 10
print(pair.a)            # ClusterDiamond(...)
print(pair.b)            # ClusterDiamond(...)

# Deterministic
pair = PairCluster.Factory.of_diamonds(
    grid=grid,
    center_a=grid[2][2],
    center_b=grid[17][17],
    steps=2)
assert pair.distance == 30
```
