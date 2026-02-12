# Equatable

## Purpose
Mixin for objects that support equality checks (`==`, `!=`).
Subclasses implement a single abstract `key` property; `__eq__` delegates to comparing keys.
`__ne__` is omitted — Python derives `!=` from `__eq__` by default.

## Public API

### Class Attribute
```python
Factory: type | None = None
```
Factory for creating test instances. Wired via `__init__.py`.

### Abstract Property
```python
@property
@abstractmethod
def key(self) -> SupportsEquality:
```
Return the value used for equality comparison. Must be implemented by every subclass.
This single property also drives `__lt__` (via `Comparable`) and `__hash__` (via `Hashable`) downstream.

### Dunder Methods
```python
def __eq__(self, other: object) -> bool:
```
Returns `True` if `self.key == other.key`.
Returns `NotImplemented` if `other` is not an `Equatable`.
Short-circuits with `True` on identity (`other is self`).

## Inheritance (Hierarchy)

```
SupportsEquality (Protocol)
 └── Equatable
      ├── Comparable
      └── Hashable
```

| Base | Responsibility |
|------|----------------|
| `SupportsEquality` | Protocol defining the `__eq__` contract |

## Dependencies

| Import | Purpose |
|--------|---------|
| `abc.abstractmethod` | Marks `key` as abstract |
| `f_core.protocols.equality.main.SupportsEquality` | Protocol this class implements |

## Usage Examples

### Custom Subclass
```python
from f_core.mixins.equatable import Equatable

class Point(Equatable):
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    @property
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
