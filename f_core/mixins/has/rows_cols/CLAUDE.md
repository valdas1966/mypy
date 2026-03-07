# HasRowsCols

## Purpose

1. Mixin for objects with `rows` and `cols` dimensions representing a 2D shape.
2. Provides shape tuple, bounds checking, and flat length (`rows * cols`).
3. Standalone property mixin with no bases (like HasName, HasChildren, HasParent).

## Public API

### Class Attribute
```python
Factory: type = None
```
1. Factory for creating test instances. Wired via `__init__.py`.

### Constructor
```python
def __init__(self,
             rows: int,
             cols: int | None = None) -> None
```
1. Stores `rows` and `cols`.
2. If `cols` is `None`, defaults to the value of `rows` (square shape).

### Properties
```python
@property
def rows(self) -> int
```
1. Returns the number of rows.

```python
@property
def cols(self) -> int
```
1. Returns the number of columns.

### Methods
```python
def shape(self) -> tuple[int, int]
```
1. Returns `(rows, cols)` as a tuple.

```python
def is_within(self, row: int, col: int) -> bool
```
1. Returns `True` if `0 <= row < rows` and `0 <= col < cols`.

### Dunder Methods
```python
def __len__(self) -> int
```
1. Returns `rows * cols` (flat length).

```python
def __str__(self) -> str
```
1. Returns `'(rows,cols)'` string representation.

## Inheritance (Hierarchy)

```
HasRowsCols (plain class, no mixin bases)
```

## Dependencies

No external or internal dependencies.

## Usage Examples

### Basic Usage
```python
from f_core.mixins.has.rows_cols import HasRowsCols

grid = HasRowsCols(rows=5, cols=10)
print(grid.shape())           # (5, 10)
print(len(grid))              # 50
print(grid.is_within(4, 9))   # True
print(grid.is_within(5, 10))  # False

square = HasRowsCols(rows=3)  # cols defaults to 3
print(square.shape())         # (3, 3)
```

### Factory
```python
from f_core.mixins.has.rows_cols import HasRowsCols

square  = HasRowsCols.Factory.square_3()          # (3, 3)
rect    = HasRowsCols.Factory.rect_5_10()         # (5, 10)
custom  = HasRowsCols.Factory.gen(rows=2, cols=7) # (2, 7)
```
