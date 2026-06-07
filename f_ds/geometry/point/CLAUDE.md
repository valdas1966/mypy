# Point

## Purpose

Lightweight 2-D point `(x, y)` value object in the normalized `0-100`
coordinate space used across the framework's geometry. `x` is the
horizontal axis (maps to CSS `left` / SVG `x`); `y` is the vertical axis
(maps to CSS `top` / SVG `y`). Equality and hashing are provided by the
`Hashable` mixin via the `(x, y)` key — so `Point`s are usable as set
members and dict keys.

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
@property
def key(self) -> tuple[float, float]       # (x, y) — eq + hash
```

### Methods

```python
def to_tuple(self) -> tuple[float, float]  # (x, y)
```

### Dunder Methods

```python
def __str__(self) -> str    # '(x, y)'
def __eq__(self, other) -> bool   # via Equatable (compares key)
def __hash__(self) -> int         # via Hashable (hashes key)
```

## Why Not Generic

`Bounds` is `Generic[T]` but carries no mixins. `Point` instead inherits
`Hashable` for equality/hashing. Combining `Generic[T]` with a mixin
(`Equatable`/`Hashable`) raises a metaclass `TypeError` in this codebase,
so `Point` is intentionally **non-generic** and uses `float`.

## Inheritance (Hierarchy)

```
Equatable ─── __eq__ via key
 └── Hashable ─── __hash__ via key
      └── Point  (key = (x, y))
```

## Dependencies

| Import | Purpose |
|--------|---------|
| `f_core.mixins.hashable.Hashable` | Equality + hashing via `key` |

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
