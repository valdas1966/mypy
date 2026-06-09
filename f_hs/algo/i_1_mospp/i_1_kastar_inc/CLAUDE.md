# KAStarIncMOSPP — Incremental kA* for MOSPP (flip-to-OMSPP)

## Purpose

Solves the Many-to-One Shortest Path Problem (k starts → 1
goal) on **undirected** graphs by the axis-swap trick: build a
`_FlippedView` (the MOSPP goal becomes the OMSPP shared start;
the MOSPP starts become the OMSPP goals), delegate to the
**incremental** OMSPP solver `KAStarInc`, then re-key the
per-goal OMSPP result as a per-start MOSPP result.

Sibling of `KBFSMOSPP` / `KDijkstraMOSPP` (same flip
delegation) — but the inner solver carries **one shared
`SearchStateSPP` across the k goals** (a single search tree
grown OUTWARD from the shared goal), so it is the OMSPP-side
mirror of `AStarIncMOSPP`'s forward goal-anchored reuse: the
same MOSPP instance solved by growing one search from the goal
rather than running k forward searches into it.

## Public API

### Constructor
```python
KAStarIncMOSPP(problem: ProblemSPP[State],
               h: Callable[[State, State], int],
               name: str = 'KAStarIncMOSPP',
               is_recording: bool = False,
               is_timing: bool = True)
```
`h` is the bi-arg MOSPP heuristic; it is passed UNCHANGED to
the inner `KAStarInc`, which calls it as `h(state, omspp_goal)
= h(state, mospp_start_j)` — the correct OMSPP heuristic
(symmetric ⇒ valid under the flip).

### Methods
| Method | Description |
|---|---|
| `run() -> SolutionMOSPP` | Build the flipped view, delegate to `KAStarInc`, re-key per-goal → per-start. |
| `extend(new_starts) -> SolutionMOSPP` | **Batch** resume: the new MOSPP starts ARE the new OMSPP goals, so a single `inner.extend(new_starts)` grows the one shared search. Counters/elapsed cumulative. |
| `reconstruct_path(start) -> list[State]` | Inner OMSPP path (goal→…→start) reversed to MOSPP direction `[start, …, goal]`. |
| `search_state` | The inner `KAStarInc`'s shared `SearchStateSPP`. |

**Why a direct batch `extend()`, not `ExtendableMOSPP`.** That
mixin's `extend()` is a per-start `_handle_start` loop — the
wrong granularity for a single-inner-search delegate. This
class delegates a whole batch to `KAStarInc.extend()` and
reimplements the short timing/counter-sync epilogue
(`_flush_phase_timer` → accumulate `_elapsed` →
`_sync_frontier_counters` → `_sync_memory_snapshot` →
`finalize_mem_total`). So `is_extendable(algo)` returns False,
but `run()` + `extend()` work and drive the s_3 nested chain.

## Correctness preconditions
1. **Undirected graph** (symmetric `successors`/`w`) — the
   flip relabels starts↔goals without reversing adjacency. On
   a directed graph it silently computes the wrong quantity.
   No runtime check. (Contrast `AStarIncMOSPP`: works on
   directed graphs.)
2. **Consistent heuristic** — required by inner `KAStarInc`
   (same-nodes guarantee + already-closed fast-path). Manhattan
   on grids is consistent.
3. **Exactly one goal** — `ValueError` at construction.

## Counters

Per-class `_COUNTER_NAMES` mirrors the inner `KAStarInc`:

| group | counters |
|---|---|
| heuristic | `cnt_h_search`, `cnt_h_update` |
| search | `cnt_expanded`, `cnt_generated` |
| frontier | `cnt_push`, `cnt_pop`, `cnt_decrease` |
| memory | `mem_open`, `mem_closed`, `mem_total` |

Mirrored from the inner (which accumulates across run+extend)
via `assign` in `_sync_frontier_counters`. **No** BPMX /
propagation / adaptive / cache-hit counters — this solver has
none (they default to 0 in the shared s_3 CSV schema).
`cnt_h_update` (inter-sub-search refresh cost) is exposed here
but is intentionally NOT in `s_3._CSV_COLUMNS` (dropped from
the CSV at this stage).

## Inheritance
```
AlgoMOSPP[State]
    └── KAStarIncMOSPP[State]      (this class)

# inner (private):
AlgoOMSPP[State] └── KAStarInc[State]  (OMSPP, ExtendableOMSPP)
```

## Factory
| Method | Description |
|---|---|
| `grid_6x6_zigzag_mospp()` | Canonical MOSPP grid shared with the `AStarIncMOSPP` oracle (cost cross-check). |
| `graph_abc_two_starts()` | Undirected A--B--C, starts [A, B], goal C. |

## Tests
`_tester.py` (6): costs match `AStarRepMOSPP` ground truth and
`AStarIncMOSPP`; `run()+extend()` == fresh full run; graph ABC
costs; exactly-one-goal + extend-before-run validation.

## Dependencies
- `f_hs.algo.i_1_mospp.i_0_base.AlgoMOSPP` — variant base.
- `f_hs.algo.i_1_mospp._flipped_view._FlippedView` — axis swap.
- `f_hs.algo.i_1_mospp._recorder_shim._OnGoalToOnStartShim`.
- `f_hs.algo.i_1_omspp.i_1_kastar_inc.KAStarInc` — inner solver.
- `f_hs.algo.u_mem.finalize_mem_total`.
- `f_hs.solution.SolutionMOSPP`.
