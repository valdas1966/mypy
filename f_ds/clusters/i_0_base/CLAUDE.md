# ClusterBase (General Abstract Base)

## Purpose
Domain-agnostic abstract root of every cluster: a named collection of
members with an optional representative. Subclasses own their member
storage and implement `to_iterable()`.

```python
class ClusterBase(Generic[Item], Collectionable[Item], HasName, ABC)
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
`to_iterable()`.

### String forms
- `__str__` → `'name(size=n)'`, plus `', rep=…'` when `representative`
  is not `None` (e.g. `'K(size=3, rep=1)'`).
- `__repr__` is **not** defined here — it comes from `HasRepr` (via
  `HasName`) and wraps `__str__` as `'<Cls: str>'`
  (e.g. `'<ClusterList: K(size=3, rep=1)>'`).

## Inheritance
```
Collection[Item], Sizable          HasRepr
 └── Collectionable[Item]           └── HasName
              └────────── ClusterBase (abstract) ──────────┘
                   ├── ClusterList                       (i_1_list — explicit members)
                   └── f_ds.grids.cluster.ClusterBase[CellMap] → ClusterDiamond
```

## Notes
- Abstract → no `Factory` and **no `_tester.py`**. The behaviour is
  exercised through the concrete `ClusterList` (`../i_1_list/`), which
  replaced the former `_ClusterList` test double.
- `members` (not `items`): `items` is the Python *Mapping* term for
  key→value pairs (`dict.items()`, `Dictable.items()`); a flat
  collection uses iteration + a domain noun (`members`).
- Deliberately minimal — no set algebra / merge / split / provenance at
  this stage.
