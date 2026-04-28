# AlgoOMSPP — One-to-Many SPP base

## Purpose

Abstract base for OMSPP algorithms (`KAStarInc`, `KAStarAgg`,
future `KDijkstra`). Inherits the standard f_cs `Algo`
lifecycle (so `elapsed`, `recorder`, `name`, `problem` are all
provided), plus a unified 8-counter scaffold for
cross-algorithm benchmark comparison.

## Inheritance

```
f_cs.algo.Algo[ProblemSPP[State], SolutionOMSPP]
    └── AlgoOMSPP[State]
            ├── KAStarInc
            └── KAStarAgg
```

`AlgoOMSPP` is a **sibling** of `AlgoSPP` under the same
`Algo` parent — both adapt the f_cs lifecycle to their problem
type. AlgoSPP wraps a single SPP search loop returning a
single `SolutionSPP`; AlgoOMSPP orchestrates a multi-goal
search returning a per-goal `SolutionOMSPP`.

## Public API

### Constructor
```python
def __init__(self,
             problem: ProblemSPP[State],
             h: Callable[[State, State], int],
             name: str = 'AlgoOMSPP',
             is_recording: bool = False) -> None
```

### Properties
| Property | Type | Description |
|---|---|---|
| `problem` | `ProblemSPP[State]` | Inherited from `Algo`; alias for `self.input` |
| `name` | `str` | Inherited from `HasName` |
| `recorder` | `Recorder` | Inherited from `ProcessBase` |
| `elapsed` | `float \| None` | Inherited from `ProcessBase`; auto-set in `_run_post()` |
| `solutions` | `dict[State, SolutionSPP]` | Per-goal map populated by `_run()` |
| `counters` | `dict[str, int]` | Per-run 8-counter snapshot |

### Lifecycle (inherited from `Algo` / `ProcessBase`)
| Method | Description |
|---|---|
| `run()` | Public entry. Calls `_run_pre()` → `_run()` → `_run_post()`; returns a `SolutionOMSPP` |
| `_run_pre()` | Resets `_elapsed`, then resets the 8 counters and `_solutions` (overridden in this base) |
| `_run()` | **Subclass override.** Execute the algorithm, populate `self._solutions`, return `SolutionOMSPP(self._solutions)` |
| `_run_post()` | Records `_elapsed = time_finish - time_start` |

## The 8 counters

Each counter name is also the dict key returned by
`algo.counters`. Subclasses increment whichever subset they
support; unsupported counters stay at 0 with a documented
reason.

| counter | semantics |
|---|---|
| `cnt_h_search` | h(state, goal) call in normal search flow |
| `cnt_h_update` | h(state, goal) call in refresh flow |
| `cnt_phi_search` | `_compute_F` call in normal flow (Φ-aggregation algorithms only) |
| `cnt_phi_update` | `_compute_F` call in refresh flow (Φ-aggregation algorithms only) |
| `cnt_push` | `frontier.push` call |
| `cnt_pop` | `frontier.pop` call |
| `cnt_pop_stale` | subset of `cnt_pop`: stale-F re-insertions (lazy-mode algorithms only) |
| `cnt_decrease` | `frontier.decrease` call |

### Per-algorithm support (current state)

| counter | KAStarAgg | KAStarInc |
|---|:---:|:---:|
| `cnt_h_search` | ✓ | ✓ |
| `cnt_h_update` | ✓ | ✓ |
| `cnt_phi_search` | ✓ | N/A (no Φ aggregation) |
| `cnt_phi_update` | ✓ | N/A (no Φ aggregation) |
| `cnt_push` | ✓ | deferred (requires AStar/FrontierPriority instrumentation) |
| `cnt_pop` | ✓ | deferred |
| `cnt_pop_stale` | ✓ (lazy only) | N/A (no lazy stale-pop) |
| `cnt_decrease` | ✓ | deferred |

KAStarInc tracks `cnt_h_search` / `cnt_h_update` by wrapping
the h-callable handed to each inner AStar; phase tracking
(`'search'` during sub-search execution, `'update'` during
inter-sub-search priority refresh) routes increments to the
right counter.

## Subclass contract

A subclass MUST:

1. Inherit `AlgoOMSPP[State]`.
2. Call `AlgoOMSPP.__init__(self, problem=problem, h=h,
   name=..., is_recording=is_recording)` to wire `Algo`'s
   `_input` / `_recorder` / `_elapsed` plumbing and the
   counter scaffold.
3. Override `_run() -> SolutionOMSPP`.
4. Populate `self._solutions[goal]` with a `SolutionSPP` for
   every goal in `self.problem.goals` (cost=`float('inf')`
   for unreachable).
5. Return `SolutionOMSPP(self._solutions)` from `_run()`.
6. Increment `self._cnt_*` counters in the algorithm body
   wherever the operation occurs.

A subclass MAY:

- Override `_run_pre()` if additional reset is needed; call
  `super()._run_pre()` first.
- Add its own properties / methods (e.g., `KAStarInc.search_state`,
  `KAStarAgg.is_lazy`).
- Add subclass-specific counters or events; keep the base
  8-counter set canonical.

## Dependencies

- `f_cs.algo.Algo` — lifecycle scaffold.
- `f_hs.problem.i_0_base.ProblemSPP` — problem with multiple
  goals.
- `f_hs.solution.SolutionOMSPP` — per-goal solution wrapper.
- `f_hs.solution.SolutionSPP` — per-goal cost holder.
- `f_hs.state.i_0_base.StateBase` — generic state bound.
