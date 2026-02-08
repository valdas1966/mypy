# Equable

## Purpose

Mixin for objects that support equality checks. Implements the `SupportsEquality` protocol by delegating `==` to a single `key_comparison()` method that subclasses must implement.

Note: `__ne__()` is omitted because Python automatically implements it as `not self == other`.

## Public API

### Class Attributes

```python
Factory: type | None = None
```
Factory class for creating instances. Attached via `__init__.py`.

### Abstract Methods

```python
@abstractmethod
def key_comparison(self) -> SupportsEquality
```
Returns the key used for equality comparison. Must be implemented by subclasses.

### Dunder Methods

```python
def __eq__(self, other: object) -> bool
```
Returns `True` if `self.key_comparison() == other.key_comparison()`. Returns `NotImplemented` if `other` is not an `Equable`.

## Inheritance (Hierarchy)

```
SupportsEquality (Protocol)
 └── Equable
```

| Base | Responsibility |
|------|----------------|
| `SupportsEquality` | Protocol defining `__eq__` contract |

**Direct subclass:** `Comparable` (`f_core.mixins.comparable`)

## Dependencies

| Import | Purpose |
|--------|---------|
| `abc.abstractmethod` | Decorator for `key_comparison()` |
| `f_core.protocols.equality.SupportsEquality` | Protocol this class implements |

## Usage Example

```python
from f_core.mixins.equatable import Equatable


class Point(Equatable):
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def key_comparison(self) -> tuple[int, int]:
        return (self.x, self.y)


p1 = Point(1, 2)
p2 = Point(1, 2)
p3 = Point(3, 4)

p1 == p2  # True
p1 != p3  # True
```

### Using the Factory

```python
from f_core.mixins.equatable import Equatable

a = Equatable.Factory.a()  # Char('A')
b = Equatable.Factory.b()  # Char('B')

a == a  # True
a != b  # True
```
