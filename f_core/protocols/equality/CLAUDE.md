# SupportsEquality

## Purpose

Protocol defining the contract for objects that support equality checks via `__eq__`. Used as a type hint and base for classes that can be compared for equality.

Note: `__ne__()` is omitted; Python derives `!=` from `__eq__` by default.

## Public API

### Protocol Methods

```python
def __eq__(self, other: object) -> bool
```
Returns `True` if the object is equal to `other`.

## Inheritance (Hierarchy)

```
Protocol
 └── SupportsEquality
```

| Base | Responsibility |
|------|----------------|
| `Protocol` | Enables structural subtyping (duck typing with type hints) |

**Direct subclass:** `SupportsComparison` (`f_core.protocols.comparison`)

## Dependencies

| Import | Purpose |
|--------|---------|
| `typing.Protocol` | Base class for structural subtyping |

## Usage Example

```python
from f_core.protocols.equality import SupportsEquality


def are_equal(a: SupportsEquality, b: SupportsEquality) -> bool:
    return a == b


# Any object with __eq__ satisfies the protocol
are_equal("hello", "hello")  # True
are_equal(1, 2)              # False
```

### Implemented By

- `Equable` mixin (`f_core.mixins.equable`)
