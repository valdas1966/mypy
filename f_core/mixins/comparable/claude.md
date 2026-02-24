# Comparable

## Purpose
Mixin for objects that support comparison operations (`<`, `<=`, `>`, `>=`).
Extends `Equatable` and implements `SupportsComparison` by delegating
all comparison operators to a single abstract `key` property.
All four operators are explicitly implemented for performance — no
`@total_ordering` overhead.

No type guards — comparing incompatible types raises `AttributeError`.
This is intentional; cross-type comparison is a bug in this framework.

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
def key(self) -> SupportsComparison:
```
Return the value used for comparison and equality.
Must be implemented by every subclass.
Drives `__lt__`, `__le__`, `__gt__`, `__ge__` (this class),
`__eq__` (inherited from `Equatable`),
and `__hash__` (via `Hashable`) downstream.

### Dunder Methods
```python
def __lt__(self, other: object) -> bool:
def __le__(self, other: object) -> bool:
def __gt__(self, other: object) -> bool:
def __ge__(self, other: object) -> bool:
```
Each returns the result of comparing `self.key` with `other.key`.
2 `key` accesses per call — no indirection, no extra method calls.

### Inherited from Equatable
```python
def __eq__(self, other: object) -> bool:
```
Equality via `key`. Identity short-circuit.

## Inheritance (Hierarchy)

```
SupportsEquality (Protocol)
 ├── Equatable
 │    └── Comparable (+ SupportsComparison)
 └── SupportsComparison (Protocol)
```

| Base                 | Responsibility                                   |
|----------------------|--------------------------------------------------|
| `SupportsEquality`   | Protocol defining `__eq__` contract              |
| `Equatable`          | Provides `__eq__` implementation via `key`       |
| `SupportsComparison` | Protocol defining `__lt__` contract              |

## Dependencies

| Import                                            | Purpose                                              |
|---------------------------------------------------|------------------------------------------------------|
| `abc.abstractmethod`                              | Marks `key` as abstract                              |
| `f_core.mixins.equatable.main.Equatable`          | Base class providing equality via `key`              |
| `f_core.protocols.comparison.SupportsComparison`  | Protocol this class implements; return type of `key` |

## Usage Examples

### Custom Subclass
```python
from f_core.mixins.comparable import Comparable

class Score(Comparable):
    def __init__(self, points: int) -> None:
        self.points = points

    @property
    def key(self) -> int:
        return self.points

s1 = Score(100)
s2 = Score(150)

s1 < s2   # True
s2 > s1   # True
s1 <= s1  # True
s1 == Score(100)  # True (from Equatable)

sorted([Score(50), Score(100), Score(75)])  # [50, 75, 100]
```

### Using the Factory
```python
from f_core.mixins.comparable import Comparable

a = Comparable.Factory.a()  # Char('A')
b = Comparable.Factory.b()  # Char('B')

a < b   # True
a == a  # True
b > a   # True
```
