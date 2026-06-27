# Group

## Purpose
A **named list** — a `UserList` of items that also carries a name and is
ordered/compared by `(name, data)`. Adds grouping utilities on top of a
plain list: filtering, sampling, moving, distributing into sub-groups,
union, and random access.

## Public API

### Construction
```python
Group(data: Sequence[Item] = None, name: str = 'Group') -> None
```
Wraps `data` in a list and labels it `name`.

### Identity
```python
@property
def key(self) -> tuple[str, list[Item]]   # (name, data)
```
Identity = `(name, data)`. Equality and ordering (from `Comparable`)
compare **first by name, then by data**. Groups are not hashable (they
hold mutable data — `Comparable` defines `__eq__` without `__hash__`).

### List utilities
```python
@property
def random(self) -> Random                         # random-access helper
def filter(predicate, name=None) -> Group[Item]    # items meeting predicate
def sample(size=None, pct=None, name=None,
           preserve_order=False) -> Group[Item]     # random sub-sample
def move(item: Item, index: int) -> None           # reposition an item
def distribute(n: int) -> list[Group[Item]]        # split into n groups
def display() -> None                              # print items, one per row
def __iadd__(other: list[Item]) -> Group[Item]     # extend with a list
def __str__(self) -> str                           # 'Name[items...]'
```

### Class methods
```python
@classmethod union(name, groups) -> Group[Item]            # merge groups
@classmethod to_groups(data, n, name=None) -> list[Group]  # split data into n
```

### Factory
```python
Group.Factory.ab() -> Group[str]     # Group(['a', 'b'], name='AB')
```

## Inheritance (Hierarchy)
```
HasName        — name label + str()/repr() (no identity of its own)
Comparable     — __eq__/__lt__/__le__/__gt__/__ge__ via key
UserList[Item] — list storage + list protocol
   └── Group(HasName, Comparable, UserList[Item])
```
`Comparable` precedes `UserList` in the MRO, so comparison uses
`key=(name, data)` rather than `UserList`'s data-only comparison.

## Dependencies
| Import | Purpose |
|--------|---------|
| `collections.UserList` | List storage + protocol |
| `f_core.mixins.has.name.HasName` | Name label |
| `f_core.mixins.comparable.Comparable` | Ordering / equality via `key` |
| `f_ds.groups._random.Random` | Random-access helper |
| `f_utils.dtypes.u_seq.USeq` | `filter` / `sample` sequence ops |

## Usage Example
```python
from f_ds.groups.main import Group

g = Group(data=[3, 1, 2], name='nums')
g += [4]                       # extend
parts = g.distribute(n=2)      # [Group[3,1], Group[2,4]]
evens = g.filter(lambda x: x % 2 == 0)

Group(name='A', data=[1, 2]) == Group(name='A', data=[1, 2])   # True
Group(name='A', data=[1]) < Group(name='B', data=[1])          # True (A < B)
```
