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
| `push(state, priority)` | O(log n) | If State exists, decrease if better. Increments `counters['cnt_push']`. |
| `pop()` | O(log n) | Returns min-priority State. Increments `counters['cnt_pop']`. |
| `decrease(state, priority)` | O(log n) | No-op if new priority not better. Increments `counters['cnt_decrease']`. |
| `__contains__(state)` | O(1) | dict-backed |
| `__bool__()` | O(1) | inherited from `Sizable` (via `__len__`) |
| `__len__()` | O(1) | |
| `clear()` | O(n) | Does NOT reset counters. |

### Counters

The `_counters` instance and the `counters` read-only property
live on `FrontierBase`. `FrontierPriority` inherits the base
2-name scaffold (`cnt_push`, `cnt_pop`) and **extends it with
`cnt_decrease` via a `_COUNTER_NAMES` override** — it owns the
`decrease` op, so it owns the counter. All three names
(`cnt_push`, `cnt_pop`, `cnt_decrease`) are incremented here on
every call to the matching method.

- **By call-site, not internal op.** A `push` whose internal
  `QueueIndexed.push` falls through to `decrease_key`
  (because the state is already present) still increments
  `cnt_push`. The counter reflects what the algorithm
  *called*, not what the heap *did*.
- **Survive `clear()`.** Counters accumulate over the whole
  run, not over the heap state. `AlgoSPP.refresh_priorities`
  and `KAStarAgg._refresh_priorities` (which drain-and-rebuild)
  keep the running totals intact.
- **Reset only via a fresh instance.** No public `reset()` on
  the frontier — algorithms that want a clean count construct
  a new `FrontierPriority`.

The frontier is the **single source of truth** for heap-op
counts. Upstream algorithms read these values at end-of-run
(e.g., `AlgoOMSPP._sync_frontier_counters`) and mirror them
into a wider counter scaffold via `Counters.assign`. This
prevents drift between caller and callee.

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
- `f_hs.frontier.i_0_base.FrontierBase` — provides the base
  2-name `Counters` scaffold via composition; `FrontierPriority`
  extends it with `cnt_decrease`.
