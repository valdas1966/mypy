# SupportsBounds

## Purpose

Protocol defining the contract for objects that have rectangular bounds. Used as a type hint for any object that can provide its bounding box as a `(top, left, bottom, right)` tuple. Generic over `int` or `float`.

## Public API

### Protocol Methods

```python
def bounds(self) -> tuple[T, T, T, T]
```
Returns the bounds of the object as a tuple `(top, left, bottom, right)`. `T` is constrained to `int` or `float`.

## Inheritance (Hierarchy)

```
Protocol
 └── SupportsBounds[T]    # T: int | float
```

| Base | Responsibility |
|------|----------------|
| `Protocol` | Enables structural subtyping (duck typing with type hints) |
| `Generic[T]` | Parameterizes bound values over `int` or `float` |

## Dependencies

| Import | Purpose |
|--------|---------|
| `typing.Protocol` | Base class for structural subtyping |
| `typing.Generic` | Enables generic type parameterization |
| `typing.TypeVar` | Defines `T` constrained to `int`, `float` |

## Usage Example

```python
from f_core.protocols.bounds import SupportsBounds


def is_within(row: int, col: int, obj: SupportsBounds[int]) -> bool:
    top, left, bottom, right = obj.bounds()
    return top <= row <= bottom and left <= col <= right


# Any object with a bounds() -> tuple[int, int, int, int] satisfies the protocol
```
