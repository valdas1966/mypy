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
├── i_2_astar_bpmx/         AStarBPMX — AStar + BPMXMixin (Felner pathmax / BPMX(d))
├── i_2_dijkstra/           Dijkstra — A* with h=0
└── i_3_astar_lookup_bpmx/  AStarLookupBPMX — AStarLookup + BPMXMixin (combined)
```

## Inheritance

```
AlgoSPP[State]                                — i_0_base/
├── BFS                                       — i_1_bfs/
└── AStar (simple; (f, -g, state))            — i_1_astar/
    ├── AStarLookup (cache + bounds)          — i_2_astar_lookup/
    │     └── AStarLookupBPMX (cache+bounds   — i_3_astar_lookup_bpmx/
    │                          + BPMXMixin)
    ├── AStarBPMX (BPMXMixin + AStar)         — i_2_astar_bpmx/
    └── Dijkstra (h = 0)                      — i_2_dijkstra/
```

The shared `BPMXMixin` (in-search Felner pathmax / BPMX(d)
mechanism) lives at `f_hs/algo/i_0_oospp/mixins/bpmx/main.py`.
BPMX is intrinsically OOSPP-scoped — it operates on a
per-search-tree A* (single source / single goal). Even when
an OMSPP / MOSPP orchestrator composes a BPMX-flavored
sub-algo via the `_inner_algo_cls` hook on `KAStarInc`, the
BPMX mechanism still runs *inside* the OOSPP sub-search.
A multi-goal-aware BPMX variant (e.g., aggregate-Φ pathmax)
would be a different mixin with different math, not a reuse
of this one.

## Package Exports

```python
from f_hs.algo.i_0_oospp import (
    AlgoSPP, SearchStateSPP,
    BFS, AStar, AStarLookup, AStarBPMX, AStarLookupBPMX,
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

`AlgoSPP.counters` is a delegation property returning
`self._search.frontier.counters` — the 3-name `Counters`
scaffold (`cnt_push`, `cnt_pop`, `cnt_decrease`) owned by
`FrontierBase`. Every concrete OOSPP algo (BFS, AStar,
AStarLookup, Dijkstra) inherits the same `counters` surface.

`AStarBPMX` and `AStarLookupBPMX` override via `BPMXMixin`
to expose a 10-counter scaffold (pathmax 2 + bpmx 5 +
frontier 3 mirrored from FrontierPriority).

## Dependencies

- `f_hs.problem.ProblemSPP` — the (currently unified) SPP
  problem class.
- `f_hs.solution.SolutionSPP` — the OOSPP solution shape.
- `f_hs.frontier.{FrontierFIFO, FrontierPriority}` —
  injected per algo.
- `f_hs.heuristic.*` — heuristic chain layers (HBase,
  HCallable, HBounded, HCached).
- `f_hs.algo.i_0_oospp.mixins.bpmx.BPMXMixin` — composed by the two
  BPMX-flavored classes.
