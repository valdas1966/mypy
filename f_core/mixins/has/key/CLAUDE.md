# HasKey

## Purpose

Generic mixin that gives objects a typed `key` property and derives equality, ordering, hashing, string representation, and repr from it. Objects with `HasKey` can be compared, sorted, used in sets/dicts, and printed — all based on their key.

## Public API

### Class Attributes

```python
Factory: type | None = None
```
Factory class for creating instances. Attached via `__init__.py`.

### Constructor

```python
def __init__(self, key: Key) -> None
```
Stores `key` as `_key`.

### Properties

```python
@property
def key(self) -> Key
```
Returns the key. Satisfies the abstract `key` contract from `Equatable`/`Comparable`.

### Dunder Methods

```python
def __str__(self) -> str
```
Returns `str(self.key)`.

```python
def __repr__(self) -> str
```
Returns `<ClassName: Key=value>`.

## Inheritance (Hierarchy)

```
Equatable (abstract key, __eq__)
  ├── Comparable (@total_ordering, __lt__)
  └── Hashable (__hash__ via key)
       └── HasKey(Comparable, Hashable, Generic[Key])
```

| Base | Responsibility |
|------|----------------|
| `Equatable` | Abstract `key` property, concrete `__eq__` |
| `Comparable` | `@total_ordering`, concrete `__lt__` |
| `Hashable` | Concrete `__hash__` via `hash(self.key)` |
| `Generic[Key]` | Type parameterization for the key type |

## Dependencies

| Import | Purpose |
|--------|---------|
| `f_core.mixins.comparable.Comparable` | Base — ordering operators |
| `f_core.mixins.hashable.Hashable` | Base — hashing |
| `typing.Generic`, `TypeVar` | Generics |

## Usage Example

```python
from f_core.mixins.has.key import HasKey

a = HasKey.Factory.a()   # HasKey[str](key='A')
b = HasKey.Factory.b()   # HasKey[str](key='B')

print(a.key)      # 'A'
print(str(a))     # 'A'
print(repr(a))    # '<HasKey: Key=A>'
print(a == HasKey.Factory.a())  # True
print(a < b)      # True
print(hash(a))    # hash('A')
```
