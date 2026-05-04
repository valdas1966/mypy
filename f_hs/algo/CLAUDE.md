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
    │   — composes BPMXMixin with vanilla AStar.
    │     rule_pathmax ∈ {None, 1, 2, 3} (Felner numbering),
    │     depth_bpmx ∈ {None, 0, 1, 2, ...} for BPMX(d).
    │     Sibling of AStarLookup, not in chain.
    └── Dijkstra (h = 0)

AStarLookup
    └── AStarLookupBPMX (i_3_astar_lookup_bpmx/) — cache +
        bounds + propagate_pathmax + in-search BPMX in one
        pass; composes BPMXMixin with AStarLookup. Phase-2
        integration; used by k×A*-CB for OMSPP/MOSPP sub-search.
```

The shared in-search Felner mechanism lives in
`f_hs/algo/i_0_oospp/mixins/bpmx/main.py` (`BPMXMixin`). Both `AStarBPMX`
and `AStarLookupBPMX` inherit from it via MRO; the host class
just owns init validation and chain assembly.

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
├── __init__.py            Top-level lazy aggregator
├── _run_tests.py          Recursive test runner
├── CLAUDE.md              (this file)
├── i_0_oospp/             Variant-depth 0 — One-to-One SPP
│   ├── i_0_base/          AlgoSPP — abstract base
│   ├── i_1_bfs/           BFS — breadth-first search
│   ├── i_1_astar/         AStar — simple A*
│   ├── i_2_astar_lookup/  AStarLookup — cache + bounds
│   ├── i_2_astar_bpmx/    AStarBPMX — AStar + BPMXMixin
│   ├── i_2_dijkstra/      Dijkstra — A* with h=0
│   ├── i_3_astar_lookup_bpmx/
│   │                      AStarLookupBPMX — combined
│   └── mixins/bpmx/       BPMXMixin (Felner pathmax / BPMX(d))
├── i_1_omspp/             Variant-depth 1 — One-to-Many SPP
│   │                      (composes i_0_oospp algos as
│   │                       sub-searches; no inheritance)
│   ├── i_0_base/          AlgoOMSPP — orchestrator base
│   ├── i_1_kastar_inc/    KAStarInc
│   ├── i_1_kastar_agg/    KAStarAgg
│   ├── i_1_kbfs/          KBFS
│   └── i_2_kdijkstra/     KDijkstra
├── i_1_mospp/             (future) Many-to-One SPP
└── i_2_mmspp/             (future) Many-to-Many SPP
                           (composes both i_1_omspp and i_1_mospp)
```

## Variant Dependency DAG

The `i_X_VAR/` prefix at the top level encodes
**variant-composition depth** in the algo namespace, mirroring
how `i_X_NAME/` inside a variant folder encodes inheritance
depth. `i_0_*` is the kernel (no variant deps); `i_1_*` composes
`i_0_*`; `i_2_*` composes `i_1_*`.

```
              i_0_oospp/   (kernel — AlgoSPP, AStar*, BFS,
              ▲    ▲       Dijkstra; no variant deps)
              │    │
       ┌──────┘    └──────┐
       │                  │
   i_1_omspp/          i_1_mospp/    (compose i_0_oospp;
       │                  │           orchestrate sub-searches)
       └──────┐    ┌──────┘
              │    │
              ▼    ▼
              i_2_mmspp/    (composes i_1_omspp and i_1_mospp;
                             iterates one axis, delegates the
                             other)
```

The relationship between levels is **composition**, not
inheritance. `AlgoOMSPP` does NOT extend `AlgoSPP` — it
extends `f_cs.algo.Algo` directly and instantiates `AStar`
sub-searches internally. The `i_X_` numbering reflects "uses"
arrows, not class chains.

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
