# Cluster (General Abstract Base)

## Purpose
Domain-agnostic abstract root of every cluster: a named collection of
members with an optional representative. Subclasses own their member
storage and implement `to_iterable()`.

```python
class Cluster(Generic[Item], Collectionable[Item], HasName, ABC)
```

## Public API

### Constructor
```python
def __init__(self, name: str = 'Cluster')
```
`name` is the cluster's identity / label (via `HasName`).

### Properties
| Property | Type | Meaning |
|----------|------|---------|
| `name` | `str` | identity / label (from `HasName`) |
| `members` | `list[Item]` | members as a list (a copy of `to_iterable()`) |
| `representative` | `Item \| None` | distinguished member; default `None`, override |

### Abstract
```python
def to_iterable(self) -> IterableSized[Item]   # subclass owns storage
```

### Free from `Collectionable`
`len()`, `in`, `iter()`, `bool()` — all dispatched through
`to_iterable()`. `__str__` → `'name(size=n)'`; `__repr__` →
`'<Cls: name=…, size=…>'`.

## Inheritance
```
Collection[Item], Sizable          HasRepr
 └── Collectionable[Item]           └── HasName
              └────────── Cluster (abstract) ──────────┘
                   └── f_ds.grids.cluster.Cluster[CellMap] → ClusterDiamond
```

## Notes
- Abstract → no `Factory`. Tested via a list-backed test double
  (`_ClusterList`) in `_tester.py`.
- `members` (not `items`): `items` is reserved in `f_ds` for mapping
  (key→value) views (`dual_indexable`, `indexable_key`).
- Deliberately minimal — no set algebra / merge / split / provenance at
  this stage.
