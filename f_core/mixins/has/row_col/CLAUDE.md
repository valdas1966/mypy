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
def __init__(self, row: int | None = None, col: int | None = None) -> None
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

```python
@property
def key(self) -> tuple[int, int]
```
Returns `(self.row, self.col)`. Satisfies the abstract `key` contract from `Equatable`/`Comparable`. Row-major order.

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
def to_tuple(self) -> tuple[int, int]
```
Returns `(self.row, self.col)`.

### Dunder Methods

```python
def __str__(self) -> str
```
Returns `(row,col)`.

## Inheritance (Hierarchy)

```
Equatable (abstract key, __eq__)
  ├── Comparable (@total_ordering, __lt__)
  └── Hashable (__hash__ via key)
       └── HasRowCol(Comparable, Hashable)
```

| Base | Responsibility |
|------|----------------|
| `Equatable` | Abstract `key` property, concrete `__eq__` |
| `Comparable` | `@total_ordering`, concrete `__lt__` |
| `Hashable` | Concrete `__hash__` via `hash(self.key)` |

## Dependencies

| Import | Purpose |
|--------|---------|
| `__future__.annotations` | Postponed evaluation of annotations |
| `f_core.mixins.comparable.Comparable` | Base — ordering operators |
| `f_core.mixins.hashable.Hashable` | Base — hashing |
| `typing.Self` | Self-type for `distance()` annotation |
| `typing.TYPE_CHECKING` | Guard for type-only imports |
| `f_math.shapes.Rect` | Type-only import for `is_within()` parameter |

## Usage Example

```python
from f_core.mixins.has.row_col import HasRowCol

zero = HasRowCol.Factory.zero()     # row=0, col=0
one = HasRowCol.Factory.one()       # row=1, col=1
twelve = HasRowCol.Factory.twelve()  # row=1, col=2

print(str(twelve))           # '(1,2)'
print(twelve.to_tuple())     # (1, 2)
print(zero < one)            # True
print(twelve.neighbors())    # [HasRowCol(0,2), HasRowCol(1,3), HasRowCol(2,2), HasRowCol(1,1)]
print(zero.distance(twelve)) # 3
```
