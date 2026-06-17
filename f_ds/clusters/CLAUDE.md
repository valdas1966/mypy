# Clusters Package

## Purpose
The **general, domain-agnostic** `Cluster` abstraction for `f_ds`. A
`Cluster` is a *named collection of members* that belong together, which
may expose a single `representative` member (centroid / medoid / seed /
center).

It is the abstract root that domain-specific clusters extend — e.g. the
grid clusters in `f_ds/grids/cluster/` (`Cluster[CellMap]`,
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
| **`Cluster`** | named members + representative | `.members` / `to_iterable()` |

## Package Exports

```python
from f_ds.clusters import Cluster        # abstract base
```

## Module Hierarchy

```
f_ds/clusters/
├── __init__.py          lazy re-export (ULazy)
└── i_0_base/            abstract Cluster
    ├── main.py
    ├── _tester.py       (via a list-backed test double)
    └── __init__.py
```

## Design Notes

- Composes `Collectionable[Item]` (`len`/`in`/`iter`/`bool` from
  `to_iterable()`) and `HasName` (identity / label).
- **Storage is abstract**: subclasses own their members and implement
  `to_iterable()`. The base never holds the member container itself.
- `members` is the public read accessor (a list copy of `to_iterable()`);
  `to_iterable()` is the low-level contract (mirrors how the grid
  `Cluster` exposes `cells`).
- `representative` defaults to `None`; subclasses with a distinguished
  member override it.
- Accessor is named `members` (not `items`) — `items` is already used in
  `f_ds` for mapping (key→value) views (`dual_indexable`, `indexable_key`).
