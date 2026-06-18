# Clusters Package

## Purpose
The **general, domain-agnostic** `Cluster` abstraction for `f_ds`. A
cluster is a *named collection of members* that belong together, which
may expose a single `representative` member (centroid / medoid / seed /
center).

- `ClusterBase` — the abstract root that every cluster extends.
- `ClusterList` — the default concrete cluster (members supplied
  explicitly).

Domain-specific clusters extend `ClusterBase` elsewhere — e.g. the grid
clusters in `f_ds/grids/cluster/` (`ClusterBase[CellMap]`,
`ClusterDiamond`).

## Scope (intentionally minimal)
Current surface is deliberately small (YAGNI): identity + members +
representative. **No** set algebra / `merge` / `split` / provenance yet —
those are added only when a concrete need appears.

## Where it sits among the f_ds containers

| Container | Semantics | Element accessor |
|-----------|-----------|------------------|
| `Group` | ordered named list (dups OK) | `.data` (UserList) |
| `SetOrdered` | unordered unique set | the set itself |
| **`ClusterBase`** | named members + representative (abstract) | `.members` / `to_iterable()` |
| **`ClusterList`** | the above, members given explicitly | `.members` |

## Package Exports

```python
from f_ds.clusters import ClusterBase     # abstract base
from f_ds.clusters import ClusterList     # concrete (explicit members)
```

## Module Hierarchy

```
f_ds/clusters/
├── __init__.py          lazy re-export (ULazy)
├── i_0_base/            abstract ClusterBase
│   ├── main.py
│   └── __init__.py      (no _tester.py — abstract)
└── i_1_list/            concrete ClusterList (explicit members)
    ├── main.py
    ├── _factory.py
    ├── _tester.py
    └── __init__.py
```

## Design Notes

- Composes `Collectionable[Item]` (`len`/`in`/`iter`/`bool` from
  `to_iterable()`) and `HasName` (identity / label).
- **Storage is abstract on the base**: subclasses own their members and
  implement `to_iterable()`. `ClusterBase` never holds the member
  container itself — `ClusterList` does (a plain list).
- `members` is the public read accessor (a list copy of `to_iterable()`);
  `to_iterable()` is the low-level contract (mirrors how the grid
  `Cluster` exposes `cells`).
- `representative` defaults to `None`; concrete classes with a
  distinguished member override it (`ClusterList` takes it as a
  constructor arg; the grid `ClusterDiamond` returns its center).
- Accessor is named `members` (not `items`) — `items` is the Python
  *Mapping* term for key→value pairs (`dict.items()`, `Dictable.items()`);
  a flat collection uses iteration + a domain noun.
