# ProblemAlgo

## Purpose
Abstract base class for algorithm problem definitions.
Provides named identity and equality via `HasName` + `Equatable`.

## Public API

### Constructor
```python
def __init__(self, name: str = 'ProblemAlgo') -> None
```

### Properties
| Property | Type | Description |
|----------|------|-------------|
| `name` | `str` | Problem name (inherited from HasName) |
| `key` | `SupportsEquality` | Abstract — subclasses must implement |

### Inherited
- `__eq__`, `__ne__`, `__hash__` via `key` (from Equatable)
- `__str__` returns `name` (from HasName)

## Inheritance
```
HasName + Equatable
    └── ProblemAlgo
```

## Dependencies
- `f_core.mixins.Equatable`
- `f_core.mixins.has.name.HasName`
- `f_core.protocols.equality.SupportsEquality`
