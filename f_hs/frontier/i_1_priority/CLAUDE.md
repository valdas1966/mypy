# FrontierPriority

## Purpose
Priority-ordered frontier backed by `QueueIndexed` (indexed
min-heap with decrease_key). Each State appears at most once.
Used by A* and Dijkstra. Priorities are tuples compared
lexicographically — the Algorithm decides the shape
(e.g., `(f, -g, state)` for A*).

## Public API

### Constructor
```python
def __init__(self) -> None
```

### Methods (from FrontierBase)
| Method | Complexity | Notes |
|--------|------------|-------|
| `push(state, priority)` | O(log n) | If State exists, decrease if better |
| `pop()` | O(log n) | Returns min-priority State |
| `decrease(state, priority)` | O(log n) | No-op if new priority not better |
| `__contains__(state)` | O(1) | dict-backed |
| `__bool__()` | O(1) | |
| `__len__()` | O(1) | |
| `clear()` | O(n) | |

## Factory
| Method | Description |
|--------|-------------|
| `empty()` | Empty FrontierPriority |
| `abc()` | A(3), B(1), C(2) — pops B, C, A |

## Inheritance
```
FrontierBase[State]
    └── FrontierPriority[State]
```

## Dependencies
- `f_ds.queues.i_1_indexed.QueueIndexed`
- `f_hs.frontier.i_0_base.FrontierBase`
