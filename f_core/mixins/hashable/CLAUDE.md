# Hashable

## Purpose

Mixin for objects that support hashing. Extends `Equatable` and implements `__hash__` by delegating to the inherited `key()` method. Ensures that objects with equal keys produce equal hashes, maintaining the Python invariant `a == b` implies `hash(a) == hash(b)`.

## Public API

### Class Attributes

```python
Factory: type | None = None
```
Factory class for creating test instances. Attached via `__init__.py`.

### Dunder Methods

```python
def __hash__(self) -> int
```
Returns `hash(self.key())`. The `key()` value must be hashable (i.e., immutable).

### Inherited from Equatable

```python
@abstractmethod
def key(self) -> SupportsEquality
```

```python
def __eq__(self, other: object) -> bool
```

## Inheritance (Hierarchy)

```
SupportsEquality (Protocol)
 └── Equatable
      └── Hashable
```

| Base | Responsibility |
|------|----------------|
| `SupportsEquality` | Protocol defining `__eq__` contract |
| `Equatable` | Provides `__eq__` and abstract `key()` |

## Dependencies

| Import | Purpose |
|--------|---------|
| `f_core.mixins.equatable.Equatable` | Base class providing `key()` and `__eq__` |

## Usage Examples

```python
from f_core.mixins.hashable import Hashable


class Tag(Hashable):
    def __init__(self, name: str):
        self.name = name

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

a = Hashable.Factory.a()  # Char('A')
b = Hashable.Factory.b()  # Char('B')

{a, a, b} == {a, b}  # True
```
