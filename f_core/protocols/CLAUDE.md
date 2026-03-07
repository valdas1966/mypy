# Protocols Package

## Purpose
Collection of structural typing protocols that define behavioral contracts
for the mixin and data-structure layers. All protocols use `typing.Protocol`
for duck-typed type hints — no runtime inheritance required.

## Package Exports

```python
from f_core.protocols import (
    SupportsEquality,    # __eq__
    SupportsComparison,  # __lt__ (extends SupportsEquality)
    SupportsBounds,      # bounds property
)
from f_core.protocols.rect_like import RectLike  # to_rect_coords()
```

## Module Hierarchy

```
f_core/protocols/
├── __init__.py              re-exports 3 protocols
├── equality/                SupportsEquality — __eq__ contract
├── comparison/              SupportsComparison — __lt__ contract
├── bounds/                  SupportsBounds[T] — bounds property
└── rect_like/               RectLike — to_rect_coords() contract
```

## Module Summary

| Module | Protocol | Methods | Used By |
|--------|----------|---------|---------|
| `equality` | `SupportsEquality` | `__eq__` | `Equatable` mixin |
| `comparison` | `SupportsComparison` | `__lt__` (+ inherited `__eq__`) | `Comparable` mixin, `PriorityQueue` |
| `bounds` | `SupportsBounds[T]` | `bounds` property | (no consumers yet) |
| `rect_like` | `RectLike` | `to_rect_coords()` | `HasRowCol.is_within()` |

## Protocol Chain

```
Protocol
 ├── SupportsEquality          __eq__
 │    └── SupportsComparison   __lt__
 ├── SupportsBounds[T]         bounds property (T: int | float)
 └── RectLike                  to_rect_coords()
```

## Dependencies

All protocols depend only on `typing` stdlib. One exception:
- `SupportsBounds` uses `TYPE_CHECKING` guard for `f_ds.geometry.bounds.Bounds`.
- `SupportsComparison` imports `SupportsEquality` from sibling module.

## Usage Examples

### Type hint for equality
```python
from f_core.protocols import SupportsEquality

def are_equal(a: SupportsEquality, b: SupportsEquality) -> bool:
    return a == b
```

### Type hint for ordering
```python
from f_core.protocols import SupportsComparison

def is_sorted(items: list[SupportsComparison]) -> bool:
    return all(a <= b for a, b in zip(items, items[1:]))
```

### Bounds checking
```python
from f_core.protocols.rect_like import RectLike

def is_within(row: int, col: int, rect: RectLike) -> bool:
    x_min, y_min, x_max, y_max = rect.to_rect_coords()
    return x_min <= row <= x_max and y_min <= col <= y_max
```
