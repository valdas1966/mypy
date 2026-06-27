# f_hs/frontier — Search Frontiers

## Purpose
Frontier data structures for search algorithms. Each subclass
wraps a specific container and exposes the shared
`FrontierBase` interface. The algorithm composes a frontier
via constructor injection — BFS holds a `FrontierFIFO`, A* and
Dijkstra hold a `FrontierPriority`.

## Architecture
```
FrontierBase[State]
    ├── FrontierFIFO[State]      (deque + set, FIFO)
    └── FrontierPriority[State]  (QueueIndexed, min-priority)
```

## Module Structure
```
frontier/
├── __init__.py         FrontierBase, FrontierFIFO, FrontierPriority
├── i_0_base/           FrontierBase — abstract
├── i_1_fifo/           FrontierFIFO — BFS frontier
└── i_1_priority/       FrontierPriority — A*/Dijkstra frontier
```

## Interface (FrontierBase)
| Method | Purpose |
|--------|---------|
| `push(state, priority=None)` | Add a State |
| `pop()` | Remove and return next State |
| `__contains__(state)` | Membership check |
| `__bool__()` | Non-empty? — inherited from `Sizable` (via `__len__`) |
| `__len__()` | Count |
| `__iter__()` | Iterate over pending states; order is implementation-defined |
| `clear()` | Empty the Frontier |

`decrease(state, priority=None)` is **not** part of the
`FrontierBase` interface — it lives only on `FrontierPriority`
(decrease-key on the indexed min-heap). FIFO has no decrease op.

`FrontierBase` inherits `f_core.mixins.Sizable`, which supplies
`__bool__` (emptiness) derived from `__len__` — so each frontier
declares its size in exactly one place (`__len__`) and `bool()`
follows. `Sizable` adds only `__bool__`/`Sized`; `__contains__`
and `__iter__` stay hand-declared (a frontier keeps a separate
O(1) membership index, so it is not a single-iterable wrapper).

Iteration order is not priority-sorted — it exists to let
`AlgoSPP.refresh_priorities` drain-and-rebuild the frontier
when an injected seed has stale priorities.

## Design Decisions
- **Priority is computed by the Algorithm, not the Frontier.**
  The frontier only knows "priorities are comparable." This keeps
  AStar's `(f, -g, state)` tuple logic in AStar and keeps the
  frontier dumb.
- **Uniform signature across subclasses.** FIFO accepts a
  `priority` argument for interface symmetry and ignores it.
- **`decrease` is Priority-only — hierarchy honesty.** The base
  has neither a `decrease` method nor a `cnt_decrease` counter
  (2-name scaffold: `cnt_push`, `cnt_pop`). `FrontierFIFO` is
  insertion-order only and visibly carries no decrease op;
  `FrontierPriority` owns both the `decrease` method and the
  `cnt_decrease` counter (added via a `_COUNTER_NAMES`
  override). The algo-level comparison surface synthesizes the
  structural `cnt_decrease=0` for FIFO-backed algos (e.g. BFS)
  so cross-algo benchmark tables stay rectangular.
