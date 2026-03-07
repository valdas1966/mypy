# Mixins Package

## Purpose
Library of composable mixin classes that inject standard behaviors into
domain objects via multiple inheritance. Three categories: equality/ordering,
size/validity, and property injection (name, key, position).

## Package Exports

```python
from f_core.mixins import (
    Sizable, Dictable, Equatable, Comparable,
    Validatable, ValidatableMutable,
    HasKey, HasName, HasRowCol, HasRowsCols
)
```

## Module Hierarchy

```
f_core/mixins/
├── __init__.py                 re-exports 10 classes
├── equatable/                  Equatable — __eq__ via abstract key
├── comparable/                 Comparable — __lt__, __le__, __gt__, __ge__
├── hashable/                   Hashable — __hash__ via key
├── sizable/                    Sizable — __len__ + __bool__
├── dictable/                   Dictable[K, V] — dict-like wrapper
├── validatable/                Validatable — immutable __bool__
├── validatable_mutable/        ValidatableMutable — mutable validity
└── has/                        Has* property mixins (6 submodules)
    ├── children/               HasChildren — children list
    ├── key/                    HasKey[Key] — generic typed key
    ├── name/                   HasName — string name
    ├── parent/                 HasParent — parent reference
    ├── row_col/                HasRowCol — 2D cell position
    └── rows_cols/              HasRowsCols — 2D dimensions
```

## Module Summary

| Module | Class | Bases | Key Capability |
|--------|-------|-------|----------------|
| `equatable` | `Equatable` | `SupportsEquality` | `__eq__` via abstract `key` |
| `comparable` | `Comparable` | `Equatable`, `SupportsComparison` | `__lt__`, `__le__`, `__gt__`, `__ge__` |
| `hashable` | `Hashable` | `Equatable` | `__hash__` via `key` |
| `sizable` | `Sizable` | `Sized` | Abstract `__len__`, concrete `__bool__` |
| `dictable` | `Dictable[K, V]` | `Sizable`, `Generic[K, V]` | Dict-like wrapper with `__getitem__`, iteration |
| `validatable` | `Validatable` | (none) | Immutable `__bool__` from constructor |
| `validatable_mutable` | `ValidatableMutable` | `Validatable` | `set_valid()`, `set_invalid()` |
| `has/key` | `HasKey[Key]` | `Comparable`, `Hashable` | Generic typed key identity |
| `has/name` | `HasName` | (none) | String name + `str()`/`repr()` |
| `has/row_col` | `HasRowCol` | `Comparable`, `Hashable` | Position, neighbors, distance |
| `has/rows_cols` | `HasRowsCols` | `Comparable`, `Hashable` | Dimensions, shape, `len()` |
| `has/children` | `HasChildren` | (none) | Children list, `add_child()` |
| `has/parent` | `HasParent` | (none) | Parent ref, `path_from_root()` |

## Inheritance Chain

```
SupportsEquality (Protocol)
 └── Equatable ─── __eq__ via key
      ├── Comparable (+ SupportsComparison) ─── __lt__, __le__, __gt__, __ge__
      │    ├── HasKey[Key](+ Hashable) ─── generic key identity
      │    ├── HasRowCol(+ Hashable) ─── (row, col) position
      │    └── HasRowsCols(+ Hashable) ─── (rows, cols) dimensions
      └── Hashable ─── __hash__ via key

Sized (collections.abc)
 └── Sizable ─── abstract __len__, __bool__
      └── Dictable[K, V] ─── dict wrapper

Validatable ─── immutable __bool__
 └── ValidatableMutable ─── set_valid(), set_invalid()

HasChildren ─── standalone
HasName ─── standalone
HasParent ─── standalone
```

## Composition Patterns

Mixins are designed to be combined:

```python
# Graph node with position, parent, and comparison
class Cell(HasRowCol, HasParent):
    ...

# Process with name-based identity and mutable validity
class ProcessBase(HasName, ValidatableMutable):
    ...

# Dictionary that is also validatable
class Solutions(Dictable[Node, Path], Validatable):
    ...
```

## Dependencies

| Import | Used By | Purpose |
|--------|---------|---------|
| `f_core.protocols.equality.SupportsEquality` | Equatable | Protocol for `__eq__` |
| `f_core.protocols.comparison.SupportsComparison` | Comparable | Protocol for `__lt__` |
| `f_core.protocols.rect_like.RectLike` | HasRowCol | Bounds checking |
| `collections.abc.Sized` | Sizable | ABC for `__len__` |
| `abc.abstractmethod` | Equatable, Comparable, Sizable | Abstract methods |
| `typing.Generic`, `TypeVar`, `Self` | Dictable, HasKey, Has* | Generics |

## Usage Examples

### Equality and Comparison
```python
from f_core.mixins import Comparable

class Score(Comparable):
    def __init__(self, points: int) -> None:
        self.points = points

    @property
    def key(self) -> int:
        return self.points

Score(100) < Score(150)  # True
Score(100) == Score(100) # True
```

### Dict-like Object
```python
from f_core.mixins import Dictable

d = Dictable(data={'a': 1, 'b': 2})
d['c'] = 3
print(len(d))     # 3
print(bool(d))    # True
```

### Validity Checking
```python
from f_core.mixins import ValidatableMutable

obj = ValidatableMutable(is_valid=True)
if obj:            # True
    obj.set_invalid()
if not obj:        # True
    pass
```
