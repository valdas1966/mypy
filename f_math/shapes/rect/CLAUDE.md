# Rect

## Purpose
A rectangle stored as **(Top, Left, Width, Height)** — used as a GUI
bounding box. A value-shape: identity is its four coordinates (not its
name), so two Rects with equal coordinates are equal.

## Public API

### Construction
```python
Rect(top: T = None, left: T = None, width: T = None, height: T = None,
     name: str = 'Rect') -> None       # T = int | float
```

### Coordinates
```python
@property top(self)    -> T
@property left(self)   -> T
@property width(self)  -> T
@property height(self) -> T
```

### Conversions
```python
def to_tuple(self) -> tuple[T, T, T, T]        # (top, left, width, height)
def to_rect_coords(self) -> tuple[T, T, T, T]  # (x_min, y_min, x_max, y_max)
#   x = vertical axis (top .. top+height-1), y = horizontal (left ..
#   left+width-1); maxima inclusive — feeds HasRowCol.is_within().
```

### Identity
```python
@property
def key(self) -> tuple[T, T, T, T]    # (top, left, width, height)
```
Identity = the coordinate tuple. Equality (from `Shape` → `Equatable`)
compares by `key`, so `Rect(10,20,30,40) == Rect(10,20,30,40)`. `name`
is a label only and does not affect equality.

```python
def __str__(self) -> str              # '(top, left, width, height)'
```

### Factory / From
```python
Rect.Factory.full()    -> Rect   # (0, 0, 100, 100)
Rect.Factory.half()    -> Rect   # (25, 25, 50, 50)
Rect.Factory.quarter() -> Rect   # (37.5, 37.5, 25, 25)
Rect.From.Center(x, y, distance) -> Rect   # square centred on (x, y)
```

## Inheritance (Hierarchy)
```
Shape(HasName, Equatable)   — name label + __eq__ via key
Generic[T]                  — T = int | float
   └── Rect(Shape, Generic[T])   — overrides key = (top, left, width, height)
```

## Dependencies
| Import | Purpose |
|--------|---------|
| `f_math.shapes.i_0_shape.Shape` | Base — name + equality |
| `typing.Generic`, `TypeVar` | Numeric type parameter `T` |

## Usage Example
```python
from f_math.shapes import Rect

r = Rect(top=10, left=20, width=30, height=40)
r.to_tuple()                     # (10, 20, 30, 40)
r == Rect(10, 20, 30, 40)        # True  (identity = coordinates)
Rect.Factory.half()              # Rect(25, 25, 50, 50)
Rect.From.Center(x=50, y=50, distance=25)   # 51×51 square at (25, 25)
```
