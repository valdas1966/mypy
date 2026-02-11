# Equatable

## Purpose

Mixin for objects that support equality checks. Implements the `SupportsEquality` protocol by delegating `__eq__` to a single abstract `key()` method that subclasses must implement.

`__ne__()` is omitted — Python derives `!=` from `__eq__` by default.

## Public API

### Class Attributes

```python
Factory: type | None = None
```
Factory class for creating test instances. Attached via `__init__.py`.

### Abstract Methods

```python
@abstractmethod
def key(self) -> SupportsEquality
```
Returns the value that represents this object for equality. Must be implemented by subclasses. The returned value drives `__eq__`, and downstream: `__lt__` (via `Comparable`) and `__hash__` (via `Hashable`).

### Dunder Methods

```python
def __eq__(self, other: object) -> bool
```
Returns `True` if `self.key() == other.key()`. Returns `NotImplemented` if `other` is not an `Equatable`. Short-circuits with `True` if `other is self`.

## Inheritance (Hierarchy)

```
SupportsEquality (Protocol)
 └── Equatable
```

| Base | Responsibility |
|------|----------------|
| `SupportsEquality` | Protocol defining `__eq__` contract |

**Direct subclasses:** `Comparable`, `Hashable`

## Dependencies

| Import | Purpose |
|--------|---------|
| `abc.abstractmethod` | Decorator for `key()` |
| `f_core.protocols.equality.main.SupportsEquality` | Protocol this class implements |

## Usage Examples

```python
from f_core.mixins.equatable import Equatable


class Point(Equatable):
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def key(self) -> tuple[int, int]:
        return (self.x, self.y)


Point(1, 2) == Point(1, 2)  # True
Point(1, 2) != Point(3, 4)  # True
```

### Using the Factory

```python
from f_core.mixins.equatable import Equatable

a = Equatable.Factory.a()  # Char('A')
b = Equatable.Factory.b()  # Char('B')

a == a  # True
a != b  # True
```
