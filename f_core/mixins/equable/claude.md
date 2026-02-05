# Equable

## Purpose

Abstract mixin class for objects that support equality checks. Provides `==`, `!=`, and `hash()` operations based on a single `key_comparison()` method that subclasses must implement.

## Public API

### Abstract Methods

```python
@abstractmethod
def key_comparison(self) -> ProtocolEquable
```
Must be implemented by subclasses. Returns the key used for equality comparison and hashing. The returned object must support `==`.

### Dunder Methods

```python
def __eq__(self, other: Equable) -> bool
```
Returns `True` if `self.key_comparison() == other.key_comparison()`. If `other` lacks `key_comparison()`, compares directly: `self.key_comparison() == other`.

```python
def __ne__(self, other: Equable) -> bool
```
Returns `not self == other`.

```python
def __hash__(self) -> int
```
Returns `hash(self.key_comparison())`. Enables use in sets and as dict keys.

## Inheritance (Hierarchy)

```
ABC
 └── Equable
```

| Base Class | Responsibilities |
|------------|------------------|
| `ABC` | Makes `Equable` abstract; enforces `key_comparison()` implementation |

### Classes That Inherit Equable

| Class | Module |
|-------|--------|
| `Comparable` | `f_core.mixins.comparable` |

## Dependencies

| Import | Purpose |
|--------|---------|
| `abc.ABC` | Abstract base class |
| `abc.abstractmethod` | Decorator for `key_comparison()` |
| `f_core.protocols.equable.Equable` | Type hint for `key_comparison()` return value (aliased as `ProtocolEquable`) |

## Usage Example

```python
from f_core.mixins.equable import Equable

class Point(Equable):
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def key_comparison(self) -> tuple[int, int]:
        return (self.x, self.y)

# Equality
p1 = Point(1, 2)
p2 = Point(1, 2)
p3 = Point(3, 4)

p1 == p2  # True
p1 != p3  # True

# Works with sets and dicts
points = {Point(1, 2), Point(1, 2), Point(3, 4)}  # len = 2
data = {Point(0, 0): "origin"}

# Comparison with raw values (via fallback in __eq__)
p1 == (1, 2)  # True - compares key_comparison() with tuple directly
```
