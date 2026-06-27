# f_hs/algo/i_0_oospp — One-to-One SPP algorithms

## Purpose

Algorithms for the **One-to-One Shortest Path Problem** —
a single start, a single goal, one optimal path. Sibling
of `omspp/` (one-to-many) and the future `mospp/`
(many-to-one) under `f_hs/algo/`.

## Module Structure

```
oospp/
├── __init__.py             Lazy aggregator
├── CLAUDE.md               This file
├── mixins/                 OOSPP-scoped reusable mechanisms
│   └── bpmx/               BPMXMixin — Felner pathmax + BPMX(d)
├── i_0_base/               AlgoSPP — abstract base, classical search loop
├── i_1_bfs/                BFS — breadth-first search
├── i_1_astar/              AStar — simple A*
├── i_2_astar_lookup/       AStarLookup — cache + bounds + propagate_pathmax
├── i_2_dijkstra/           Dijkstra — A* with h=0
└── i_3_astar_bpmx/         AStarBPMX — AStarLookup + in-search BPMX
```

## Inheritance

```
AlgoSPP[State]                                — i_0_base/
├── BFS                                       — i_1_bfs/
└── AStar (simple; (f, -g, state))            — i_1_astar/
    ├── AStarLookup (cache + bounds +         — i_2_astar_lookup/
    │   │            propagate_pathmax)
    │   └── AStarBPMX (BPMXMixin)             — i_3_astar_bpmx/
    └── Dijkstra (h = 0)                      — i_2_dijkstra/
```

The shared `BPMXMixin` (in-search Felner pathmax / BPMX(d)
mechanism) lives at `f_hs/algo/i_0_oospp/mixins/bpmx/main.py`
and is consumed by `AStarBPMX` only. BPMX is intrinsically
OOSPP-scoped — it operates on a per-search-tree A* (single
source / single goal). Even when an OMSPP / MOSPP orchestrator
composes a BPMX-flavored sub-algo via the `_inner_algo_cls`
hook on `KAStarInc`, the BPMX mechanism still runs *inside*
the OOSPP sub-search. A multi-goal-aware BPMX variant (e.g.,
aggregate-Φ pathmax) would be a different mixin with
different math, not a reuse of this one.

## Package Exports

```python
from f_hs.algo.i_0_oospp import (
    AlgoSPP, SearchStateSPP,
    BFS, AStar, AStarLookup, AStarBPMX,
    Dijkstra,
)
# Or via the parent package:
from f_hs.algo import AStar          # same class, lazy-imported
from f_hs import AStar               # convenience top-level
```

## Why a sub-package

Before this restructuring, OOSPP algos sat at the algo/
namespace top level alongside `omspp/`. Asymmetric: OO was
implicit ("the default"), OM was an explicit folder. The
asymmetry would worsen as MOSPP and MMSPP arrive.

The current layout makes every immediate child of `algo/`
either a problem-variant folder (`oospp/`, `omspp/`, future
`mospp/`) or a shared utility (`_run_tests.py`,
`__init__.py`, `CLAUDE.md`). Discoverable, extensible, no
taxonomy-vs-implementation conflation. OOSPP-scoped mixins
(currently just `BPMXMixin`) live under `oospp/mixins/`.

## Class Naming

The class names retain the "SPP" stem (`AlgoSPP`,
`SolutionSPP`) rather than being renamed to "OOSPP" suffixes
— the umbrella term "SPP" is the framework's established
naming, and renaming would ripple through 80+ sites for
zero behavioral gain. Folder name (`oospp/`) reflects the
problem variant; class names keep the conventional stem.

## Counters

`AlgoSPP.counters` mirrors the injected frontier's heap-op
counts. `FrontierBase` owns only the 2-name scaffold
(`cnt_push`, `cnt_pop`); `FrontierPriority` adds `cnt_decrease`
via a `_COUNTER_NAMES` override (the decrease op and its
counter live only where the op does). FIFO frontiers have no
decrease op and no `cnt_decrease` counter — `AlgoSPP.counters`
**guards** the read and synthesizes a structural `0` for
FIFO-backed BFS, so the algo-level scaffold still exposes
`cnt_decrease` for every algo and the comparison grid stays
rectangular. Every concrete OOSPP algo (BFS, AStar,
AStarLookup, AStarBPMX, Dijkstra) exposes the same `counters`
surface.

Per-class scaffold overrides via `_COUNTER_NAMES`:

| Class | Names | Composition |
|---|---|---|
| `AlgoSPP` (default) | 8 | frontier 3 + search 2 + memory 3 (incl. `mem_total`) |
| `AStarLookup` | 13 | propagate 3 + frontier 3 + search 2 + memory 5 (`mem_open` / `mem_closed` / `mem_cache` / `mem_bounds` / `mem_total`) |
| `AStarBPMX` | 16 | propagate 3 + bpmx 3 + frontier 3 + search 2 + memory 5 |

The "frontier 3" group (`cnt_push`, `cnt_pop`, `cnt_decrease`)
is declared at the **algo level** for every algo, so the
cross-algo grid is rectangular. The frontier object itself
carries only the names for ops it has (FIFO: 2; Priority: 3);
`AlgoSPP.counters` synthesizes the missing `cnt_decrease=0` for
FIFO-backed BFS.

## Dependencies

- `f_hs.problem.ProblemSPP` — the (currently unified) SPP
  problem class.
- `f_hs.solution.SolutionSPP` — the OOSPP solution shape.
- `f_hs.frontier.{FrontierFIFO, FrontierPriority}` —
  injected per algo.
- `f_hs.heuristic.*` — heuristic chain layers (HBase,
  HCallable, HBounded, HCached).
- `f_hs.algo.i_0_oospp.mixins.bpmx.BPMXMixin` — composed
  by `AStarBPMX`.
