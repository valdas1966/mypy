# Tupleable

## Purpose
Mixin for **value-record** objects that are defined entirely by their
tuple — points, pairs, bounds, shapes. Subclasses implement a single
abstract `to_tuple()`; equality, ordering, hashing, iteration, indexing,
length and `str`/`repr` all derive from it.

It composes `Comparable`, `Hashable` and `HasRepr`, and supplies the
concrete `key` (= `to_tuple()`) that those bases need. So one method —
`to_tuple()` — gives a class the full tuple-like behaviour set.

**Immutability is a contract.** The tuple is the identity, so a
`Tupleable` must not mutate after construction — a changing tuple means a
changing hash, which corrupts any `set` / `dict` holding it.

Foreign operands are guarded via `Equatable` / `Comparable`: `obj == None`
is `False` and `obj < None` raises `TypeError` (never a leaky
`AttributeError`).

## Public API

### Class Attribute
```python
Factory: type | None = None
```
Factory for creating test instances. Wired via `__init__.py`.

### Abstract Method
```python
@abstractmethod
def to_tuple(self) -> tuple:
```
Return the object's data as a tuple. The single method every subclass
implements; everything else derives from it.

### Property
```python
@property
def key(self) -> tuple:
```
Returns `self.to_tuple()`. Satisfies the abstract `key` contract from
`Comparable` / `Hashable`, so identity = the tuple.

### Dunder Methods
```python
def __iter__(self) -> Iterator[Any]   # unpacking: a, b = obj
def __getitem__(self, index: int)     # indexing: obj[0]
def __len__(self) -> int              # len(obj) == len(to_tuple())
def __str__(self) -> str              # str(to_tuple()), e.g. '(1, 2)'
def __repr__(self) -> str             # from HasRepr: '<ClassName: (1, 2)>'
```

### Inherited
```python
def __eq__(self, other) -> bool   # Equatable — compares key (the tuple)
def __lt__ / __le__ / __gt__ / __ge__   # Comparable — lexicographic by tuple
def __hash__(self) -> int         # Hashable — hash(self.key)
```

## Inheritance (Hierarchy)

```
Equatable
 ├── Comparable (+ SupportsComparison)
 └── Hashable
HasRepr
     └── Tupleable(Comparable, Hashable, HasRepr)
          └── key = to_tuple()
```

| Base | Responsibility |
|------|----------------|
| `Comparable` | `__lt__`/`__le__`/`__gt__`/`__ge__` via `key` |
| `Hashable` | `__hash__` via `key` |
| `HasRepr` | standardized `__repr__` as `<ClassName: str(self)>` |

## Dependencies

| Import | Purpose |
|--------|---------|
| `f_core.mixins.comparable.Comparable` | Base — ordering operators |
| `f_core.mixins.hashable.Hashable` | Base — hashing |
| `f_core.mixins.has.repr.HasRepr` | Base — standardized repr |
| `abc.abstractmethod` | Marks `to_tuple` as abstract |
| `typing.Any`, `typing.Iterator` | Iteration / indexing annotations |

## Adopters

Value objects whose identity *is* their full tuple:

| Class | `to_tuple()` |
|-------|--------------|
| `f_ds.geometry.PointXY` | `(x, y)` |
| `f_ds.geometry.Bounds[T]` | `(top, left, bottom, right)` |

`HasRowCol` was migrated too — it is a positional value-record
(identity = `(row, col)`), so `class HasRowCol(Tupleable)`.

`HasRowsCols` is **deliberately not** a `Tupleable`: its consumers
(`Grid`, `Container`, `Range`) hold contents and must keep object
identity — value-equality by `(rows, cols)` would make different
same-shape objects equal/hash-equal. It stays a plain dimensions mixin.

## Usage Example

```python
from f_core.mixins.tupleable import Tupleable

class Coord(Tupleable):
    def __init__(self, x: int, y: int) -> None:
        self._x, self._y = x, y
    def to_tuple(self) -> tuple[int, int]:
        return self._x, self._y

c = Coord(1, 2)
x, y = c                 # (1, 2) — unpacking via __iter__
c[0]                     # 1
len(c)                   # 2
c == Coord(1, 2)         # True
c < Coord(1, 3)          # True (lexicographic)
len({c, Coord(1, 2)})    # 1 — equal tuples dedup
repr(c)                  # '<Coord: (1, 2)>'
```
