# f_hs/algo — Search Algorithms

## Purpose
Search algorithms for Shortest-Path-Problem. Built on top of
`AlgoSPP`, which owns the classical search loop and composes a
`FrontierBase` via constructor injection. Subclasses pick a
frontier (`FrontierFIFO` for BFS, `FrontierPriority` for A*) and
override `_priority(state)` if needed.

## Architecture
```
AlgoSPP (loop + SearchState + recording + path + Frontier)
├── BFS                                      — FrontierFIFO
└── AStar (simple; (f, -g, state))           — FrontierPriority
    ├── AStarLookup (cache + bounds; (f, -g, cache_rank, state))
    │   — HCached early-term, HBounded admissible bounds,
    │     to_cache harvest, suffix-stitched reconstruct_path,
    │     pre-search propagate_pathmax.
    ├── AStarBPMX (in-search Felner pathmax + BPMX(d) cascade)
    │   — rule_pathmax ∈ {None, 1, 2, 3} (Felner numbering),
    │     depth_bpmx ∈ {None, 0, 1, 2, ...} for BPMX(d).
    │     Sibling of AStarLookup, not in chain. A Phase-2
    │     integration class will combine cache/bounds with BPMX.
    └── Dijkstra (h = 0)
```

The dynamic per-search bundle (frontier, g, parent, closed,
goal_reached) is held as a single `SearchStateSPP` dataclass on
`AlgoSPP._search`, exposed read-only via the `search_state`
property. `AlgoSPP.resume()` continues the loop without
reinitializing the bundle — the foundation for OMSPP-iterative
multi-goal pumping and bidirectional search.

**Counters** — `AlgoSPP.counters` is a delegation property
returning `self._search.frontier.counters`. The injected
frontier (FIFO or Priority) owns the 3-name `Counters`
scaffold (`cnt_push`, `cnt_pop`, `cnt_decrease`) inherited
from `FrontierBase`. Every concrete SPP algorithm (BFS,
AStar, AStarLookup, Dijkstra) inherits the same `counters`
surface — single declaration on `AlgoSPP`, single source of
truth on the frontier. FIFO frontiers report `cnt_decrease=0`
since `decrease` is a no-op on FIFO.

## Module Structure
```
algo/
├── __init__.py          AlgoSPP, BFS, AStar, AStarLookup,
│                        AStarBPMX, Dijkstra
├── i_0_base/            AlgoSPP — abstract base
├── i_1_bfs/             BFS — breadth-first search
├── i_1_astar/           AStar — simple A*, __new__ dispatcher
├── i_2_astar_lookup/    AStarLookup — cache + bounds + pathmax
├── i_2_astar_bpmx/      AStarBPMX — Felner pathmax + BPMX(d)
└── i_2_dijkstra/        Dijkstra — A* with h=0
```

## Classical Search Loop (in AlgoSPP)
```
FRONTIER ← {start}
while FRONTIER:
    n ← FRONTIER.pop_min()
    if n is goal: return cost
    CLOSED ← CLOSED ∪ {n}
    for each child of n:
        if child in CLOSED: skip
        w ← problem.w(n, child)
        if child not in FRONTIER: insert
        else if new_g < g(child): decrease
```

## Subclass Differences
| | BFS | AStar (simple) | AStarLookup | Dijkstra |
|--|-----|-----|-----|----------|
| Frontier | FIFO | Priority | Priority (inherited) | Priority (inherited) |
| `_priority` | None | `(f,-g,state)` | `(f,-g,cache_rank,state)` | `(g,-g,state)` |
| Heuristic | none | HBase / Callable | HCached / HBounded / either | h=0 |
| `_enrich_event` | no-op | h, f | + is_cached, is_bounded, propagate | no-op (drops h, f) |
| search_state | inherited | routes to Pro | accepts, refreshes | forwards to AlgoSPP |
| Pro methods | — | — | to_cache, propagate_pathmax, suffix stitch | — |

The `state` component (tertiary tie-break) relies on `State`'s
`Comparable` ordering (via `HasKey`) and keeps expansion order
deterministic when `(f, -g)` ties — crucial for recording tests.
Dijkstra overrides `_enrich_event` to drop `h` and `f` (constant
and derivable, respectively) so its events schema-match BFS.

## Edge Costs
`problem.w(parent, child)` returns the edge cost. Default 1.0.
Subclasses of `ProblemSPP` override for weighted graphs.
