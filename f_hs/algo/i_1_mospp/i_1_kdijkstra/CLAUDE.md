# KDijkstraMOSPP — k-Dijkstra for MOSPP (delegating to OMSPP)

## Purpose

Solves the Many-to-One Shortest Path Problem on **non-negative-
weight undirected graphs** via a single backward Dijkstra pass
from the shared goal. Implemented by **delegating to OMSPP
`KDijkstra`**: build a `_FlippedView` of the MOSPP problem (the
MOSPP goal becomes the OMSPP shared start; the MOSPP starts
become the OMSPP goals), run OMSPP `KDijkstra`, re-key the
per-goal result as a per-start result.

Mirror of OMSPP `KDijkstra` over the axis-swap. Sibling of
`KBFSMOSPP`; `KDijkstraMOSPP` is the more general one
(arbitrary non-negative weights vs. unit weights only).

## Public API

### Constructor
```python
KDijkstraMOSPP(problem: ProblemSPP[State],
               name: str = 'KDijkstraMOSPP',
               is_recording: bool = False,
               is_timing: bool = True)
```
No `h` kwarg — Dijkstra hardcodes h≡0. The base `AlgoMOSPP`
requires `h`, so a dummy `lambda s, g: 0` is passed internally
and never invoked.

### Inheritance
```
AlgoMOSPP[State]
    └── KDijkstraMOSPP[State]

# inner (private):
AlgoOMSPP[State]
    └── KDijkstra[State]  (OMSPP)
            └── _MultiGoalDijkstra[State]
```

### Methods
| Method | Description |
|---|---|
| `run() -> SolutionMOSPP` | Algo lifecycle entry point. Builds the flipped view, delegates to OMSPP `KDijkstra`, re-keys. |
| `reconstruct_path(start) -> list[State]` | Walks the inner's parent dict from `start` back to the MOSPP goal, then reverses so the caller sees `[start, ..., goal]`. |

### Properties
| Property | Description |
|---|---|
| `solutions`, `counters`, `elapsed`, `elapsed_search`, `elapsed_update`, `phase`, `recorder`, `name`, `problem` | Inherited from `AlgoMOSPP` |
| `search_state` | The inner OMSPP `KDijkstra`'s `SearchStateSPP` |

### Counters

Uses the base `AlgoMOSPP` scaffold unchanged. No heuristic, no
Φ — `cnt_h_*` / `cnt_phi_*` / `cnt_pop_stale` are ABSENT.

| counter | KDijkstraMOSPP |
|---|:---:|
| `cnt_push`, `cnt_pop`, `cnt_decrease` | ✓ (mirrored from inner OMSPP `KDijkstra`) |
| `cnt_expanded`, `cnt_generated` | ✓ (mirrored) |
| `mem_open`, `mem_closed` | ✓ (post-run, auto-probed via `_inner.search_state`) |

### Within/between elapsed split

`elapsed_update == 0.0` by construction — phase never flips.

### Recording event schema

| event | source | when |
|---|---|---|
| `push`, `pop`, `decrease_g` | inner `_MultiGoalDijkstra` (via `Dijkstra._enrich_event`, which drops h/f) | per g-order pop/push/decrease |
| `on_start` | recorder shim translation of inner OMSPP's `on_goal` | per start at the moment its state is popped (interleaved). Payload: `state`, `g`, `reason ∈ {expanded, unreachable}`, `start_index` |

NO `on_goal` (translated by `_OnGoalToOnStartShim`), NO
`update_frontier`, NO `update_heuristic`.

## Algorithm

```
flipped = _FlippedView(base=self.problem)
    # flipped.starts = self.problem.goals   (1 state)
    # flipped.goals  = self.problem.starts  (k states)
inner = KDijkstra(flipped, is_recording=False, is_timing=False)
inner._recorder = _OnGoalToOnStartShim(self._recorder)
inner.run()
self._solutions = dict(inner.solutions)
return SolutionMOSPP(self._solutions)
```

## Correctness preconditions

1. **Non-negative edge weights** (Dijkstra-family).
2. **Undirected graph** (or symmetric `successors` and `w`).
   The flipped view does NOT reverse the adjacency. On a
   directed graph this delegation silently computes the wrong
   quantity. No runtime check.
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
| `_tester.py` | lifecycle (single/two/unreachable start), duplicate-start, recording-schema cleanliness, counter scaffold, elapsed_update zero, multi-goal rejection, cross-algo equivalence vs `AStarRepMOSPP` and `KBFSMOSPP`, path reconstruction | 10 |
| `_tester_counters.py` | counter pin on canonical MOSPP grid (14 push / 14 pop); per-start optimal costs pin (7 / 3 / 6) | 2 |
| `_tester_recording.py` | FULL event-stream pin on canonical MOSPP — 31 events (14 push / 14 pop with 3 INTERLEAVED `on_start` events at discovery order). Identical to `KBFSMOSPP` on this uniform-cost canonical (pinned independently so a future tiebreak divergence surfaces in both testers). | 1 |

## Dependencies

- `f_hs.algo.i_1_mospp.i_0_base.AlgoMOSPP` — variant base.
- `f_hs.algo.i_1_mospp._flipped_view._FlippedView`.
- `f_hs.algo.i_1_mospp._recorder_shim._OnGoalToOnStartShim`.
- `f_hs.algo.i_1_omspp.i_2_kdijkstra.KDijkstra` — inner.
- `f_hs.solution.SolutionMOSPP`, `f_hs.solution.SolutionSPP`.
