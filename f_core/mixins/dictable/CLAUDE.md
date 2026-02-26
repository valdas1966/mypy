# Dictable

## Purpose

Generic mixin that wraps a `dict[K, V]` and exposes a dictionary-like public API. Provides key/value access, iteration, containment checks, update, and equality. Inherits size semantics (`__len__`, `__bool__`) from `Sizable`. Implements `__str__` directly (not via `Printable`).

## Public API

### Class Attributes

```python
Factory: type = None
```
Factory class for creating instances. Attached via `__init__.py`.

### Constructor

```python
def __init__(self, data: dict[K, V] = None) -> None
```
Stores `data` (or a new empty `dict`) as `_data`.

### Methods

```python
def keys(self) -> list[K]
```
Returns list of keys.

```python
def values(self) -> list[V]
```
Returns list of values.

```python
def items(self) -> list[tuple[K, V]]
```
Returns list of `(key, value)` tuples.

```python
def get(self, key: K, default: V = None) -> V | None
```
Returns value for `key`, or `default` if missing.

```python
def update(self, data: Self | dict[K, V]) -> None
```
Merges `data` into `_data`. Accepts a `dict` or another `Dictable`.

### Dunder Methods

```python
def __getitem__(self, key: K) -> V
```
`obj[key]` — raises `KeyError` if missing.

```python
def __setitem__(self, key: K, value: V) -> None
```
`obj[key] = value`.

```python
def __contains__(self, key: K) -> bool
```
`key in obj`.

```python
def __len__(self) -> int
```
`len(obj)` — satisfies `Sizable` contract.

```python
def __iter__(self) -> Iterator[K]
```
Iterates over keys.

```python
def __str__(self) -> str
```
Returns `str(self._data)`.

```python
def __eq__(self, other: object) -> bool
```
Compares `_data` dicts for equality. Returns `NotImplemented` for non-Dictable.

## Inheritance (Hierarchy)

```
Sized (collections.abc)
 └── Sizable (abstract __len__, provides __bool__)
      └── Dictable(Sizable, Generic[K, V])
```

| Base | Responsibility |
|------|----------------|
| `Sizable` | Abstract `__len__`, concrete `__bool__` |
| `Generic[K, V]` | Type parameterization for key/value types |

## Dependencies

| Import | Purpose |
|--------|---------|
| `typing.Generic`, `TypeVar`, `Iterator`, `Self` | Generics and type hints |
| `f_core.mixins.sizable.Sizable` | Base — size/bool semantics |

## Usage Example

```python
from f_core.mixins.dictable import Dictable

d = Dictable(data={'a': 1, 'b': 2, 'c': 3})
d['d'] = 4
print(d.keys())       # ['a', 'b', 'c', 'd']
print('a' in d)       # True
print(d.get('z', 0))  # 0
print(len(d))         # 4
```

### Using the Factory

```python
from f_core.mixins.dictable import Dictable

abc = Dictable.Factory.abc()  # {'a': 1, 'b': 2, 'c': 3}
print(abc.keys())             # ['a', 'b', 'c']
print(abc['b'])               # 2
```

## Power of Dictable over Plain dict

A plain `dict` is just data. `Dictable` is a **base class** that
gives dict-like access to domain objects while enabling subclassing,
mixin composition, polymorphic merging, and additional state.

### 1. Mixin Composition — Combine Dict with Other Behaviors

A plain `dict` can't also be `Validatable` or `HasName`. With
`Dictable`, you mix in any combination of capabilities:

```python
class SolutionsPath(Dictable[Node, Solution], Validatable):
    """
    Dict of Node->Solution that is also validatable.
    """
    def __init__(self, is_valid: bool,
                 sols: dict[Node, Solution]) -> None:
        Dictable.__init__(self, data=sols)
        Validatable.__init__(self, is_valid=is_valid)

sols = SolutionsPath(is_valid=True, sols={node_a: sol_a})
print(sols[node_a])     # dict-like access
print(sols.is_valid)    # Validatable behavior
print(bool(sols))       # Sizable: True (non-empty)
```

### 2. Domain-Specific State on Top of Dict Data

Subclasses can track additional attributes alongside the dict:

```python
class Boundary(Dictable[Node, int]):
    """
    Dict of Node->cost that also tracks which nodes changed.
    """
    def __init__(self) -> None:
        Dictable.__init__(self)
        self._changed: set[Node] = set()

    def add_changed(self, node: Node, depth: int) -> None:
        self._changed.add(node)

    @property
    def changed(self) -> set[Node]:
        return self._changed

b = Boundary()
b[node] = 5             # dict-like write
b.add_changed(node, 2)  # domain-specific tracking
print(b.changed)        # {node}
```

### 3. Polymorphic update() — Merge Dictable Instances

`update()` accepts both a plain `dict` and another `Dictable`.
Subclasses can override it to merge domain state, not just keys:

```python
class SolutionsPath(Dictable[Node, Solution], Validatable):

    def update(self, other: SolutionsPath) -> None:
        # Merge aggregate stats
        self._elapsed += other.elapsed
        self._generated += other.generated
        # Merge the dict data
        for node, sol in other.items():
            self[node] = sol

# Two independent search results merged into one
sols_left.update(sols_right)
print(sols_left.elapsed)  # combined elapsed time
print(len(sols_left))     # combined solution count
```

### 4. Domain Factory Methods

Subclasses can provide `@classmethod` factories that construct
the Dictable from domain-specific inputs:

```python
class Cache(Dictable[Node, Path]):

    @classmethod
    def from_path(cls, path: Path) -> Cache:
        data = {node: path.sub(node) for node in path}
        return cls(data=data)

    @classmethod
    def from_explored(cls, explored: set[Node]) -> Cache:
        data = {n: Path() for n in explored}
        return cls(data=data)

cache = Cache.from_path(path)   # build from search path
cache.update(other_cache)       # merge another Cache
print(cache[node])              # dict-like lookup
```

### 5. Type-Safe Specialization with Generics

Plain `dict` loses semantic meaning. `Dictable[K, V]` subclasses
constrain key/value types for clarity and type-checking:

```python
class Cache(Dictable[Node, Path]):  ...
class Boundary(Dictable[Node, int]):  ...
class GraphDict(Dictable[Key, Node], GraphBase[Node]):  ...
```

### Summary

| Capability | Plain `dict` | `Dictable` subclass |
|---|---|---|
| Key/value access | Yes | Yes |
| Mixin composition | No | Yes |
| Additional state | No | Yes |
| Polymorphic merge | No | Yes |
| Domain factories | No | Yes |
| Type-safe generics | No | Yes |
| `__bool__` via Sizable | No | Yes |
| `__eq__` on wrapped data | No | Yes |
