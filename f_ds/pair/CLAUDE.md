# Pair

## Purpose
Generic, **ordered**, **heterogeneous** pair: the two slots may differ in
type (`Pair[First, Second]`). Identity is `(first, second)`, so
`(first, second) != (second, first)`. A thin value-record over
`Tupleable`; general-purpose, not tied to any domain. (An unordered mode
was removed
2026-06-24 — broken on disk and unused; re-add via a `frozenset`/hash key
that works for `Hashable`-only items if ever needed.)

## Public API

### Class

```python
class Pair(Tupleable, Generic[First, Second])
```

### Constructor

```python
def __init__(self, first: First, second: Second) -> None
```

### Properties

| Property | Type | Meaning |
|----------|------|---------|
| `first` | `First` | first item |
| `second` | `Second` | second item |

`key` is inherited from `Tupleable` (`key == to_tuple() == (first,
second)`) — not defined on `Pair`.

### Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `to_tuple()` | `tuple[First, Second]` | the pair as `(first, second)` — the single `Tupleable` method; drives identity, ordering and iteration. Shared accessor with `Point.to_tuple()` / `HasRowCol.to_tuple()` |

### Dunder
- `__eq__` / `__lt__` / `__hash__` — via `Tupleable`, delegating to the
  `(first, second)` tuple. Equal/hash-equal iff their tuples match.
- `__iter__` / `__getitem__` / `__len__` — via `Tupleable`: `x, y = pair`,
  `pair[0]`, `len(pair) == 2`.
- `__str__` → `str((first, second))`; `__repr__` → `'<Pair: (1, 2)>'`
  (from `HasRepr`; uses the live class name).

### Item requirements
- Items must be **hashable** (the tuple `(first, second)` is hashed). Comparing
  pairs with `<` additionally requires items to be **comparable** (lazy —
  only when `<` is actually used).

## Factory

```python
Pair.Factory.ab()   -> Pair[str, str]   # ('a', 'b')
Pair.Factory.ba()   -> Pair[str, str]   # ('b', 'a')
```

## Inheritance

```
Tupleable (eq + order + hash + iter via to_tuple)   Generic[First, Second]
        └────────────────────────┬───────────────────────────┘
                               Pair   (to_tuple() = (first, second))
```

## Dependencies
- `f_core.mixins.Tupleable` — `__eq__`/`__lt__`/`__hash__` plus
  `__iter__`/`__getitem__`/`__len__`, all driven by the concrete
  `to_tuple()` (which supplies `Tupleable`'s `key`).

## Usage

```python
from f_ds.pair import Pair

p1 = Pair(first=1, second=2)
p2 = Pair(first=2, second=1)
assert p1 != p2                       # ordered: (1,2) != (2,1)
assert len({p1, p2, Pair(first=1, second=2)}) == 2   # hashable: dedups on key

kv = Pair(first='score', second=42)   # heterogeneous: Pair[str, int]
assert kv.first == 'score' and kv.second == 42
```
