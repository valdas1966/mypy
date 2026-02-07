# SupportsComparison

## Purpose

Protocol defining the contract for objects that support comparison operations (`<`, `<=`, `>`, `>=`). Extends `SupportsEquality` to include ordering.

Note: `@total_ordering` decorator in concrete classes will automatically generate `<=`, `>`, `>=` from `__lt__()` and `__eq__()`.

## Public API

### Protocol Methods

```python
def __lt__(self, other: object) -> bool
```
Returns `True` if the object is less than `other`.

### Inherited from SupportsEquality

```python
def __eq__(self, other: object) -> bool
```
Returns `True` if the object is equal to `other`.

## Inheritance (Hierarchy)

```
Protocol
 └── SupportsEquality
      └── SupportsComparison
```

| Base | Responsibility |
|------|----------------|
| `Protocol` | Enables structural subtyping |
| `SupportsEquality` | Provides `__eq__` contract |

## Dependencies

| Import | Purpose |
|--------|---------|
| `typing.Protocol` | Base class for structural subtyping |
| `f_core.protocols.equality.SupportsEquality` | Base protocol for equality |

## Usage Example

```python
from f_core.protocols.comparison import SupportsComparison


def is_smaller(a: SupportsComparison, b: SupportsComparison) -> bool:
    return a < b


# Any object with __lt__ and __eq__ satisfies the protocol
is_smaller(1, 2)        # True
is_smaller("a", "b")    # True
```

### Implemented By

- `Comparable` mixin (`f_core.mixins.comparable`)
