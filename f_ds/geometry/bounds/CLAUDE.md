# Bounds

## Purpose

Immutable generic container for rectangular bounds defined by four coordinates `(top, left, bottom, right)`. Generic over `int` or `float`. Used as the fundamental coordinate primitive for 2D positioning throughout the framework.

`Bounds` is **frame-agnostic** — the `Generic[int | float]` parameter
exists precisely so it can span integer grids and float canvases alike.
The `0-100` values in the `Factory` presets (`full`/`half`/`quarter`) are
an **`f_gui` canvas convention**, not a property of the `Bounds` type.

Inherits `Tupleable`, so identity, ordering, hashing and unpacking all
derive from `(top, left, bottom, right)` — two `Bounds` with the same
four coordinates are equal and hash-equal, usable as set members / dict
keys, and unpack as `t, l, b, r = bounds`.

## Public API

### Class Attributes

```python
Factory: type | None = None
```
Factory class for creating instances. Attached via `__init__.py`.

### Constructor

```python
def __init__(self,
             top: T,
             left: T,
             bottom: T,
             right: T) -> None
```
Stores four coordinates as private attributes. **No validation** — any
four `int`/`float` values are accepted (the `top <= bottom` /
`left <= right` asserts are intentionally disabled in the code).

### Properties

```python
@property
def top(self) -> T
```
Returns the top coordinate.

```python
@property
def left(self) -> T
```
Returns the left coordinate.

```python
@property
def bottom(self) -> T
```
Returns the bottom coordinate.

```python
@property
def right(self) -> T
```
Returns the right coordinate.

### Methods

```python
def anchor(self, side: Side) -> PointXY
```
Returns the **mid-point of the named edge** — a connection point of the
rectangle. `TOP`/`BOTTOM` → horizontal center on that edge; `LEFT`/`RIGHT`
→ vertical center. These are the four points a `Connector` attaches to
(via `Element.anchor`). `Side` comes from `f_ds.geometry.side`.

```python
def to_tuple(self) -> tuple[T, T, T, T]
```
Returns `(top, left, bottom, right)` as a tuple — the single `Tupleable`
method; also drives `key`, identity, ordering and iteration.

### Dunder Methods

```python
def __str__(self) -> str
```
Returns `'(top, left, bottom, right)'` — e.g. `'(0, 0, 100, 100)'`.

```python
def __repr__(self) -> str
```
Returns `'<Bounds: Top=0, Left=0, Bottom=100, Right=100>'` — a richer
override kept in place of `Tupleable`/`HasRepr`'s default.

```python
def __eq__ / __lt__ / __hash__          # via Tupleable, on the 4-tuple
def __iter__ / __getitem__ / __len__    # via Tupleable: t,l,b,r = bounds; bounds[0]; len==4
```

## Inheritance (Hierarchy)

```
Tupleable (eq + order + hash + iter via to_tuple)   Generic[T]
        └─────────────────────┬──────────────────────┘
                          Bounds[T]   # T: int | float
```

| Base | Responsibility |
|------|----------------|
| `Tupleable` | Identity, ordering, hashing, iteration via `to_tuple()` |
| `Generic[T]` | Type parameterization — constrains `T` to `int` or `float` |

Immutable value-record (the `Tupleable` immutability contract holds).

## Dependencies

| Import | Purpose |
|--------|---------|
| `f_core.mixins.Tupleable` | Identity / ordering / hashing / iteration via `to_tuple()` |
| `typing.Generic` | Generic type parameterization |
| `typing.TypeVar` | Defines `T` constrained to `int`, `float` |
| `f_ds.geometry.pointxy.PointXY` | Return type of `anchor()` |
| `f_ds.geometry.side.Side` | Edge selector for `anchor()` |

`PointXY` and `Side` are sibling geometry primitives (neither imports
`Bounds`, so there is no cycle).

## Usage Example

```python
from f_ds.geometry.bounds import Bounds

# Create bounds directly
b = Bounds(top=10, left=20, bottom=50, right=80)
print(b.top)        # 10
print(b.right)      # 80
print(b.to_tuple()) # (10, 20, 50, 80)
print(b)            # (10, 20, 50, 80)
```

### Using the Factory

```python
from f_ds.geometry.bounds import Bounds

full = Bounds.Factory.full()     # (0, 0, 100, 100)
print(full.to_tuple())           # (0, 0, 100, 100)
print(str(full))                 # (0, 0, 100, 100)
```

### Validation

`Bounds` performs **no validation**: inverted or off-frame rectangles are
legal (`Bounds(top=50, left=0, bottom=10, right=100)` constructs fine).
The ordering asserts in `__init__` are commented out by design — callers
own any frame/ordering invariants.
