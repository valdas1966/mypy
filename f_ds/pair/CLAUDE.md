# Pair

## Purpose
Generic, key-identified pair of two items of the same type. Supports an
**ordered** mode (identity is `(a, b)`) and an **unordered** mode
(identity is the sorted items, so `(a, b)` and `(b, a)` are equal). Used
directly and as the base of domain pairs (e.g. `PairCluster`).

## Public API

### Class

```python
class Pair(Hashable, Generic[Item])
```

### Constructor

```python
def __init__(self, a: Item, b: Item, is_ordered: bool = False) -> None
```

### Properties

| Property | Type | Meaning |
|----------|------|---------|
| `a` | `Item` | first item |
| `b` | `Item` | second item |
| `is_ordered` | `bool` | whether `(a, b)` differs from `(b, a)` |
| `key` | `tuple[Item, Item]` | identity — `(a, b)` if ordered, else `sorted(a, b)`; drives `__eq__`/`__hash__` |

### Dunder
- `__eq__` / `__hash__` — via `Hashable`, delegating to `key`. Two pairs
  are equal/hash-equal iff their `key`s match.
- `__str__` → `'(a, b)'`; `__repr__` → `'<Pair: (a, b)>'`.

### Item requirements
- **Ordered**: items must be hashable.
- **Unordered**: items must additionally be **sortable** (`key` calls
  `sorted`). For unsortable-but-hashable items, use ordered mode (or a
  subclass with a hash-based key).

## Factory

```python
Pair.Factory.ab_ordered()   -> Pair[str]   # ('a','b'), ordered
Pair.Factory.ab_unordered() -> Pair[str]   # ('a','b'), unordered
Pair.Factory.ba_ordered()   -> Pair[str]   # ('b','a'), ordered
Pair.Factory.ba_unordered() -> Pair[str]   # ('b','a'), unordered
```

## Inheritance

```
Hashable (eq + hash via key)   Generic[Item]
        └────────────┬─────────────┘
                   Pair
                     └── PairCluster(Pair[ClusterGrid])   (f_ds/grids/cluster/pair/)
```

## Dependencies
- `f_core.mixins.Hashable` — `__eq__` (via `Equatable`) + `__hash__`,
  both driven by the abstract `key` (here a concrete `@property`).

## Usage

```python
from f_ds.pair import Pair

p1 = Pair(a=1, b=2, is_ordered=True)
p2 = Pair(a=2, b=1, is_ordered=True)
assert p1 != p2                       # ordered: (1,2) != (2,1)

u1 = Pair(a=1, b=2)                    # unordered (default)
u2 = Pair(a=2, b=1)
assert u1 == u2 and {u1, u2} == {u1}   # sorted key: (1,2) == (1,2)
```
