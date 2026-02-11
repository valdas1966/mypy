# Bounds & SupportsBounds

## Purpose

Defines a `Bounds` NamedTuple for rectangular bounding boxes `(top, left, bottom, right)` and a `SupportsBounds` Protocol for objects that can provide their bounds. Generic over `int` or `float`.

This module contains two public symbols:
- **`Bounds`** — immutable data container (NamedTuple) for 4-coordinate bounds.
- **`SupportsBounds`** — structural protocol requiring a `bounds()` method.

## Public API

### Bounds (NamedTuple)

```python
class Bounds(NamedTuple, Generic[T]):  # T: int | float
    top: T
    left: T
    bottom: T
    right: T
```
Immutable named tuple. Inherits all tuple behavior (`__eq__`, indexing, unpacking, iteration).

### SupportsBounds (Protocol)

```python
class SupportsBounds(Protocol, Generic[T]):  # T: int | float
    def bounds(self) -> Bounds[T]: ...
```
Structural protocol — any class with a `bounds() -> Bounds[T]` method satisfies it without explicit inheritance.

## Inheritance (Hierarchy)

```
NamedTuple
 └── Bounds[T]          # T: int | float

Protocol
 └── SupportsBounds[T]  # T: int | float
```

| Base | Responsibility |
|------|----------------|
| `NamedTuple` | Provides immutable tuple semantics, field names, `__repr__`, `__eq__` |
| `Protocol` | Enables structural subtyping (duck typing with type hints) |
| `Generic[T]` | Parameterizes over `int` or `float` |

## Dependencies

| Import | Purpose |
|--------|---------|
| `typing.Protocol` | Base for structural subtyping |
| `typing.Generic` | Generic type parameterization |
| `typing.TypeVar` | Defines `T` constrained to `int`, `float` |
| `typing.NamedTuple` | Base for `Bounds` data container |

All dependencies are stdlib. No internal or third-party imports.

## Usage Example

```python
from f_core.protocols.bounds.main import Bounds, SupportsBounds


# Create bounds directly
b = Bounds(top=0, left=0, bottom=100, right=200)
print(b.top, b.right)  # 0 200

# Unpack like a tuple
top, left, bottom, right = b


# Use protocol as type hint
def area(obj: SupportsBounds[int]) -> int:
    b = obj.bounds()
    return (b.bottom - b.top) * (b.right - b.left)


# Any object with bounds() -> Bounds[int] satisfies the protocol
```

### Implemented By

- No implementations found in codebase yet.

## Questions / Ambiguities

1. **No `__init__.py`** — the module is not exported from `f_core.protocols`. Intentional?
2. **Naming collision** — `f_gui.layout.bounds.Bounds` is a completely different class (GUI layout utility). Could cause confusion.
3. **`bounds()` is a plain method, not a `@property`** — intentional deviation from the GUI `Bounds` which uses `@property`?
