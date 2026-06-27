# FrontierFIFO

## Purpose
FIFO (First-In-First-Out) frontier. Used by BFS. Backed by a
`deque` for order and an auxiliary `set` for O(1) membership
check. Priority is accepted on `push` (for interface symmetry)
but ignored — order is insertion-only. FIFO has **no `decrease`
method and no `cnt_decrease` counter**; it carries only the
base 2-counter scaffold. The algo-level comparison surface
synthesizes the structural `cnt_decrease=0` for FIFO-backed
algos (e.g. BFS) so cross-algo benchmark tables stay rectangular.

## Public API

### Constructor
```python
def __init__(self) -> None
```
Calls `FrontierBase.__init__(self)` to wire the 2-counter
scaffold (`cnt_push`, `cnt_pop`), then sets up the `deque`
and membership `set`.

### Methods (from FrontierBase)
| Method | Complexity | Counter |
|--------|------------|---------|
| `push(state, priority=None)` | O(1) | `cnt_push` |
| `pop()` | O(1) | `cnt_pop` |
| `__contains__(state)` | O(1) | — |
| `__bool__()` | O(1) | — (inherited from `Sizable`, via `__len__`) |
| `__len__()` | O(1) | — |
| `clear()` | O(n) | counters preserved |

### Counters
Inherited from `FrontierBase` — the base 2-counter scaffold
(`cnt_push`, `cnt_pop`), incremented on the corresponding
methods. FIFO has no `decrease` op, so there is no
`cnt_decrease` counter on the frontier at all. The algo-level
comparison surface synthesizes the structural `cnt_decrease=0`
for FIFO-backed algos (e.g. BFS) to keep benchmark tables
rectangular.

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
