# HasName Mixin Module

> **Location:** `f_core/mixins/has/name`
> **Purpose:** Provides name-based identification, comparison, and string representation

---

## Quick Reference

| Component | Description |
|-----------|-------------|
| `HasName` | Mixin class with `name` property |
| `Factory` | Static factory for test instances |
| Inherits | [Comparable](../../comparable/claude.md) → [Equable](../../equable/claude.md), Printable |

---

## Architecture

```
ABC
 └── Equable ─────────────── ../../equable/
      │  ├── __eq__()
      │  ├── __ne__()
      │  └── __hash__()
      │
      └── Comparable ─────── ../../comparable/
           │  ├── __lt__()
           │  ├── __le__()
           │  ├── __gt__()
           │  └── __ge__()
           │
           └── HasName ───── (this module)
                │  ├── name (property)
                │  ├── key_comparison()
                │  ├── __str__()
                │  └── __repr__()
                │
                └── Printable
                     ├── __str__() [abstract]
                     └── __repr__()
```

### What You Get

| From [Equable](../../equable/claude.md) | From [Comparable](../../comparable/claude.md) | From HasName |
|-----------------------------------------|-----------------------------------------------|--------------|
| `==` equality | `<` less than | `name` property |
| `!=` inequality | `<=` less or equal | `__str__()` |
| `hash()` | `>` greater than | `__repr__()` |
| | `>=` greater or equal | `key_comparison()` |

---

## Files

| File | Purpose |
|------|---------|
| `main.py` | Core `HasName` class |
| `_factory.py` | Factory with preset instances |
| `_tester.py` | Unit tests |
| `__init__.py` | Exports + Factory binding |

---

## HasName Class

### Constructor

```python
def __init__(self, name: str = None) -> None
```

### Properties

| Property | Type | Access | Description |
|----------|------|--------|-------------|
| `name` | `str` | get/set | The object's name (default: None) |

### Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `key_comparison()` | `str` | Returns `name` or `''` for sorting |
| `__str__()` | `str` | Returns `name` or `'None'` |
| `__repr__()` | `str` | Returns `<HasName: Name={name}>` |
| `__hash__()` | `int` | Hash of name (overrides [Equable](../../equable/claude.md)) |

### Inherited from [Comparable](../../comparable/claude.md)

| Operator | Method |
|----------|--------|
| `<` | `__lt__()` |
| `<=` | `__le__()` |
| `>` | `__gt__()` |
| `>=` | `__ge__()` |

### Inherited from [Equable](../../equable/claude.md)

| Operator | Method |
|----------|--------|
| `==` | `__eq__()` |
| `!=` | `__ne__()` |

---

## Factory Methods

```python
HasName.Factory.a()      # name='A'
HasName.Factory.empty()  # name=''
HasName.Factory.none()   # name=None
```

---

## Behavior

### Name States

| State | `str()` | `key_comparison()` | Sort Position |
|-------|---------|-------------------|---------------|
| `name=None` | `'None'` | `''` | First |
| `name=''` | `'None'` | `''` | First |
| `name='X'` | `'X'` | `'X'` | Alphabetical |

### Sort Order

```
None/empty < 'A' < 'B' < 'apple' < 'zebra'
```

---

## Usage Examples

### Basic Usage

```python
from f_core.mixins.has.name import HasName

obj = HasName(name="MyObject")
print(obj.name)   # "MyObject"
print(str(obj))   # "MyObject"
print(repr(obj))  # <HasName: Name=MyObject>
```

### Sorting

```python
items = [HasName("zebra"), HasName("apple"), HasName(None)]
sorted(items)  # [None, "apple", "zebra"]
min(items)     # HasName(None)
max(items)     # HasName("zebra")
```

### Collections

```python
# Sets work (via Equable)
names = {HasName("alice"), HasName("bob")}

# Dict keys work
data = {HasName("config"): {"debug": True}}
```

### Inheritance

```python
class Person(HasName):
    def __init__(self, name: str, age: int):
        super().__init__(name=name)
        self.age = age

people = [Person("Bob", 30), Person("Alice", 25)]
sorted(people)  # [Alice, Bob] - sorted by name
```

---

## Dependencies

**Inherits:**
- [f_core.mixins.comparable.Comparable](../../comparable/claude.md)
- f_core.mixins.printable.Printable

**Through Comparable:**
- [f_core.mixins.equable.Equable](../../equable/claude.md)

**External:** None

---

## Related Modules

| Module | Relationship |
|--------|--------------|
| [Equable](../../equable/claude.md) | Grandparent - provides equality |
| [Comparable](../../comparable/claude.md) | Parent - provides ordering |
| `has/key` | Sibling - generic key mixin |
| `has/id` | Sibling - timestamp ID mixin |

---

## Design Patterns

1. **Template Method** - Implements `key_comparison()` from [Comparable](../../comparable/claude.md)
2. **Factory Pattern** - `HasName.Factory.<method>()` for test instances
3. **Property Pattern** - Encapsulated `_name` with getter/setter
4. **None Handling** - None/empty treated as empty string for sorting
