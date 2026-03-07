# HasRowCol

## Purpose
Mixin that gives objects `row` and `col` properties for 2D grid
positioning. Provides row-major comparison, hashing, clockwise
neighbor discovery, Manhattan distance, and bounds checking.
All operators delegate to the `(row, col)` key tuple.

## Public API

### Constructor
```python
def __init__(self,
             row: int | None = None,
             col: int | None = None) -> None
```
Sets `_row` and `_col`. `row=None` defaults to `0`.
`col=None` defaults to the value of `row`.

### Properties
```python
@property
def row(self) -> int

@property
def col(self) -> int

@property
def key(self) -> tuple[int, int]
```
`key` returns `(row, col)` — row-major order. Satisfies the
abstract `key` contract from `Comparable` and `Hashable`.

### Methods
```python
def neighbors(self) -> list[Self]
```
Returns up to 4 neighbors in clockwise order (N, E, S, W).
Filters out positions with negative row or col.
Uses `type(self)` to create instances — subclass-safe.

```python
def distance(self, other: Self) -> int
```
Returns Manhattan distance: `|row_diff| + |col_diff|`.

```python
def is_within(self,
              rect: RectLike | None = None,
              row_min: int | None = None,
              col_min: int | None = None,
              row_max: int | None = None,
              col_max: int | None = None) -> bool
```
Returns `True` if position is inside the given `rect` or explicit
min/max bounds. If `rect` is provided, extracts bounds via
`rect.to_rect_coords()`.

### Dunder Methods
```python
def __str__(self) -> str       # '(row,col)'
def __repr__(self) -> str      # '<HasRowCol: Row=1, Col=2>'
```

### Inherited
```python
def __eq__(self, other: object) -> bool   # from Equatable
def __lt__(self, other: object) -> bool   # from Comparable
def __le__(self, other: object) -> bool   # from Comparable
def __gt__(self, other: object) -> bool   # from Comparable
def __ge__(self, other: object) -> bool   # from Comparable
def __hash__(self) -> int                 # from Hashable
```
All delegate to `self.key` — the `(row, col)` tuple.

## Inheritance (Hierarchy)

```
SupportsEquality (Protocol)
 └── Equatable ─── __eq__ via key
      ├── Comparable (+ SupportsComparison) ─── __lt__, __le__, __gt__, __ge__
      └── Hashable ─── __hash__ via key
           └── HasRowCol(Comparable, Hashable)
                └── key = (row, col)
```

| Base | Responsibility |
|------|----------------|
| `Equatable` | Abstract `key` property, concrete `__eq__` |
| `Comparable` | Comparison operators via `key` |
| `Hashable` | `__hash__` via `hash(self.key)` |

## Dependencies

| Import | Purpose |
|--------|---------|
| `f_core.mixins.comparable.Comparable` | Base — ordering operators |
| `f_core.mixins.hashable.Hashable` | Base — hashing |
| `f_core.protocols.rect_like.RectLike` | Protocol for `is_within()` rect param |
| `typing.Self` | Self-type for `neighbors()`, `distance()` |

## Usage Examples

### Basic Usage
```python
from f_core.mixins.has.row_col import HasRowCol

cell = HasRowCol(row=1, col=2)
print(cell)           # (1,2)
print(cell.key)       # (1, 2)
print(repr(cell))     # <HasRowCol: Row=1, Col=2>
```

### Comparison and Hashing
```python
a = HasRowCol(0, 0)
b = HasRowCol(1, 1)
a < b                 # True (row-major)
hash(a) != hash(b)    # True
{a, b, HasRowCol(0, 0)}  # {(0,0), (1,1)} — dedup works
```

### Neighbors and Distance
```python
cell = HasRowCol(1, 2)
cell.neighbors()      # [(0,2), (1,3), (2,2), (1,1)]
cell.distance(HasRowCol(3, 4))  # 4
```

### Bounds Checking
```python
from f_math.shapes import Rect

cell = HasRowCol(1, 2)
rect = Rect.From.Center(x=0, y=0, distance=2)
cell.is_within(rect=rect)  # True
cell.is_within(row_min=0, col_min=0, row_max=5, col_max=5)  # True
```

### Factory
```python
from f_core.mixins.has.row_col import HasRowCol

zero   = HasRowCol.Factory.zero()    # (0,0)
one    = HasRowCol.Factory.one()     # (1,1)
twelve = HasRowCol.Factory.twelve()  # (1,2)
```
