# AlgoMOSPP — Many-to-One SPP base

## Purpose

Abstract base for MOSPP algorithms (currently:
`AStarRepMOSPP`). Sibling of `AlgoOMSPP` — both inherit
the standard `f_cs.algo.Algo` lifecycle, plus a minimal
counter scaffold (composed via `f_core.counters.Counters`).
Returns `SolutionMOSPP` (Mapping over `{start: SolutionSPP}`).

## Inheritance

```
f_cs.algo.Algo[ProblemSPP[State], SolutionMOSPP]
    └── AlgoMOSPP[State]
            └── AStarRepMOSPP
```

Mirrors `AlgoOMSPP` in body — counter scaffold, phase
setter, lifecycle hooks, `_flush_phase_timer`,
`_sync_frontier_counters`. The differences are the `Algo`
Solution generic argument (`SolutionMOSPP` vs
`SolutionOMSPP`), naming, and `_sync_memory_snapshot` (see
below).

## Memory metric — node counts at completion (exact peak)

`_sync_memory_snapshot` writes **node counts**, read ONCE at
search completion: `mem_open = |OPEN|` (`len(frontier)`) and
`mem_closed = |CLOSED|` (`len(closed)`), with `mem_total =
|OPEN| + |CLOSED|` (via `u_mem.finalize_mem_total`).

The end snapshot is the **EXACT** peak coincident memory
because the search is **accumulative**: a node moves OPEN →
CLOSED (or CLOSED → OPEN on re-open) but never leaves both, so
`|OPEN| + |CLOSED| = |nodes seen|` is monotone and peaks at the
end. No per-step peak tracking, and no over-count from summing
region peaks (e.g. `max_size` + final `|CLOSED|`) that never
co-occur.

This base reading is used by the flip-to-OMSPP delegates
(`AStarFlipMOSPP` / `BFSFlipMOSPP` / `DijkstraFlipMOSPP`) via
`_inner.search_state`. The forward family (`AStarRepMOSPP` /
`AStarIncMOSPP`) **overrides** it to take the MAX-total over
its k disjoint sub-searches (each freed before the next) —
that run's peak. Either way every MOSPP algo reports the same
node-count `|OPEN| + |CLOSED|` exact peak — fully
apples-to-apples. Contrast `AlgoOMSPP`, which still uses the
`getsizeof` byte probe.

## Problem shape

MOSPP = `ProblemSPP` with `len(starts) >= 1, len(goals) ==
1`. The orchestrator iterates `self.problem.starts` and
runs k sub-searches, one per start, each searching forward
toward the shared single goal.

## Public API

Same shape as `AlgoOMSPP` (see its CLAUDE.md):
- `run()` → `SolutionMOSPP` (inherited from `Algo`).
- `solutions: dict[State, SolutionSPP]` keyed by START.
- `counters: Counters` (per-class scaffold).
- `elapsed`, `elapsed_search`, `elapsed_update`.
- `phase` property (mutate via setter).

## Subclass contract

A subclass MUST:

1. Inherit `AlgoMOSPP[State]`.
2. Call `AlgoMOSPP.__init__(self, problem=problem, h=h,
   name=..., is_recording=is_recording)`.
3. Override `_run() -> SolutionMOSPP`.
4. Populate `self._solutions[start]` with a `SolutionSPP`
   for every start in `self.problem.starts` (cost=`inf`
   for unreachable).
5. Return `SolutionMOSPP(self._solutions)` from `_run()`.
6. Increment counters via `self._counters.inc('cnt_X')`.

## Dependencies

- `f_cs.algo.Algo`
- `f_core.counters.Counters`
- `f_hs.problem.i_0_base.ProblemSPP`
- `f_hs.solution.SolutionMOSPP`
- `f_hs.solution.SolutionSPP`
- `f_hs.state.i_0_base.StateBase`
