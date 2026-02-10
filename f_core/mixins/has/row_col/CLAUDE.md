# HasRowCol

## Purpose

Mixin that gives objects `row` and `col` properties representing a position on a 2D grid. Provides comparison (row-major order), hashing, neighbor discovery, Manhattan distance, and bounds checking — all derived from the `(row, col)` pair.

## Public API

### Class Attributes

```python
Factory = None
```
Factory class for creating instances. Attached via `__init__.py`.

### Constructor

```python
def __init__(self, row: int = None, col: int = None) -> None
```
Sets `_row` and `_col`. If `row` is `None`, defaults to `0`. If `col` is `None`, defaults to the value of `row`.

### Properties

```python
@property
def row(self) -> int
```
Returns the object's row (read-only).

```python
@property
def col(self) -> int
```
Returns the object's column (read-only).

### Methods

```python
def neighbors(self) -> list[HasRowCol]
```
Returns up to 4 neighbors in clock-wise order (North, East, South, West). Filters out positions with negative row or col.

```python
def distance(self, other: Self) -> int
```
Returns Manhattan distance (`|row_diff| + |col_diff|`) to `other`.

```python
def is_within(self, rect: Rect = None, row_min: int = None, col_min: int = None, row_max: int = None, col_max: int = None) -> bool
```
Returns `True` if position is within the given `Rect` or explicit bounds. If `rect` is provided, it overrides the individual min/max parameters.

```python
def key_comparison(self) -> tuple[int, int]
```
Returns `(self.row, self.col)`. Implements the abstract method from `Equatable`. Row is prioritized over col (row-major order).

```python
def to_tuple(self) -> tuple[int, int]
```
Returns `(self.row, self.col)`.

### Dunder Methods

```python
def __str__(self) -> str
```
Returns `(row,col)`.

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
           └── HasRowCol(Comparable, Hashable)
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
| `typing.Self` | Self-type for `distance()` return annotation |
| `f_math.shapes.Rect` | Type-only import for `is_within()` parameter |

## Usage Example

```python
from f_core.mixins.has.row_col import HasRowCol

zero = HasRowCol.Factory.zero()     # row=0, col=0
one = HasRowCol.Factory.one()       # row=1, col=1
twelve = HasRowCol.Factory.twelve()  # row=1, col=2

assert str(twelve) == '(1,2)'
assert twelve.to_tuple() == (1, 2)

# Comparison (row-major)
assert zero < one
assert HasRowCol(0, 3) < HasRowCol(1, 2)  # row 0 < row 1

# Neighbors (clock-wise: N, E, S, W)
assert twelve.neighbors() == [
    HasRowCol(0, 2), HasRowCol(1, 3),
    HasRowCol(2, 2), HasRowCol(1, 1)
]

# Manhattan distance
assert HasRowCol(0, 0).distance(HasRowCol(2, 3)) == 5

# Hashing
assert hash(zero) != hash(one)
```
