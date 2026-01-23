# priority - Priority Classes for Search State Ordering

## Purpose
Defines a hierarchy of priority classes used to order states in the search open-list. Each level adds an additional dimension to the comparison tuple, enabling progressively richer tie-breaking strategies.

## Structure

```
PriorityKey (i_0_key)
  └─ PriorityG (i_1_g)
       └─ PriorityGH (i_2_gh)
            └─ PriorityGHFlags (i_3_gh_flags)
```

- **i_0_key/** - Base priority: comparison by key only
- **i_1_g/** - Adds g-value: maximizes path cost (higher g = higher priority)
- **i_2_gh/** - Adds h-value: minimizes f=g+h, breaks ties with g
- **i_3_gh_flags/** - Adds is_cached/is_bounded flags between f and g tiebreakers

## Comparison Tuples

Each level defines `key_comparison()` returning a tuple used by the `Comparable` mixin:

| Class | Comparison Tuple | Semantics |
|-------|-----------------|-----------|
| PriorityKey | `(key)` | Identity only |
| PriorityG | `(-g, key)` | Maximize g |
| PriorityGH | `(g+h, -g, key)` | Minimize f, then maximize g |
| PriorityGHFlags | `(g+h, !cached, !bounded, -g, key)` | Minimize f, prefer cached, prefer bounded, then maximize g |

## Design Patterns

### Incremental Inheritance
Each level inherits from the previous, adding one concept. The `i_X_` prefix encodes the inheritance depth.

### Comparable via key_comparison()
All classes implement `key_comparison()` which returns a tuple. The `Comparable` mixin (from f_core) uses this tuple for `<`, `>`, `==` operators.

### Factory Attachment
Factories are defined in `_factory.py` and attached via monkey-patching in `__init__.py` to avoid circular imports:
```python
PriorityGH.Factory = Factory
```

## Relationship to Other Data Structures

- **Cost** (in `ds/cost/`): An older/alternative approach to state priority
- **Generated** (in `ds/generated/`): Uses priority objects to order the open-list
- **StateBase** (in `ds/state/`): States are identified by their key, which is the same key stored in priority objects

## External Dependencies

- **f_core.mixins.Comparable** - Provides comparison operators via `key_comparison()`
