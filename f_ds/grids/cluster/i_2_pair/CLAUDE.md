# PairCluster

## Purpose
An **ordered pair of two `ClusterDiamond`s**, treated as a single
**value-record** — usable as a `set` member or `dict` key, e.g. to
enumerate start/goal cluster pairs for MOSPP / OMSPP problem instances.
Ordered: `(A, B) != (B, A)`. Concrete over `ClusterDiamond` (not generic
over `ClusterGrid`): a diamond always exposes a `center`, so `distance()`
is total and no center-Protocol guard is needed.

## Why `Tupleable`
`PairCluster` is a two-element value-record, so it composes `Tupleable`
(`Comparable + Hashable + HasRepr`) and implements the single
`to_tuple()` hook returning `(cluster_a, cluster_b)`. That one method
drives `==`, `hash`, `iter`, `[]`, `len` (and ordering) — no
hand-written `__eq__` / `__hash__` / `__iter__` / `__getitem__`.

### Ordering (`<`, `<=`, `>`, `>=`)
`Tupleable` exposes the comparison operators via `key < key`, and they
work as a **real total order**: `ClusterDiamond` is `Comparable` (its
`key = (map, center.key, steps)` is a totally-ordered tuple), so the
tuple comparison that recurses into the clusters resolves cleanly.
`pair1 < pair2` orders lexicographically by `(cluster_a, cluster_b)`.

## Public API

### Class

```python
class PairCluster(Tupleable)
```

### Constructor

```python
def __init__(self, cluster_a: ClusterDiamond, cluster_b: ClusterDiamond) -> None
```

### Properties

| Property | Type | Meaning |
|----------|------|---------|
| `cluster_a` | `ClusterDiamond` | first cluster |
| `cluster_b` | `ClusterDiamond` | second cluster |
| `key` | `tuple[ClusterDiamond, ClusterDiamond]` | inherited from `Tupleable` (`== to_tuple()`) — drives `__eq__` / `__hash__` |

### Methods

```python
def to_tuple(self) -> tuple[ClusterDiamond, ClusterDiamond]
```
The data-tuple `(cluster_a, cluster_b)` — the single hook `Tupleable`
delegates all record behaviour to.

```python
def distance(self) -> int
```
Manhattan distance between the two diamonds' **centers**, reusing
`CellMap.distance`. Total (every `ClusterDiamond` has a `center`). E.g.
the factory pair (centers `(2,2)` / `(7,7)`) → `10`.

### Dunder (all from `Tupleable`, via `to_tuple()`)
- `__eq__` / `__hash__` — equal / hash-equal iff both clusters are equal
  **and** in the same order.
- `__iter__` / `__getitem__` / `__len__` — `a, b = pair`, `pair[0]`,
  `len(pair) == 2`.
- `__lt__` / `__le__` / `__gt__` / `__ge__` — a real total order (see
  *Ordering*); `PairCluster`s are sortable.
- `__str__` → `'PairCluster(str_a, str_b)'` is **overridden** here
  (domain format). `__repr__` is **not** overridden — it comes from
  `HasRepr`, wrapping `__str__` as `'<PairCluster: PairCluster(…)>'`.

## Factory

```python
PairCluster.Factory.diamonds() -> PairCluster
```
Two deterministic `ClusterDiamond`s on a 10x10 `GridMap` (centers
`(2,2)` / `(7,7)`, `steps=2`).

```python
PairCluster.Factory.random_many(
    grid, many,
    steps_a=0, min_cells_a=1,
    steps_b=1, min_cells_b=1,
    min_dist=0, max_tries=100) -> list[PairCluster]
```
Sample two **distinct** pools of `ClusterDiamond`s on `grid` — up to
`many` "A" diamonds (`steps_a` / `min_cells_a`) and up to `many` "B"
diamonds (`steps_b` / `min_cells_b`) — and return every
`PairCluster(a, b)` whose `distance() >= min_dist` (the full **A × B
cross product**, so up to `many * many` pairs; `min_dist=0` keeps all).

- **Best-effort:** a grid that cannot supply `many` distinct diamonds of
  a side yields fewer — coverage degrades gracefully, no raise (unlike
  `ClusterDiamond.Factory.random_many`, which raises). Each side is
  drawn by the private `_sample_pool` helper (a lenient
  `ClusterDiamond.Factory.random` loop, de-duped by identity).
- **Randomness** is the **process-global** `random` module (each draw →
  `ClusterDiamond.Factory.random` → `grid.random.cells`); seed it before
  calling for a reproducible pool. `max_tries` bounds per-diamond center
  resampling on both sides.
- **Use case:** the OMSPP `goal_distance` s_2 samples a START pool
  (`steps_a=0`) × a GOAL pool (`steps_b=20, min_cells_b=200`) and bins
  the pairs by `distance()` into phase-diagram bands — this factory
  replaces the former two-stage `s_0`/`s_1` pool-CSV pipeline.

## Inheritance

```
Comparable ─┐
Hashable  ──┼── Tupleable (==, <, hash, iter, [], len via to_tuple())
HasRepr   ─┘        └── PairCluster   (to_tuple() = (cluster_a, cluster_b))
```

## Dependencies
- `f_core.mixins.Tupleable` — value-record behaviour via the abstract
  `to_tuple()`, which `PairCluster` implements as `(cluster_a, cluster_b)`.
- `f_ds.grids.cluster.ClusterDiamond` — the concrete cluster type
  (`Comparable + Hashable`, so it is both orderable and hashable); its
  `center` (a `CellMap`) and `CellMap.distance` back `distance()`.

## Usage

```python
from f_ds.grids import GridMap, ClusterDiamond, PairCluster

grid = GridMap(rows=10, cols=10)
a = ClusterDiamond(grid=grid, center=grid[2][2], steps=2)
b = ClusterDiamond(grid=grid, center=grid[7][7], steps=2)

pair = PairCluster(cluster_a=a, cluster_b=b)
assert pair != PairCluster(cluster_a=b, cluster_b=a)   # ordered
assert len({pair, PairCluster(cluster_a=a, cluster_b=b)}) == 1  # hashable

x, y = pair                 # __iter__ — unpacking
assert (x, y) == (a, b)
assert pair[0] is a         # __getitem__
assert pair.distance() == 10   # center-to-center Manhattan: (2,2)->(7,7)
assert sorted([pair]) == [pair]   # sortable (ClusterDiamond is Comparable)
```
