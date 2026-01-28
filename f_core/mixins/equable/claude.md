# Equable Mixin Module

> **Location:** `f_core/mixins/equable.py`
> **Purpose:** Foundational mixin providing equality operations via key-based comparison

---

## Quick Reference

| Component | Description |
|-----------|-------------|
| `Equable` | Abstract mixin for equality operations |
| `key_comparison()` | Abstract method returning comparison key |
| Provides | `__eq__`, `__ne__`, `__hash__` |
| Inherits | `ABC` |

---

## Architecture

```
Equable (ABC)
    │
    ├── key_comparison()  [abstract]
    │
    ├── __eq__()   ──┐
    ├── __ne__()   ──┼── All delegate to key_comparison()
    └── __hash__() ──┘

         ┌─────────────────┐
         │    Equable      │
         └────────┬────────┘
                  │
    ┌─────────────┼─────────────┐
    │             │             │
    ▼             ▼             ▼
Comparable      Pair      EntryPriority
    │
    ▼
HasName, HasKey, ...
```

---

## Core Concept: Template Method Pattern

Equable uses the **Template Method Pattern**:

1. Concrete methods (`__eq__`, `__ne__`, `__hash__`) are implemented
2. They delegate to abstract `key_comparison()`
3. Subclasses only implement `key_comparison()`

```python
# You implement this:
def key_comparison(self) -> Equable:
    return self.value

# You get these for free:
__eq__, __ne__, __hash__
```

---

## Equable Class

### Abstract Method

```python
@abstractmethod
def key_comparison(self) -> Equable:
    """Return a value used for equality comparison."""
    pass
```

### Provided Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `__eq__(other)` | `bool` | True if keys are equal |
| `__ne__(other)` | `bool` | True if keys differ |
| `__hash__()` | `int` | Hash of comparison key |

### Equality Logic

```python
def __eq__(self, other):
    if hasattr(other, 'key_comparison'):
        return self.key_comparison() == other.key_comparison()
    else:
        return self.key_comparison() == other
```

- Compares keys if both have `key_comparison()`
- Falls back to direct comparison otherwise

---

## Valid Key Types

| Type | Example | Hashable |
|------|---------|----------|
| Primitives | `int`, `str`, `float` | Yes |
| Tuples | `(a, b, c)` | Yes |
| Named Tuples | `Point(x=1, y=2)` | Yes |
| Frozen Sets | `frozenset({1,2})` | Yes |
| Lists | `[a, b, c]` | No* |

*Lists work for equality but not hashing

---

## Classes That Inherit Equable

### Direct Subclasses

| Class | Module | key_comparison() returns |
|-------|--------|-------------------------|
| `Comparable` | `mixins/comparable` | Ordering key |
| `Pair` | `f_ds/pair` | Tuple of items |
| `EntryPriority` | `f_ds/entry_priority` | `[name] + item.key` |
| `GraphBase` | `f_graph/graphs` | Graph structure |

### Through Comparable

| Class | Module |
|-------|--------|
| `HasName` | `mixins/has/name` |
| `HasKey` | `mixins/has/key` |
| Graph classes | `f_graph/` |

---

## Usage Examples

### Basic Implementation

```python
from f_core.mixins.equable import Equable
from abc import ABC

class Point(Equable):
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def key_comparison(self) -> tuple:
        return (self.x, self.y)

# Now works:
p1 = Point(1, 2)
p2 = Point(1, 2)
p3 = Point(3, 4)

p1 == p2  # True
p1 == p3  # False
p1 != p3  # True
hash(p1) == hash(p2)  # True
```

### Composite Keys

```python
class Person(Equable):
    def __init__(self, name: str, dob: date):
        self.name = name
        self.dob = dob

    def key_comparison(self) -> tuple:
        return (self.name.lower(), self.dob)

# Case-insensitive name comparison
Person("Alice", date(1990,1,1)) == Person("ALICE", date(1990,1,1))  # True
```

### With Collections

```python
# In sets
points = {Point(1,2), Point(3,4)}
Point(1,2) in points  # True

# As dict keys
distances = {Point(0,0): 0, Point(1,1): 1.414}
```

### Ordered/Unordered Keys

```python
class Pair(Equable):
    def __init__(self, a, b, ordered=False):
        self.a, self.b = a, b
        self.ordered = ordered

    def key_comparison(self):
        if self.ordered:
            return (self.a, self.b)
        return tuple(sorted([self.a, self.b]))

# Unordered pairs
Pair(1, 2) == Pair(2, 1)  # True

# Ordered pairs
Pair(1, 2, ordered=True) == Pair(2, 1, ordered=True)  # False
```

---

## Comparison with Other Objects

```python
class Item(Equable):
    def __init__(self, val):
        self.val = val

    def key_comparison(self):
        return self.val

item = Item(42)

# Compare with Equable object
item == Item(42)  # True (compares keys)

# Compare with raw value
item == 42        # True (direct comparison)
```

---

## Protocol vs Mixin

| | Protocol (`protocols/equable.py`) | Mixin (`mixins/equable.py`) |
|---|---|---|
| Purpose | Type checking interface | Implementation |
| Provides | Type hints | `__eq__`, `__ne__`, `__hash__` |
| Usage | `isinstance` checks | Inheritance |

```python
# Protocol - for type hints
from f_core.protocols.equable import Equable as EquableProtocol

def compare(a: EquableProtocol, b: EquableProtocol) -> bool:
    return a == b

# Mixin - for implementation
from f_core.mixins.equable import Equable

class MyClass(Equable):
    ...
```

---

## Dependencies

**Internal:**
- `f_core.protocols.equable.Equable` (Protocol type)

**Standard Library:**
- `abc.ABC`, `abc.abstractmethod`

**External:** None

---

## Design Patterns

1. **Template Method** - Concrete methods delegate to abstract `key_comparison()`
2. **Strategy Pattern** - Key can be any comparable value
3. **Separation of Concerns** - Comparison logic separate from object state
4. **Consistent Hashing** - Hash always derived from same key as equality

---

## Common Pitfalls

### Unhashable Keys

```python
# BAD - lists are not hashable
def key_comparison(self):
    return [self.a, self.b]  # Can't use in sets!

# GOOD - use tuple
def key_comparison(self):
    return (self.a, self.b)
```

### Mutable Keys

```python
# BAD - key changes after hashing
def key_comparison(self):
    return self.mutable_list  # Hash will be wrong!

# GOOD - immutable snapshot
def key_comparison(self):
    return tuple(self.mutable_list)
```

### Inconsistent Keys

```python
# BAD - different types in different states
def key_comparison(self):
    if self.x:
        return self.x
    return None  # Different type!

# GOOD - consistent type
def key_comparison(self):
    return self.x or ""  # Always string
```
