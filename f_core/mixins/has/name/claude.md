# HasName

## Purpose

Mixin that gives objects a `name` property and derives equality, ordering, hashing, string representation, and repr from it. Objects with `HasName` can be compared, sorted, used in sets/dicts, and printed — all based on their name.

## Public API

### Class Attributes

```python
Factory: type | None = None
```
Factory class for creating instances. Attached via `__init__.py`.

### Constructor

```python
def __init__(self, name: str = 'None') -> None
```
Stores `name` as `_name`. Default is the string `'None'`.

### Properties

```python
@property
def name(self) -> str
```
Returns the object's name (read-only).

```python
@property
def key(self) -> str
```
Returns `self._name`. Satisfies the abstract `key` contract from `Equatable`/`Comparable`.

### Dunder Methods

```python
def __str__(self) -> str
```
Returns `self.name`.

```python
def __repr__(self) -> str
```
Returns `<ClassName: Name=value>`. Uses `type(self).__name__`, so subclasses show their own class name.

## Inheritance (Hierarchy)

```
Equatable (abstract key, __eq__)
  ├── Comparable (@total_ordering, __lt__)
  └── Hashable (__hash__ via key)
       └── HasName(Comparable, Hashable)
```

| Base | Responsibility |
|------|----------------|
| `Equatable` | Abstract `key` property, concrete `__eq__` |
| `Comparable` | `@total_ordering`, concrete `__lt__` |
| `Hashable` | Concrete `__hash__` via `hash(self.key)` |

## Dependencies

| Import | Purpose |
|--------|---------|
| `__future__.annotations` | Postponed evaluation of annotations |
| `f_core.mixins.comparable.Comparable` | Base — ordering operators |
| `f_core.mixins.hashable.Hashable` | Base — hashing |

## Usage Example

```python
from f_core.mixins.has.name import HasName

a = HasName.Factory.a()   # HasName(name='A')
b = HasName.Factory.b()   # HasName(name='B')

print(a.name)      # 'A'
print(str(a))      # 'A'
print(repr(a))     # '<HasName: Name=A>'
print(a == HasName.Factory.a())  # True
print(a < b)       # True
print(hash(a))     # hash('A')
```
