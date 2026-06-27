# BFSFlipMOSPP — k-BFS for MOSPP (delegating to OMSPP)

## Purpose

Solves the Many-to-One Shortest Path Problem on **uniform-weight
undirected graphs** via a single backward BFS pass from the
shared goal. Implemented by **delegating to OMSPP `KBFS`**: build
a `_FlippedView` of the MOSPP problem (the MOSPP goal becomes
the OMSPP shared start; the MOSPP starts become the OMSPP goals),
run OMSPP `KBFS`, re-key the per-goal result as a per-start
result.

Mirror of OMSPP `KBFS` over the axis-swap. The inner OMSPP
algorithm does the real work; this class is the
problem-flipping + solution-re-keying orchestrator.

## Public API

### Constructor
```python
BFSFlipMOSPP(problem: ProblemSPP[State],
          name: str = 'BFSFlipMOSPP',
          is_recording: bool = False,
          is_timing: bool = True)
```
No `h` kwarg — BFS has no heuristic. The base `AlgoMOSPP`
requires `h`, so a dummy `lambda s, g: 0` is passed internally
and never invoked.

### Inheritance
```
AlgoMOSPP[State]
    └── BFSFlipMOSPP[State]

# inner (private):
AlgoOMSPP[State]
    └── KBFS[State]  (OMSPP)
            └── _MultiGoalBFS[State]
```

### Methods
| Method | Description |
|---|---|
| `run() -> SolutionMOSPP` | Algo lifecycle entry point. Builds the flipped view, delegates to OMSPP `KBFS`, re-keys. |
| `reconstruct_path(start) -> list[State]` | Walks the inner's parent dict from `start` back to the MOSPP goal, then reverses so the caller sees `[start, ..., goal]`. |

### Properties
| Property | Description |
|---|---|
| `solutions`, `counters`, `elapsed`, `elapsed_search`, `elapsed_update`, `phase`, `recorder`, `name`, `problem` | Inherited from `AlgoMOSPP` |
| `search_state` | The inner OMSPP `KBFS`'s `SearchStateSPP` (its inner `_MultiGoalBFS`'s bundle) |

### Counters

Uses the base `AlgoMOSPP` scaffold unchanged. No heuristic, no
Φ — `cnt_h_*` / `cnt_phi_*` / `cnt_pop_stale` are ABSENT.

| counter | BFSFlipMOSPP |
|---|:---:|
| `cnt_push` | ✓ (mirrored from inner OMSPP `KBFS`) |
| `cnt_pop` | ✓ (mirrored) |
| `cnt_decrease` | 0 (FIFO has no decrease op; synthesized at algo level) |
| `cnt_expanded`, `cnt_generated` | ✓ (mirrored) |
| `mem_open`, `mem_closed` | ✓ **node counts** via `AlgoMOSPP._sync_memory_snapshot`: `len(frontier)` + `len(closed)` from `_inner.search_state` at completion; `mem_total = \|OPEN\| + \|CLOSED\|` = exact peak (accumulative ⇒ monotone). Apples-to-apples with every MOSPP algo. |

### Within/between elapsed split

`elapsed_update == 0.0` by construction — phase never flips
to `PHASE_UPDATE`.

### Recording event schema

| event | source | when |
|---|---|---|
| `push`, `pop` | inner `_MultiGoalBFS` | per BFS layer-order pop/push |
| `on_start` | recorder shim translation of inner OMSPP's `on_goal` | per start at the moment its state is popped (interleaved). Payload: `state`, `g`, `reason ∈ {expanded, unreachable}`, `start_index` |

NO `on_goal` (translated by `_OnGoalToOnStartShim`), NO
`update_frontier`, NO `update_heuristic`, NO `decrease_g`
(FIFO has no decrease op).

## Algorithm

```
flipped = _FlippedView(base=self.problem)
    # flipped.starts = self.problem.goals   (1 state)
    # flipped.goals  = self.problem.starts  (k states)
inner = KBFS(flipped, is_recording=False, is_timing=False)
inner._recorder = _OnGoalToOnStartShim(self._recorder)
inner.run()
self._solutions = dict(inner.solutions)
return SolutionMOSPP(self._solutions)
```

The shim rewrites every `on_goal` event from the inner OMSPP
`KBFS` orchestrator as an `on_start` event (translating
`goal_index` → `start_index`). All push/pop events pass through
unchanged.

## Correctness preconditions

1. **Uniform edge weights** — BFS depth = optimal cost. For
   non-uniform non-negative weights use `DijkstraFlipMOSPP`.
2. **Undirected graph** (or symmetric `successors` and `w`).
   The flipped view does NOT reverse the adjacency — it
   relabels which list is "starts" vs "goals." On an
   undirected graph `dist(goal, start_i) == dist(start_i,
   goal)`. On a directed graph this delegation silently
   computes the wrong quantity. No runtime check
   (`ProblemSPP` does not expose directionality).
3. **Exactly one goal** — `ValueError` at construction if
   `len(problem.goals) != 1`.

## Factory

| Method | Description |
|---|---|
| `graph_abc_two_starts()` | Undirected A--B--C, starts=[A, B], goal=C; both reachable. |
| `graph_abc_repeated_start()` | Undirected A--B, starts=[A, A], goal=B; duplicate-start handling. |

## Tests

| File | Scope | Count |
|---|---|---|
| `_tester.py` | lifecycle (single/two/unreachable start), duplicate-start, recording-schema cleanliness, counter scaffold, elapsed_update zero, multi-goal rejection, cross-algo equivalence vs `AStarRepMOSPP`, path reconstruction | 9 |
| `_tester_counters.py` | counter pin on canonical MOSPP grid (14 push / 14 pop); per-start optimal costs pin (7 / 3 / 6) | 2 |
| `_tester_recording.py` | FULL event-stream pin on canonical MOSPP — 31 events (14 push / 14 pop with 3 INTERLEAVED `on_start` events at discovery order) | 1 |

## Dependencies

- `f_hs.algo.i_1_mospp.i_0_base.AlgoMOSPP` — variant base.
- `f_hs.algo.i_1_mospp._flipped_view._FlippedView` — problem
  swap.
- `f_hs.algo.i_1_mospp._recorder_shim._OnGoalToOnStartShim` —
  event-type translator.
- `f_hs.algo.i_1_omspp.i_1_kbfs.KBFS` — inner orchestrator.
- `f_hs.solution.SolutionMOSPP`, `f_hs.solution.SolutionSPP`.
