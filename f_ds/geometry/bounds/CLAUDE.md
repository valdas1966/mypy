# Bounds

## Purpose

Immutable generic container for rectangular bounds defined by four coordinates `(top, left, bottom, right)`. Generic over `int` or `float`. Validates that `top <= bottom` and `left <= right` at construction time. Used as the fundamental coordinate primitive for 2D positioning throughout the framework.

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
Stores four coordinates as private attributes. Asserts `top <= bottom` and `left <= right`.

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
def anchor(self, side: Side) -> Point
```
Returns the **mid-point of the named edge** — a connection point of the
rectangle. `TOP`/`BOTTOM` → horizontal center on that edge; `LEFT`/`RIGHT`
→ vertical center. These are the four points a `Connector` attaches to
(via `Element.anchor`). `Side` comes from `f_ds.geometry.side`.

```python
def to_tuple(self) -> tuple[T, T, T, T]
```
Returns `(top, left, bottom, right)` as a tuple.

### Dunder Methods

```python
def __str__(self) -> str
```
Returns `'(top, left, bottom, right)'` — e.g. `'(0, 0, 100, 100)'`.

```python
def __repr__(self) -> str
```
Returns `'<Bounds: Top=0, Left=0, Bottom=100, Right=100>'`.

## Inheritance (Hierarchy)

```
Generic[T]
 └── Bounds[T]  # T: int | float
```

| Base | Responsibility |
|------|----------------|
| `Generic[T]` | Type parameterization — constrains `T` to `int` or `float` |

No mixins. Pure immutable data container.

## Dependencies

| Import | Purpose |
|--------|---------|
| `typing.Generic` | Generic type parameterization |
| `typing.TypeVar` | Defines `T` constrained to `int`, `float` |
| `f_ds.geometry.point.Point` | Return type of `anchor()` |
| `f_ds.geometry.side.Side` | Edge selector for `anchor()` |

`Point` and `Side` are sibling geometry primitives (neither imports
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

```python
from f_ds.geometry.bounds import Bounds

# This raises AssertionError: top must be <= bottom
b = Bounds(top=50, left=0, bottom=10, right=100)
```
