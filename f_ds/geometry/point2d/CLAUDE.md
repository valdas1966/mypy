# Point2D

## Purpose

2-D **integer lattice** point `(row, col)` — a grid-coordinate value
object. A pure coordinate: equality, ordering, hashing, unpacking and
indexing come from the `Tupleable` mixin via the `(row, col)`
`to_tuple()`, so `Point2D`s are usable as set members, dict keys, and
unpack as `row, col = point`.

Introduced as the footgun-free coordinate type for the grid
**Connectivity** policy (`f_ds/grids/connectivity`). Unlike `HasRowCol`
(a behavior-rich *mixin*: `neighbors()`, `is_within()`, **Manhattan**
`distance()`), `Point2D` is a bare *value object* with **no grid
behavior** — so a Connectivity method that takes a `Point2D` can never
accidentally reach a stored Manhattan distance that would be inadmissible
on 8-connectivity. The 3-D twin (`Point3D`, `(row, col, level)`) is added
when 3-D connectivity work begins.

## Not To Be Confused With

| Type | Axes | Scalar | Kind | Domain |
|------|------|--------|------|--------|
| `Point2D` (here) | `row, col` | `int` | value object | grid lattice |
| `geometry.PointXY` | `x, y` | `float` | value object | GUI / rendering |
| `HasRowCol` | `row, col` | `int` | **mixin (role)** | grid cells |

## Public API

### Class Attributes

```python
Factory: type = None
```

### Constructor

```python
def __init__(self, row: int, col: int) -> None
```

### Properties

```python
@property
def row(self) -> int                       # vertical axis
@property
def col(self) -> int                       # horizontal axis
```
`key` is **not** defined here — inherited from `Tupleable`
(`key == to_tuple()`).

### Methods

```python
def to_tuple(self) -> tuple[int, int]      # (row, col) — the Tupleable method
```

### Dunder Methods

```python
def __str__(self) -> str          # '(row, col)'
def __eq__ / __lt__ / __hash__    # via Tupleable (compare/hash the (row, col) tuple)
def __iter__ / __getitem__ / __len__   # via Tupleable: row, col = point; point[0]; len==2
```

## Inheritance (Hierarchy)

```
Comparable, Hashable, HasRepr
 └── Tupleable ─── key = to_tuple()
      └── Point2D  (to_tuple() = (row, col))
```

## Dependencies

| Import | Purpose |
|--------|---------|
| `f_core.mixins.tupleable.Tupleable` | Equality, ordering, hashing, iteration via `to_tuple()` |

## Factory Presets

| Method   | Point2D  |
|----------|----------|
| `zero()` | `(0, 0)` |

## Usage Example

```python
from f_ds.geometry.point2d import Point2D

a = Point2D(row=1, col=2)
b = Point2D(row=1, col=2)
assert a == b
assert len({a, b}) == 1            # equal -> same hash
row, col = a                       # unpack via Tupleable
assert a.to_tuple() == (1, 2)
print(Point2D.Factory.zero())      # (0, 0)
```
