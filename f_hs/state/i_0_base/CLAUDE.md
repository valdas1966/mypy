# StateBase

## Purpose
Base class for configurations in a search space. Wraps a generic
key with identity (equality, hashing) and ordering via HasKey.

## Public API

### Constructor
```python
def __init__(self, key: Key) -> None
```

### Inherited from HasKey
| Member | Description |
|--------|-------------|
| `key` | The wrapped identifier |
| `__eq__`, `__lt__`, `__hash__` | Via key |
| `__str__` | `str(key)` |

## Factory
| Method | Returns | Description |
|--------|---------|-------------|
| `a()` | `StateBase[str]` | Key = 'A' |
| `b()` | `StateBase[str]` | Key = 'B' |

## Dependencies
- `f_core.mixins.has.key.HasKey`
