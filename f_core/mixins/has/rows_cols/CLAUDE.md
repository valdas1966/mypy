# HasRowsCols

## Purpose

Mixin for objects with `rows` and `cols` dimensions representing a 2D shape. Provides shape string, bounds checking, length (rows * cols), and hashing.

## Public API

### Constructor

```python
def __init__(self, rows: int, cols: int = None) -> None
```
Stores `rows` and `cols`. If `cols` is falsy, defaults to the value of `rows` (square shape).

### Properties

```python
@property
def rows(self) -> int
```
Returns the number of rows.

```python
@property
def cols(self) -> int
```
Returns the number of columns.

### Methods

```python
def shape(self) -> str
```
Returns `'(rows,cols)'` string.

```python
def is_within(self, row: int, col: int) -> bool
```
Returns `True` if `0 <= row < rows` and `0 <= col < cols`.

```python
def key_comparison(self) -> list
```
Returns `[len(self), self.rows]`. First compares by total size, then by rows.

### Dunder Methods

```python
def __len__(self) -> int
```
Returns `rows * cols` (flat length).

```python
def __str__(self) -> str
```
Returns `self.shape()`.

```python
def __hash__(self) -> int
```
Returns `hash((self.rows, self.cols))`.

## Inheritance (Hierarchy)

```
HasRowsCols (plain class, no mixin bases)
```

## Dependencies

| Import | Purpose |
|--------|---------|
| `__future__.annotations` | Postponed evaluation of annotations |

## Usage Example

```python
from f_core.mixins.has.rows_cols import HasRowsCols

grid = HasRowsCols(rows=3, cols=4)
print(grid.shape())        # '(3,4)'
print(len(grid))           # 12
print(grid.is_within(2, 3))  # True
print(grid.is_within(3, 4))  # False

square = HasRowsCols(rows=5)  # cols defaults to 5
print(square.shape())      # '(5,5)'
```
