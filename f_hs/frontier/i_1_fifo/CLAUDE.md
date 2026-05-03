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
Calls `FrontierBase.__init__(self)` to wire the 3-counter
scaffold, then sets up the `deque` and membership `set`.

### Methods (from FrontierBase)
| Method | Complexity | Counter |
|--------|------------|---------|
| `push(state, priority=None)` | O(1) | `cnt_push` |
| `pop()` | O(1) | `cnt_pop` |
| `decrease(state, priority=None)` | no-op | none (counter does NOT increment) |
| `__contains__(state)` | O(1) | — |
| `__bool__()` | O(1) | — |
| `__len__()` | O(1) | — |
| `clear()` | O(n) | counters preserved |

### Counters
Inherited from `FrontierBase`. `cnt_push` and `cnt_pop`
increment on the corresponding methods; `cnt_decrease` stays
at 0 because `decrease` is the inherited no-op (counts reflect
what the frontier actually did, not what was called).

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
- `f_hs.frontier.i_0_base.FrontierBase` — provides the
  `Counters` scaffold via composition.
