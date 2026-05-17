# f_hs/algo/i_1_mospp — Many-to-One SPP algorithms

## Purpose

Algorithms for the **Many-to-One Shortest Path Problem
(MOSPP)**: find `k` shortest paths from each of `k` start
states `[s₁, ..., sₖ]` to a shared single goal `t`.

Sibling of `i_1_omspp/` (One-to-Many SPP). The two scopes
are mirror images:

| | OMSPP | MOSPP |
|---|---|---|
| Problem shape | 1 start, k goals | k starts, 1 goal |
| Solution | `{goal: SolutionSPP}` | `{start: SolutionSPP}` |
| Iteration axis | `problem.goals` | `problem.starts` |
| h closure | per sub-search (over current goal) | once, over fixed goal |
| Sub-search marker | `on_goal` event | `on_start` event |

MOSPP algorithms orchestrate multiple OOSPP A* sub-searches
(or other SPP variants) — they don't extend `AlgoSPP`
directly. They DO inherit from a shared `AlgoMOSPP` base in
`i_0_base/`, which extends `f_cs.algo.Algo` and provides
the lifecycle, counter scaffold, and `SolutionMOSPP`
return.

## Module Structure

```
mospp/
├── __init__.py             Lazy aggregator
├── _single_start_view.py   ProblemSPP wrapper exposing
│                           exactly one start (mirror of
│                           OMSPP _SingleGoalView)
├── _flipped_view.py        ProblemSPP wrapper that SWAPS
│                           starts ↔ goals (turns MOSPP into
│                           OMSPP). Used by KBFSMOSPP /
│                           KDijkstraMOSPP delegation.
├── _recorder_shim.py       _OnGoalToOnStartShim — rewrites
│                           `on_goal` → `on_start` events
│                           for the OMSPP-delegation algos.
├── i_0_base/               AlgoMOSPP — abstract base
│                             (Algo lifecycle + counter
│                              scaffold + SolutionMOSPP)
├── mixins/                 MOSPP-scoped capability mixins
│   └── extendable/         ExtendableMOSPP — prefix-extend
│                             the START sequence after run()
│                             (composed by AStarRepMOSPP)
├── i_1_astar_rep/          AStarRepMOSPP — Repetitive k×A*
│                             baseline (Extendable)
├── i_1_astar_inc/          AStarIncMOSPP — Incremental k×A*
│                             (goal-anchored cache + bounds
│                              reuse; cache-hit-at-init;
│                              study/oracle.py)
├── i_1_kbfs/               KBFSMOSPP — k-BFS via flip-to-
│                             OMSPP delegation (undirected,
│                             uniform-weight)
└── i_1_kdijkstra/          KDijkstraMOSPP — k-Dijkstra via
                              flip-to-OMSPP delegation
                              (undirected, non-negative
                              weights)
```

## Package Exports

```python
from f_hs.algo.i_1_mospp import (
    AStarRepMOSPP, KBFSMOSPP, KDijkstraMOSPP,
)
from f_hs.algo.i_1_mospp.i_1_astar_inc import AStarIncMOSPP
# also re-exported at top-level:
from f_hs import AStarRepMOSPP, KBFSMOSPP, KDijkstraMOSPP
```

## Algorithm matrix

| Name | Status | Extendable | Notes |
|---|---|---|---|
| `AStarRepMOSPP` | shipped | yes | Repetitive k×A* — MOSPP paper baseline; k independent A*s, no state sharing. Composes `ExtendableMOSPP`; gains the `already_reached` fast-path skip only. Admissible h sufficient. Works on directed graphs. |
| `AStarIncMOSPP` | shipped | no | Incremental k×A* — k sequential forward `AStarBPMX` sub-searches sharing a goal-anchored on-path cache + admissible bounds (NOT a shared `SearchStateSPP`; start varies). Cache-hit-at-init headline win. Opt-in pre-search `propagate_pathmax` and in-search BPMX. Admissible h sufficient (consistency not required). Works on directed graphs. |
| `KBFSMOSPP` | shipped | no | k-BFS via flip-to-OMSPP delegation. **Undirected, uniform-weight precondition.** Single backward BFS pass from the goal; emits `on_start` (translated by `_OnGoalToOnStartShim` from the inner OMSPP `KBFS`'s `on_goal`). Mirror of OMSPP `KBFS`. |
| `KDijkstraMOSPP` | shipped | no | k-Dijkstra via flip-to-OMSPP delegation. **Undirected, non-negative-weight precondition.** Single backward Dijkstra pass from the goal; same event-translation pattern as `KBFSMOSPP`. Mirror of OMSPP `KDijkstra`. |

`AStarIncMOSPP` is the realized state-sharing MOSPP
algorithm: forward-direction sub-searches with goal-anchored
suffix-caching via `AStarLookup.to_cache()` + accumulated
admissible bounds, NOT the flip-to-OMSPP delegation pattern
(which only works on undirected graphs). It deliberately does
**not** compose `ExtendableMOSPP` — the reuse axis is the
cache/bounds stores, not a prefix-extendable start sequence.

## Capability mixins

| Mixin | Path | Composed by |
|---|---|---|
| `ExtendableMOSPP` | `mixins/extendable/` | `AStarRepMOSPP` |

`ExtendableMOSPP` adds `extend(new_starts)` (instance
method) and `run_nested(problems, h, ...)` (classmethod).
See its own `CLAUDE.md` for the subclass contract. The free
function `is_extendable(algo)` (in the same module) checks
the MOSPP mixin specifically:

```python
from f_hs.algo.i_1_mospp.mixins.extendable import is_extendable
if is_extendable(algo):
    algo.extend([s_new])
```

The OMSPP-scope `is_extendable` checks `ExtendableOMSPP` —
scope determines which mixin is queried. Both share the
same function name in their respective modules.

## Design Principles

1. **Sibling-of-AlgoOMSPP, mirror in body.** `AlgoMOSPP`'s
   counter scaffold, phase setter, `_flush_phase_timer`,
   `_sync_memory_snapshot`, and lifecycle hooks are
   identical to `AlgoOMSPP` — only the `Algo` Solution
   generic argument and naming differ. This duplication
   is accepted in exchange for natural OMSPP/MOSPP naming;
   refactor into a shared abstract base if/when a third
   variant (MMSPP) arrives.
2. **Fixed-h optimization.** Because the goal is fixed
   across MOSPP sub-searches, `AStarRepMOSPP` precomputes
   the counter-wrapped h ONCE in `__init__` and reuses the
   same callable across every sub-search. OMSPP cannot do
   this (h's goal closure varies per sub-search).
3. **Honest event schema.** MOSPP emits `on_start` (not
   `on_goal`) — semantically correct for the axis. Cross-
   variant tooling forks on the event type when needed.
4. **Composition over `AlgoSPP`.** MOSPP orchestrators
   instantiate AStar sub-searches via `_SingleStartView` —
   they don't extend `AlgoSPP`.

## Dependencies

- `f_cs.algo.Algo`
- `f_core.counters.Counters`
- `f_hs.algo.i_0_oospp.i_1_astar.AStar`
- `f_hs.problem.i_0_base.ProblemSPP`
- `f_hs.solution.SolutionMOSPP`
- `f_hs.solution.SolutionSPP`
- `f_hs.state.i_0_base.StateBase`
