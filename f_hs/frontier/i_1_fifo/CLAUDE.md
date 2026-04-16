# FrontierFIFO

## Purpose
FIFO (First-In-First-Out) frontier. Used by BFS. Backed by a
`deque` for order and an auxiliary `set` for O(1) membership
check. Priority is accepted on `push` (for interface symmetry)
but ignored. `decrease` is a no-op inherited from `FrontierBase`.

## Public API

### Constructor
```python
def __init__(self) -> None
```

### Methods (from FrontierBase)
| Method | Complexity |
|--------|------------|
| `push(state, priority=None)` | O(1) |
| `pop()` | O(1) |
| `decrease(state, priority=None)` | no-op |
| `__contains__(state)` | O(1) |
| `__bool__()` | O(1) |
| `__len__()` | O(1) |
| `clear()` | O(n) |

## Factory
| Method | Description |
|--------|-------------|
| `empty()` | Empty FrontierFIFO |
| `abc()` | FrontierFIFO with A, B, C pushed in order |

## Inheritance
```
FrontierBase[State]
    └── FrontierFIFO[State]
```

## Dependencies
- `collections.deque` (stdlib)
- `f_hs.frontier.i_0_base.FrontierBase`
