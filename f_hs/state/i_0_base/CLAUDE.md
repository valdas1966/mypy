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
No own methods beyond the `HasKey` surface. Canonical
identity-rendering for recording tests / visualization is no
longer a per-State method: it is the free function
`f_core.canonize.canonize`, which descends `HasKey` → `.key`
automatically (the old `event_key()` was deleted 2026-06-20).

## Factory
| Method | Returns | Description |
|--------|---------|-------------|
| `a()` | `StateBase[str]` | Key = 'A' |
| `b()` | `StateBase[str]` | Key = 'B' |

## Dependencies
- `f_core.mixins.has.key.HasKey`
