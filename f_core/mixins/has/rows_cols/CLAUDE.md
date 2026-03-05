# HasRowsCols

## Purpose

Mixin for objects with `rows` and `cols` dimensions representing a 2D
shape. Provides shape string, bounds checking, flat length
(`rows * cols`), ordering, equality, and hashing via the framework's
`Comparable` and `Hashable` mixins.

## Public API

### Constructor

```python
def __init__(self,
             rows: int,
             cols: int | None = None) -> None
```
Stores `rows` and `cols`. If `cols` is `None`, defaults to the value
of `rows` (square shape).

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

```python
@property
def key(self) -> tuple[int, int]
```
Returns `(rows * cols, rows)`. Drives equality, comparison, and
hashing. Compares by total size first, then by rows.

### Methods

```python
def shape(self) -> str
```
Returns `'(rows,cols)'` string.

```python
def is_within(self, row: int, col: int) -> bool
```
Returns `True` if `0 <= row < rows` and `0 <= col < cols`.

### Dunder Methods

```python
def __len__(self) -> int
```
Returns `rows * cols` (flat length).

```python
def __str__(self) -> str
```
Returns `self.shape()`.

### Inherited

```python
def __eq__(self, other: object) -> bool   # from Equatable
def __lt__(self, other: object) -> bool   # from Comparable
def __le__(self, other: object) -> bool   # from Comparable
def __gt__(self, other: object) -> bool   # from Comparable
def __ge__(self, other: object) -> bool   # from Comparable
def __hash__(self) -> int                 # from Hashable
```
All delegate to `self.key` — the `(rows * cols, rows)` tuple.

## Inheritance (Hierarchy)

```
SupportsEquality (Protocol)
 └── Equatable ─── __eq__ via key
      ├── Comparable (+ SupportsComparison) ─── __lt__, __le__, __gt__, __ge__
      └── Hashable ─── __hash__ via key
           └── HasRowsCols(Comparable, Hashable)
                └── key = (rows * cols, rows)
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

## Usage Examples

### Basic Usage
```python
from f_core.mixins.has.rows_cols import HasRowsCols

grid = HasRowsCols(rows=3, cols=4)
print(grid.shape())           # '(3,4)'
print(len(grid))              # 12
print(grid.is_within(2, 3))   # True
print(grid.is_within(3, 4))   # False

square = HasRowsCols(rows=5)  # cols defaults to 5
print(square.shape())         # '(5,5)'
```

### Comparison and Hashing
```python
a = HasRowsCols(rows=3, cols=4)
b = HasRowsCols(rows=3, cols=4)
c = HasRowsCols(rows=4, cols=3)

a == b            # True (same key)
a < c             # True (12,3) < (12,4)
hash(a) == hash(b)  # True
{a, b} == {a}    # True — dedup works
```

### Factory
```python
from f_core.mixins.has.rows_cols import HasRowsCols

square  = HasRowsCols.Factory.square_3()    # (3,3)
rect    = HasRowsCols.Factory.rect_5_10()   # (5,10)
custom  = HasRowsCols.Factory.gen(rows=2, cols=7)  # (2,7)
```
