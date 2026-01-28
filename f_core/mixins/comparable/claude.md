# Comparable Mixin Module

> **Location:** `f_core/mixins/comparable`
> **Purpose:** Extends [Equable](../equable/claude.md) with ordering operators for sortable objects

---

## Quick Reference

| Component | Description |
|-----------|-------------|
| `Comparable` | Mixin for ordering operations |
| `key_comparison()` | Abstract method (same as Equable) |
| Inherits | [Equable](../equable/claude.md) (`==`, `!=`, `hash`) |
| Adds | `<`, `<=`, `>`, `>=` |

---

## Architecture

```
ABC
 └── Equable ─────────────── (../equable/)
      │  ├── __eq__()
      │  ├── __ne__()
      │  └── __hash__()
      │
      └── Comparable ─────── (this module)
           ├── __lt__()
           ├── __le__()
           ├── __gt__()
           └── __ge__()
```

### What You Get

| From [Equable](../equable/claude.md) | From Comparable |
|--------------------------------------|-----------------|
| `==` equality | `<` less than |
| `!=` inequality | `<=` less or equal |
| `hash()` hashing | `>` greater than |
| | `>=` greater or equal |

---

## Files

| File | Purpose |
|------|---------|
| `main.py` | Core `Comparable` class |
| `_factory.py` | Factory with test instances |
| `_tester.py` | Unit tests for all operators |
| `__init__.py` | Exports + Factory binding |

---

## Comparable Class

### Abstract Method

```python
@abstractmethod
def key_comparison(self) -> Equable:
    """Return the key for comparison."""
    pass
```

Same as [Equable.key_comparison()](../equable/claude.md) - one method drives all operators.

### Provided Methods

| Method | Returns | Implementation |
|--------|---------|----------------|
| `__lt__(other)` | `bool` | `self.key < other.key` |
| `__le__(other)` | `bool` | `self.key <= other.key` |
| `__gt__(other)` | `bool` | `self.key > other.key` |
| `__ge__(other)` | `bool` | `self.key >= other.key` |

### Inherited from [Equable](../equable/claude.md)

| Method | Returns | Description |
|--------|---------|-------------|
| `__eq__(other)` | `bool` | Equality via key |
| `__ne__(other)` | `bool` | Inequality via key |
| `__hash__()` | `int` | Hash of key |

---

## Factory Methods

```python
Comparable.Factory.a()  # key='A'
Comparable.Factory.b()  # key='B'
```

Uses internal `Temp` class for testing:
```python
class Temp(Comparable):
    def __init__(self, key: str):
        self.key = key
    def key_comparison(self) -> str:
        return self.key
```

---

## Usage Examples

### Basic Implementation

```python
from f_core.mixins.comparable import Comparable

class Score(Comparable):
    def __init__(self, points: int):
        self.points = points

    def key_comparison(self) -> int:
        return self.points

# All operators work
s1 = Score(100)
s2 = Score(150)

s1 < s2   # True
s2 > s1   # True
s1 <= s1  # True
s1 == Score(100)  # True (from Equable)
```

### Sorting

```python
scores = [Score(50), Score(100), Score(75)]
sorted(scores)  # [Score(50), Score(75), Score(100)]
min(scores)     # Score(50)
max(scores)     # Score(100)
```

### Multi-Criteria Comparison

```python
class Person(Comparable):
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def key_comparison(self) -> tuple[int, str]:
        return (self.age, self.name)  # Sort by age, then name

people = [Person("Alice", 30), Person("Bob", 25), Person("Charlie", 30)]
sorted(people)  # [Bob(25), Alice(30), Charlie(30)]
```

### With Collections

```python
# Sets work (via Equable's __hash__)
unique = {Score(100), Score(50), Score(100)}  # len = 2

# Dict keys work
rankings = {Score(100): "Gold", Score(50): "Bronze"}
```

---

## Classes That Inherit Comparable

| Class | Module | key_comparison() |
|-------|--------|------------------|
| `HasName` | `mixins/has/name` | `self._name or ''` |
| `HasRowCol` | `mixins/has/row_col` | `(row, col)` |
| `HasKey` | `mixins/has/key` | `self._key` |
| `Bounds` | `f_gui/layout/bounds` | `(x, y, w, h)` |
| `Path` | `f_search/ds/path` | `list[State]` |
| `RGB` | `f_color/rgb` | `(r, g, b)` |
| `PriorityKey` | `f_search/ds/priority` | `self._key` |

---

## Equable vs Comparable

| Aspect | [Equable](../equable/claude.md) | Comparable |
|--------|----------------------------------|------------|
| Purpose | Identity/Equality | Ordering/Ranking |
| Operators | `==`, `!=`, `hash()` | + `<`, `<=`, `>`, `>=` |
| Use for | Sets, dicts, deduplication | Sorting, min/max, ranges |
| Inherits | `ABC` | `Equable` |
| Use when | Only need equality | Need to order objects |

---

## Common Patterns

### Tuple Keys for Multi-Criteria Sort

```python
def key_comparison(self) -> tuple[int, str]:
    return (self.priority, self.name)
# Sorts by priority first, then name
```

### Handling None Values

```python
def key_comparison(self) -> str:
    return self._name or ""  # Empty string sorts first
```

### Generic Type Wrapping

```python
class PriorityKey(Generic[Key], Comparable):
    def __init__(self, key: Key):
        self._key = key
    def key_comparison(self) -> Key:
        return self._key
```

---

## Dependencies

**Internal:**
- [f_core.mixins.equable.Equable](../equable/claude.md) (base class)
- `f_core.protocols.equable.Equable` (type hint)

**External:** None

---

## Design Patterns

1. **Template Method** - All operators delegate to `key_comparison()`
2. **Factory Pattern** - `Comparable.Factory.a()` for test instances
3. **Mixin Composition** - Often paired with `Printable`
4. **Tuple Unpacking** - Multi-criteria comparison via tuples

---

## Related Documentation

- **[Equable Mixin](../equable/claude.md)** - Base class providing equality
- **[HasName Mixin](../has/name/claude.md)** - Name-based comparable
