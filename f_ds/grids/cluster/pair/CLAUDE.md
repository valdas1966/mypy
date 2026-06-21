# PairCluster

## Purpose

Pair of `ClusterGrid`s (A, B) on a `GridMap` with a Manhattan
distance between their centers. Designed for CC-MMSPP experimental
instance generation: sample two disjoint clusters that are a known
distance apart.

## Public API

### Class

```python
class PairCluster(Pair[T])
# where T: TypeVar(bound=ClusterGrid)
```

An **ordered** `Pair` of clusters (identity `(A, B)`), parameterised over
the cluster type so `PairCluster[ClusterDiamond]` preserves shape
information. `a`/`b`/`is_ordered`/`key` and `__eq__`/`__hash__` are
inherited from [`Pair`](../../../pair/CLAUDE.md); `PairCluster` adds
`distance` and the cluster-flavoured `__str__`/`__repr__`.

### Constructor

```python
def __init__(self, a: T, b: T) -> None     # ordered Pair (is_ordered=True)
```

### Properties

| Property | Type | Meaning |
|----------|------|---------|
| `a` | `T` (ClusterGrid) | first cluster (from `Pair`) |
| `b` | `T` (ClusterGrid) | second cluster (from `Pair`) |
| `is_ordered` | `bool` | always `True` (from `Pair`) |
| `key` | `tuple[T, T]` | `(a, b)` — identity / hash (from `Pair`) |
| `distance` | `int` | Manhattan distance `a.center` ↔ `b.center` (this class) |

### Dunder

- `__str__` — `'PairCluster(a=..., b=..., distance=d)'`.
- `__repr__` — `'<PairCluster: map=X, a.center=.., b.center=.., distance=d>'`.
- `__eq__` / `__hash__` — inherited from `Pair` (ordered identity `(a, b)`),
  so `PairCluster` is usable in `set`/`dict`.

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

## Inheritance

```
Hashable   Generic[Item]
   └─────┬─────┘
     Pair[Item]                     (f_ds/pair/)
       └── PairCluster(Pair[T])     T bound=ClusterGrid, ordered
```

## Contract on `ClusterGrid.center`

`PairCluster.distance` calls `self.a.center.distance(other=self.b.center)`.
`ClusterGrid` has no `center` of its own; concrete shapes with a natural
center (e.g. `ClusterDiamond`) provide it. **Both** clusters in a pair
must expose a `center` — pairing a shape-free cluster raises
`AttributeError` at `distance` time.

## No `to_analytics()`
For structured CSV / dataframe export, build the row dict from the
pair's components inline (the script that owns the grid has it in
scope). `__repr__` carries the headline identity; the full structured
view is the script's responsibility.

## Usage

```python
from f_ds.grids import GridMap, PairCluster, ClusterDiamond

grid = GridMap(rows=20, cols=20)

# Random, two disjoint diamonds
pair = PairCluster.Factory.random(
    grid=grid, min_cells_a=8, min_cells_b=8,
    steps_a=2, steps_b=2, min_distance=10)
print(pair.distance)     # >= 10
print(pair.a)            # ClusterDiamond(...)
print(pair.b)            # ClusterDiamond(...)

# Deterministic
pair = PairCluster.Factory.of_diamonds(
    grid=grid,
    center_a=grid[2][2],
    center_b=grid[17][17],
    steps_a=2,
    steps_b=2)
assert pair.distance == 30
```
