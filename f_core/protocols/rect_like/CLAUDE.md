# RectLike

## Purpose
Protocol for objects that can be converted to a min/max rectangle
representation. Used by `HasRowCol.is_within()` for bounds checking.

## Public API

### Protocol Methods
```python
def to_rect_coords(self) -> tuple[int, int, int, int]
```
Returns `(x_min, y_min, x_max, y_max)` as a tuple.

## Inheritance (Hierarchy)

```
Protocol
 └── RectLike
```

| Base | Responsibility |
|------|----------------|
| `Protocol` | Enables structural subtyping |

## Dependencies

| Import | Purpose |
|--------|---------|
| `typing.Protocol` | Base class for structural subtyping |

## Usage Example

```python
from f_core.protocols.rect_like import RectLike


def is_within(row: int, col: int, rect: RectLike) -> bool:
    x_min, y_min, x_max, y_max = rect.to_rect_coords()
    return x_min <= row <= x_max and y_min <= col <= y_max


# Any object with to_rect_coords() -> tuple[int,int,int,int] satisfies it
# e.g. f_math.shapes.Rect implements this protocol
```
