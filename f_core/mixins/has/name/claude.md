# HasName

## Purpose

Mixin that provides a `name` property with full comparison, hashing, and string representation. Objects with `HasName` can be compared, sorted, used in sets/dicts, and printed — all based on their name.

## Public API

### Class Attributes

```python
Factory: type | None = None
```
Factory class for creating instances. Attached via `__init__.py`.

### Constructor

```python
def __init__(self, name: str = None) -> None
```
Stores `name` as the private attribute `_name`.

### Properties

```python
@property
def name(self) -> str
```
Returns the object's name.

```python
@name.setter
def name(self, name: str) -> None
```
Sets the object's name.

### Methods

```python
def key_comparison(self) -> str
```
Returns `self._name`. Implements the abstract method from `Comparable`/`Equable`, used for all comparison and equality operations.

### Dunder Methods

```python
def __str__(self) -> str
```
Returns `name` if truthy, otherwise `'None'`. Note: both `None` and `''` produce `'None'`.

```python
def __repr__(self) -> str
```
Returns `<ClassName: Name={name}>`.

```python
def __hash__(self) -> int
```
Returns `hash(self.name)`. Enables use in sets and as dict keys.

### Inherited from Comparable

```python
def __lt__(self, other: Comparable) -> bool
def __le__(self, other: Comparable) -> bool
def __gt__(self, other: Comparable) -> bool
def __ge__(self, other: Comparable) -> bool
```

### Inherited from Equable

```python
def __eq__(self, other: Equable) -> bool
```

## Inheritance (Hierarchy)

```
SupportsEquality (Protocol)
 └── Equable          # ==, != via key_comparison()
      └── Comparable  # <, <=, >, >= via key_comparison()
           └── HasName
```

| Base | Responsibility |
|------|----------------|
| `Equable` | Equality operators (`==`) via `key_comparison()` |
| `Comparable` | Ordering operators (`<`, `<=`, `>`, `>=`) via `key_comparison()` |

## Dependencies

| Import | Purpose |
|--------|---------|
| `__future__.annotations` | Postponed evaluation of annotations |
| `f_core.mixins.comparable.Comparable` | Base class providing comparison operators |

## Usage Example

```python
from f_core.mixins.has.name import HasName

obj = HasName(name="Alice")
print(obj.name)    # Alice
print(str(obj))    # Alice
print(repr(obj))   # <HasName: Name=Alice>

# Sorting
items = [HasName("zebra"), HasName("apple"), HasName("banana")]
sorted(items)  # [apple, banana, zebra]

# Sets and dicts
{HasName("a"), HasName("b"), HasName("a")}  # 2 elements
```

### Using the Factory

```python
from f_core.mixins.has.name import HasName

a = HasName.Factory.a()          # name='A'
empty = HasName.Factory.empty()  # name=''
none = HasName.Factory.none()    # name=None

assert str(a) == 'A'
assert str(empty) == 'None'    # '' is falsy
assert str(none) == 'None'

assert empty < a               # '' < 'A'
assert empty == none
```
