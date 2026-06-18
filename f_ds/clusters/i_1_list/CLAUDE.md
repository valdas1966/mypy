# ClusterList (Concrete — Explicit Members)

## Purpose
The default concrete `Cluster`: built from an explicit iterable of
members. Replaces the former `_ClusterList` test double — it is now a
real, shipped class.

```python
class ClusterList(ClusterBase[Item])
```

Use it when you already have the members in hand. For
computed-membership clusters (BFS shapes, etc.) subclass `ClusterBase`
directly instead (see `f_ds/grids/cluster/`).

## Public API

### Constructor
```python
def __init__(self,
             members: Iterable[Item],
             name: str = 'ClusterList',
             representative: Item | None = None) -> None
```
- `members` — stored as a `list` (order preserved; any `Item` type, no
  hashability required — that's why it is list-backed, not set-backed).
- `representative` — optional distinguished member. It **need not be a
  member** (a computed point such as a centroid may serve as it).

### Properties
| Property | Type | Source |
|----------|------|--------|
| `members` | `list[Item]` | base — a list copy of `to_iterable()` |
| `representative` | `Item \| None` | the value passed at construction |
| `name` | `str` | base (`HasName`) |

### Free from `ClusterBase` / `Collectionable`
`len()`, `in`, `iter()`, `bool()`; `__str__` → `'name(size=n[, rep=…])'`;
`__repr__` from `HasRepr` → `'<ClusterList: …>'`.

## Factory
```python
ClusterList.Factory.a()   # ClusterList([1,2,3], name='K', representative=1)
ClusterList.Factory.b()   # ClusterList([4,5], name='L')  — no representative
```

## Usage
```python
from f_ds.clusters import ClusterList

c = ClusterList(members=[1, 2, 3], name='K', representative=1)
len(c)             # 3
2 in c             # True
c.members          # [1, 2, 3]  (a copy)
c.representative   # 1
str(c)             # 'K(size=3, rep=1)'
```
