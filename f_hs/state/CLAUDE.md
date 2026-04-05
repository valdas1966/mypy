# StateBase

## Purpose
Base class for configurations in a search space. Wraps a generic
key with identity (equality, hashing) and ordering (comparison)
via HasKey. Domain subclasses add domain-specific behavior.

## Public API

### Constructor
```python
def __init__(self, key: Key) -> None
```

### Inherited from HasKey
| Member | Type | Description |
|--------|------|-------------|
| `key` | `Key` | The wrapped identifier |
| `__eq__` | | Equality via key |
| `__lt__` | | Ordering via key |
| `__hash__` | | Hashing via key |
| `__str__` | | `str(key)` |
| `__repr__` | | `<StateBase: Key=...>` |

## Type Parameters
- `Key` — any hashable, comparable type

## Inheritance
```
Equatable
  ├── Comparable (@total_ordering)
  └── Hashable
       └── HasKey[Key]
            └── StateBase[Key]
```

## Domain Subclasses (Examples)
| Subclass | Key Type | Domain |
|----------|----------|--------|
| `StateCell` | `CellMap` | 2D grid pathfinding |
| `StatePuzzle` | `tuple[int, ...]` | Sliding puzzles |
| `StateGraph` | `str` / `int` | Toy graphs |

## Dependencies
- `f_core.mixins.has.key.HasKey`
