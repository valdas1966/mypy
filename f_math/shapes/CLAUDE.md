# Shapes Package

## Purpose
Geometric shape classes. `Shape` (in `i_0_shape.py`) is the abstract base
for all shapes; concrete shapes live in sub-packages (`rect/`). The
package `__init__` lazily exposes `Rect` via `ULazy`.

## Shape — abstract base (`i_0_shape.py`)

### Purpose
Abstract base for all shapes. Provides a name label and name-based
identity; sub-classes override `key` when their identity is something
other than the name (e.g. `Rect` identifies by its coordinates).

### Public API
```python
Shape(name: str = 'Shape') -> None

@property
def key(self) -> str          # identity = name (sub-classes may override)
```
Equality (from `Equatable`) compares by `key`. `name`, `str()` and
`repr()` come from `HasName`.

### Inheritance (Hierarchy)
```
HasName    — name label + str()/repr()
Equatable  — __eq__ via key
   └── Shape(HasName, Equatable)
        └── Rect (overrides key = coordinates)
```

### Dependencies
| Import | Purpose |
|--------|---------|
| `f_core.mixins.has.name.HasName` | Name label |
| `f_core.mixins.equatable.Equatable` | `__eq__` via `key` |

## Package Exports
```python
from f_math.shapes import Rect      # lazy via ULazy
```

## Usage Example
```python
from f_math.shapes.i_0_shape import Shape

Shape('circle') == Shape('circle')   # True  (identity = name)
Shape('circle') == Shape('square')   # False
```
