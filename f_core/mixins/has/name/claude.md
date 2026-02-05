# HasName

## Purpose

Mixin class that provides a `name` property with comparison and string representation capabilities. Objects inheriting from `HasName` can be compared, sorted, hashed, and displayed using their name as the key.

## Public API

### Constructor

```python
def __init__(self, name: str = None) -> None
```
Initializes the object with an optional name (defaults to `None`).

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
def key_comparison(self) -> str | None
```
Returns `self._name` directly (can be `None`, `''`, or a string value).

### Dunder Methods

```python
def __str__(self) -> str
```
Returns `name` if set, otherwise `'None'`.

```python
def __repr__(self) -> str
```
Returns `<ClassName: Name={name}>`.

```python
def __hash__(self) -> int
```
Returns hash of `name`. Enables use in sets and as dict keys.

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
def __ne__(self, other: Equable) -> bool
```

## Inheritance (Hierarchy)

```
ABC
 └── Equable          # Provides ==, !=, hash()
      └── Comparable  # Provides <, <=, >, >=
           └── HasName
```

| Base Class | Responsibilities |
|------------|------------------|
| `Equable` | Equality operators (`==`, `!=`) and hashing |
| `Comparable` | Ordering operators (`<`, `<=`, `>`, `>=`) via `key_comparison()` |

## Dependencies

| Import | Purpose |
|--------|---------|
| `f_core.mixins.comparable.Comparable` | Base class providing comparison operators |

## Usage Example

```python
from f_core.mixins.has.name import HasName

# Create named objects
obj = HasName(name="Alice")
print(obj.name)    # Alice
print(str(obj))    # Alice
print(repr(obj))   # <HasName: Name=Alice>

# Sorting (only objects with string names)
items = [HasName("zebra"), HasName("apple"), HasName("")]
sorted(items)  # ['', 'apple', 'zebra']

# Using Factory (from _factory.py)
a = HasName.Factory.a()          # name='A'
empty = HasName.Factory.empty()  # name=''
none = HasName.Factory.none()    # name=None

# Comparison
assert empty < a        # '' < 'A'
assert empty != none    # '' != None
assert a == HasName('A')

# Note: Comparing None with str raises TypeError
# none < a  # TypeError: '<' not supported between 'NoneType' and 'str'
```
