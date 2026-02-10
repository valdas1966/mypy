# HasName

## Purpose

Mixin that gives objects a `name` property and derives comparison, equality, hashing, and string representation from it. Objects with `HasName` can be compared, sorted, used in sets/dicts, and printed — all based on their name.

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
Stores `name` as the private attribute `_name`. Default is the string `'None'`.

### Properties

```python
@property
def name(self) -> str
```
Returns the object's name (read-only).

### Methods

```python
def key_comparison(self) -> str
```
Returns `self._name`. Implements the abstract method from `Equatable`, used by all equality, comparison, and hashing operations.

### Dunder Methods

```python
def __str__(self) -> str
```
Returns `self.name` directly.

```python
def __repr__(self) -> str
```
Returns `<ClassName: Name={name}>`. Uses `type(self).__name__`, so subclasses show their own class name.

### Inherited from Hashable

```python
def __hash__(self) -> int
```
Returns `hash(self.key_comparison())`. Enables use in sets and as dict keys.

### Inherited from Comparable (`@total_ordering`)

```python
def __lt__(self, other: object) -> bool
def __le__(self, other: object) -> bool
def __gt__(self, other: object) -> bool
def __ge__(self, other: object) -> bool
```

### Inherited from Equatable

```python
def __eq__(self, other: object) -> bool
```

## Inheritance (Hierarchy)

```
SupportsEquality (Protocol)
 └── Equatable          # ==, != via key_comparison()
      ├── Hashable       # __hash__ via key_comparison()
      └── Comparable     # <, <=, >, >= via @total_ordering + key_comparison()
           └── HasName(Comparable, Hashable)
```

| Base | Responsibility |
|------|----------------|
| `Equatable` | Equality operator (`==`) via `key_comparison()` |
| `Comparable` | Ordering operators (`<`, `<=`, `>`, `>=`) via `@total_ordering` and `key_comparison()` |
| `Hashable` | Hashing (`__hash__`) via `key_comparison()` |

## Dependencies

| Import | Purpose |
|--------|---------|
| `__future__.annotations` | Postponed evaluation of annotations |
| `f_core.mixins.comparable.Comparable` | Base class providing ordering operators |
| `f_core.mixins.hashable.Hashable` | Base class providing `__hash__` |

## Usage Example

```python
from f_core.mixins.has.name import HasName

a = HasName.Factory.a()     # name='A'
b = HasName.Factory.b()     # name='B'
default = HasName()          # name='None' (default)

assert str(a) == 'A'
assert str(default) == 'None'
assert repr(a) == '<HasName: Name=A>'

assert HasName.Factory.a() == HasName.Factory.a()
assert a < b                 # 'A' < 'B'
assert {a, a, b} == {a, b}  # set dedup via __hash__ + __eq__
```
