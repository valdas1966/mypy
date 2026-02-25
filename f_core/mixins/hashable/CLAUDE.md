# Hashable

## Purpose

Mixin for objects that support hashing. Extends `Equatable` and implements `__hash__` by delegating to the inherited abstract `key` property.
Maintains the Python invariant: `a == b` implies `hash(a) == hash(b)`, since both `__eq__` and `__hash__` delegate to the same `key` value.

## Public API

### Class Attribute

```python
Factory: type | None = None
```
Factory for creating test instances. Wired via `__init__.py`.

### Dunder Methods

```python
def __hash__(self) -> int
```
Returns `hash(self.key)`. The `key` value must be hashable (i.e., immutable).

### Inherited from Equatable

```python
@property
@abstractmethod
def key(self) -> SupportsEquality
```
Abstract — must be implemented by every subclass. Drives both `__eq__` (inherited from `Equatable`) and `__hash__` (this class).

```python
def __eq__(self, other: object) -> bool
```
Equality via `key`. Raises `AttributeError` if `other` has no `key` property.

## Inheritance (Hierarchy)

```
SupportsEquality (Protocol)
 └── Equatable
      └── Hashable
```

| Base | Responsibility |
|------|----------------|
| `SupportsEquality` | Protocol defining `__eq__` contract |
| `Equatable` | Provides `__eq__` and abstract `key` property |

## Dependencies

| Import | Purpose |
|--------|---------|
| `f_core.mixins.equatable.Equatable` | Base class providing `key` property and `__eq__` |

## Usage Examples

### Custom Subclass

```python
from f_core.mixins.hashable import Hashable


class Tag(Hashable):
    def __init__(self, name: str) -> None:
        self.name = name

    @property
    def key(self) -> str:
        return self.name


a = Tag("python")
b = Tag("python")

a == b              # True (from Equatable)
hash(a) == hash(b)  # True
{a, a, b}           # {Tag("python")} — deduplication works
```

### Using the Factory

```python
from f_core.mixins.hashable import Hashable

a = Hashable.Factory.a()       # Char('A')
b = Hashable.Factory.b()       # Char('B')
a_other = Hashable.Factory.a() # distinct instance, same key

assert a == a_other
assert hash(a) == hash(a_other)
assert {a, a_other, b} == {a, b}
```
