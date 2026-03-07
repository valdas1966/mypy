# Has Mixins Package

## Purpose
Collection of 6 mixin classes that inject common object properties:
identity (`key`, `name`), structure (`children`, `parent`), and
2D positioning (`row_col`, `rows_cols`). Each mixin is independently
composable via multiple inheritance.

## Package Exports

```python
from f_core.mixins.has import HasKey, HasName, HasRowCol, HasRowsCols
```

| Export | Description |
|--------|-------------|
| `HasKey` | Generic typed key with comparison, hashing, str/repr |
| `HasName` | String name with comparison, hashing, str/repr |
| `HasRowCol` | Row/col position with neighbors, distance, bounds |
| `HasRowsCols` | Rows/cols dimensions with shape, length, bounds |

`HasChildren` and `HasParent` must be imported from their submodules directly.

## Module Hierarchy

```
f_core/mixins/has/
├── __init__.py           exports HasKey, HasName, HasRowCol, HasRowsCols
├── children/             HasChildren — children list + add_child()
├── key/                  HasKey[Key] — generic typed key
├── name/                 HasName — string name property
├── parent/               HasParent — parent reference + path_from_root()
├── row_col/              HasRowCol — 2D cell position (row, col)
└── rows_cols/            HasRowsCols — 2D dimensions (rows, cols)
```

## Module Summary

| Module | Class | Bases | Key Capability |
|--------|-------|-------|----------------|
| `children` | `HasChildren` | (none) | Children list, `add_child()` |
| `key` | `HasKey[Key]` | `Comparable`, `Hashable`, `Generic[Key]` | Typed key as identity |
| `name` | `HasName` | (none) | String name as identity |
| `parent` | `HasParent` | (none) | Parent ref, `path_from_root()` |
| `row_col` | `HasRowCol` | `Comparable`, `Hashable` | Cell position, neighbors, distance |
| `rows_cols` | `HasRowsCols` | `Comparable`, `Hashable` | Shape dimensions, `is_within()`, `len()` |

## Inheritance Patterns

### Identity Mixins (HasKey, HasRowCol, HasRowsCols)
```
Equatable (abstract key, __eq__)
 ├── Comparable (@total_ordering, __lt__)
 └── Hashable (__hash__ via key)
      └── HasKey / HasRowCol / HasRowsCols
```

### Standalone Mixins (HasChildren, HasName, HasParent)
```
HasChildren  — no bases
HasName      — no bases
HasParent    — no bases
```

## Dependencies

| Import | Used By | Purpose |
|--------|---------|---------|
| `f_core.mixins.comparable.Comparable` | HasKey, HasRowCol, HasRowsCols | Ordering operators |
| `f_core.mixins.hashable.Hashable` | HasKey, HasRowCol, HasRowsCols | Hash via key |
| `f_core.protocols.rect_like.RectLike` | HasRowCol | Bounds checking protocol |
| `typing.Generic`, `TypeVar` | HasKey | Generic key type |
| `typing.Self` | HasChildren, HasParent, HasRowCol | Self-referencing types |

## Usage Examples

### Identity via Key
```python
from f_core.mixins.has.key import HasKey

a = HasKey[str](key='A')
print(a.key)      # 'A'
print(a < HasKey[str](key='B'))  # True
```

### Name Property
```python
from f_core.mixins.has.name import HasName

obj = HasName(name='MyObject')
print(str(obj))   # 'MyObject'
```

### Grid Positioning
```python
from f_core.mixins.has.row_col import HasRowCol

cell = HasRowCol(row=1, col=2)
print(cell.neighbors())   # [(0,2), (1,3), (2,2), (1,1)]
print(cell.distance(HasRowCol(3, 4)))  # 4
```

### Parent-Child Trees
```python
from f_core.mixins.has.parent import HasParent
from f_core.mixins.has.children import HasChildren

parent = HasChildren()
child = HasChildren()
parent.add_child(child=child)
print(len(parent.children))  # 1
```
