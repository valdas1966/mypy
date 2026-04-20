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
| `decrease(state, priority=None)` | Update priority of existing State (decrease-only on FrontierPriority) |
| `__contains__(state)` | Membership check |
| `__bool__()` | Non-empty? |
| `__len__()` | Count |
| `__iter__()` | Iterate over pending states; order is implementation-defined |
| `clear()` | Empty the Frontier |

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
- **`decrease` default is no-op** on the base, so BFS-style
  frontiers inherit it without override.
