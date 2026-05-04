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

### Methods
| Method | Description |
|--------|-------------|
| `event_key() -> object` | Canonical comparable representation for recording-test normalizers. Default returns `self.key`. Override when the key isn't trivially comparable / readable in test output (see `StateCell.event_key()`). Consumed by `f_hs.algo.u_event_normalize.normalize(event)`. |

## Factory
| Method | Returns | Description |
|--------|---------|-------------|
| `a()` | `StateBase[str]` | Key = 'A' |
| `b()` | `StateBase[str]` | Key = 'B' |

## Dependencies
- `f_core.mixins.has.key.HasKey`
