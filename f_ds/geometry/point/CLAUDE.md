# Point

## Purpose

Lightweight 2-D point `(x, y)` value object in the normalized `0-100`
coordinate space used across the framework's geometry. `x` is the
horizontal axis (maps to CSS `left` / SVG `x`); `y` is the vertical axis
(maps to CSS `top` / SVG `y`). Equality, ordering, hashing, unpacking and
indexing are provided by the `Tupleable` mixin via the `(x, y)`
`to_tuple()` — so `Point`s are usable as set members, dict keys, and
unpack as `x, y = point`.

Introduced as the endpoint primitive for `f_gui`'s `Line` element, but is
general-purpose geometry.

## Public API

### Class Attributes

```python
Factory: type = None
```

### Constructor

```python
def __init__(self, x: float, y: float) -> None
```

### Properties

```python
@property
def x(self) -> float                       # horizontal (0-100)
@property
def y(self) -> float                       # vertical (0-100)
```
`key` is **not** defined here — it is inherited from `Tupleable`
(`key == to_tuple()`).

### Methods

```python
def to_tuple(self) -> tuple[float, float]  # (x, y) — the single Tupleable method
```
`to_tuple()` is the data-tuple accessor shared across the framework's
2-slot value objects (`HasRowCol.to_tuple()`); under
`Tupleable` it also drives identity, ordering and iteration.

### Dunder Methods

```python
def __str__(self) -> str          # '(x, y)'
def __eq__ / __lt__ / __hash__    # via Tupleable (compare/hash the (x, y) tuple)
def __iter__ / __getitem__ / __len__   # via Tupleable: x, y = point; point[0]; len==2
```

## Why Not Generic

`Point` is intentionally **non-generic** and uses `float` — a deliberate
domain choice, not a technical limitation. Geometry coordinates in this
framework live in the normalized `0-100` `float` space, so there is no
type to parameterize over (YAGNI). `Generic[T]` *does* compose with the
mixins here — `Bounds(Tupleable, Generic[T])` is a live, subclassed
example — so genericity was an option that was simply not needed.

## Inheritance (Hierarchy)

```
Comparable, Hashable, HasRepr
 └── Tupleable ─── key = to_tuple()
      └── Point  (to_tuple() = (x, y))
```

## Dependencies

| Import | Purpose |
|--------|---------|
| `f_core.mixins.tupleable.Tupleable` | Equality, ordering, hashing, iteration via `to_tuple()` |

## Factory Presets

| Method     | Point      |
|------------|------------|
| `origin()` | `(0, 0)`   |
| `center()` | `(50, 50)` |
| `end()`    | `(100, 100)`|

## Usage Example

```python
from f_ds.geometry.point import Point

a = Point(x=10, y=20)
b = Point(x=10, y=20)
assert a == b
assert len({a, b}) == 1            # equal -> same hash
assert a.to_tuple() == (10, 20)
print(Point.Factory.center())      # (50, 50)
```
