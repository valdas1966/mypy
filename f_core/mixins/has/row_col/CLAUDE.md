# HasRowCol

## Purpose
1. Mixin that gives objects `row` and `col` properties for 2D grid position.
2. Provides comparison (row-major), hashing, neighbor discovery, Manhattan distance, bounds checking.
3. All operators derived from the `(row, col)` key pair.

## Public API

### Class Attribute
```python
Factory: type = None
```
1. Factory for creating test instances. Wired via `__init__.py`.

### Constructor
```python
def __init__(self, row: int | None = None, col: int | None = None) -> None:
```
1. Sets `_row` and `_col`.
2. `row=None` defaults to `0`.
3. `col=None` defaults to the value of `row`.

### Properties
```python
@property
def row(self) -> int:
```
1. Returns the object's row (read-only).

```python
@property
def col(self) -> int:
```
1. Returns the object's column (read-only).

```python
@property
def key(self) -> tuple[int, int]:
```
1. Returns `(row, col)` — row-major order.
2. Satisfies the abstract `key` contract from `Comparable`/`Hashable`.

### Methods
```python
def neighbors(self) -> list[Self]:
```
1. Returns up to 4 neighbors in clock-wise order (N, E, S, W).
2. Filters out positions with negative row or col.

```python
def distance(self, other: Self) -> int:
```
1. Returns Manhattan distance: `|row_diff| + |col_diff|`.

```python
def is_within(self, rect: SupportsBounds = None, row_min: int = None, col_min: int = None, row_max: int = None, col_max: int = None) -> bool:
```
1. Returns `True` if position is inside the given `rect` or explicit min/max bounds.
2. If `rect` is provided, extracts bounds via `rect.to_min_max()`.

### Dunder Methods
```python
def __str__(self) -> str:
```
1. Returns `'(row,col)'`.

```python
def __repr__(self) -> str:
```
1. Returns `'<HasRowCol: Row=1, Col=2>'`.

### Inherited
```python
def __eq__(self, other: object) -> bool:    # from Equatable
def __lt__(self, other: object) -> bool:    # from Comparable
def __le__(self, other: object) -> bool:    # from Comparable
def __gt__(self, other: object) -> bool:    # from Comparable
def __ge__(self, other: object) -> bool:    # from Comparable
def __hash__(self) -> int:                  # from Hashable
```
1. All delegate to `self.key` — the `(row, col)` tuple.

## Inheritance (Hierarchy)

```
SupportsEquality (Protocol)
 └── Equatable (__eq__ via key)
      ├── Comparable (__lt__, __le__, __gt__, __ge__)
      └── Hashable (__hash__ via key)
           └── HasRowCol(Comparable, Hashable)
```

| Base         | Responsibility                              |
|--------------|---------------------------------------------|
| `Equatable`  | Abstract `key` property, concrete `__eq__`  |
| `Comparable` | Comparison operators via `key`              |
| `Hashable`   | `__hash__` via `hash(self.key)`             |

## Dependencies

| Import                                | Purpose                                  |
|---------------------------------------|------------------------------------------|
| `__future__.annotations`              | Postponed annotation evaluation          |
| `f_core.mixins.comparable.Comparable` | Base — ordering operators                |
| `f_core.mixins.hashable.Hashable`     | Base — hashing                           |
| `f_core.protocols.bounds.SupportsBounds` | Protocol for `is_within()` rect param |
| `typing.Self`                         | Self-type for `neighbors()`, `distance()`|

## Usage Example

```python
from f_core.mixins.has.row_col import HasRowCol

zero   = HasRowCol.Factory.zero()      # (0,0)
one    = HasRowCol.Factory.one()       # (1,1)
twelve = HasRowCol.Factory.twelve()    # (1,2)

zero < one                # True (row-major)
hash(zero) != hash(one)   # True
twelve.neighbors()        # [(0,2), (1,3), (2,2), (1,1)]
zero.distance(twelve)     # 3
```
