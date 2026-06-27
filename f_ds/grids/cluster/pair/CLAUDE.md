# PairCluster

## Purpose
An **ordered pair of two clusters**, treated as a single **hashable**
component — usable as a `set` member or `dict` key, e.g. to enumerate
start/goal cluster pairs for MOSPP / OMSPP problem instances. Ordered:
`(A, B) != (B, A)`. Generic over the cluster shape (`PairCluster[Cluster]`,
`Cluster` bound to `ClusterGrid`), so it pairs diamonds or any future
shape.

## Why `Hashable`, not `Tupleable`
`ClusterGrid` is `Hashable` (value-equality via its metadata `key`) but
**not `Comparable`**. `Tupleable` bundles `Comparable`, whose `<` would
`TypeError` on clusters at runtime — broken behaviour for no gain. The
requirement is only `eq + hash`, which is exactly what the `Hashable`
mixin supplies via a single `key`. Identity composes the two clusters'
own keys, so a `PairCluster` is value-equal iff both clusters are.

## Public API

### Class

```python
class PairCluster(Hashable, Generic[Cluster])   # Cluster bound=ClusterGrid
```

### Constructor

```python
def __init__(self, cluster_a: Cluster, cluster_b: Cluster) -> None
```

### Properties

| Property | Type | Meaning |
|----------|------|---------|
| `cluster_a` | `Cluster` | first cluster |
| `cluster_b` | `Cluster` | second cluster |
| `key` | `tuple[Cluster, Cluster]` | `(cluster_a, cluster_b)` — drives `__eq__` / `__hash__` |

### Dunder
- `__eq__` / `__hash__` — via `Hashable`, delegating to `key`. Equal /
  hash-equal iff both clusters are equal **and** in the same order.
- `__str__` → `'PairCluster(str_a, str_b)'` (each cluster via `str`).
- `__repr__` → `'<PairCluster: repr_a | repr_b>'` (each via `repr`).

### Item requirements
- Clusters must be **hashable** (the `key` tuple is hashed) — every
  concrete `ClusterGrid` (e.g. `ClusterDiamond`) is. Ordering is **not**
  required (and not provided).

## Factory

```python
PairCluster.Factory.diamonds() -> PairCluster[ClusterDiamond]
```
Two deterministic `ClusterDiamond`s on a 10x10 `GridMap` (centers
`(2,2)` / `(7,7)`, `steps=2`).

## Inheritance

```
Equatable ── Hashable (eq + hash via key)      Generic[Cluster]
        └───────────────────┬───────────────────────┘
                       PairCluster   (key = (cluster_a, cluster_b))
```

## Dependencies
- `f_core.mixins.Hashable` — `__eq__` / `__hash__` via the abstract
  `key`, which `PairCluster` implements as `(cluster_a, cluster_b)`.
- `f_ds.grids.cluster.ClusterGrid` — the bound on the `Cluster` type var.

## Usage

```python
from f_ds.grids import GridMap, ClusterDiamond, PairCluster

grid = GridMap(rows=10, cols=10)
a = ClusterDiamond(grid=grid, center=grid[2][2], steps=2)
b = ClusterDiamond(grid=grid, center=grid[7][7], steps=2)

pair = PairCluster(cluster_a=a, cluster_b=b)
assert pair != PairCluster(cluster_a=b, cluster_b=a)   # ordered
assert len({pair, PairCluster(cluster_a=a, cluster_b=b)}) == 1  # hashable
```
