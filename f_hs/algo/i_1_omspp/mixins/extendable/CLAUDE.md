# ExtendableOMSPP — OMSPP goal-sequence extension mixin

## Purpose

Capability mixin that adds `extend(new_goals)` to OMSPP
orchestrators whose `_run()` body is a per-goal sub-search
loop. Composes with `AlgoOMSPP`; the orchestrator's
existing per-iteration goal-handling becomes a shared
`_handle_goal()` driven by both `_run()` and `extend()`.

## Public API

### `extend(new_goals: list[State]) -> SolutionOMSPP`

Resume the orchestrator with additional goals appended to
the sequence already solved by `run()` (and any prior
`extend()`s).

- Returns a `SolutionOMSPP` over the FULL set of goals seen
  so far.
- Accumulates into `counters`, `elapsed`, `t_search`,
  `t_update`, `recorder`, `solutions`.
- Preconditions: `run()` completed; `new_goals` non-empty.

### `run_nested(problems, h, ...) -> ExtendableOMSPP`
*(classmethod)*

Convenience: solve a prefix-extending list of OMSPP
problems via one call. Internally `run(problems[0]) →
extend(suffix of problems[1]) → extend(...) → ...`. Each
problem's prefix matched against `algo._all_goals`; only
the genuinely new goals are passed to `extend`.

### `is_extendable(algo) -> bool`

Free function — equivalent to `isinstance(algo,
ExtendableOMSPP)`. For callers using functional capability
forks.

## Subclass contract

A subclass MUST:

1. Inherit `AlgoOMSPP` AND `ExtendableOMSPP`.
2. Implement `_handle_goal(goal, idx)`: the per-goal
   sub-search body. `idx` is the position in
   `self._all_goals` at call time; the subclass uses `idx <
   len(self._all_goals) - 1` for the lazy-re-push decision.
3. Implement `_repush_last_reached_goal()`: push
   `self._last_reached_goal` onto OPEN via
   `self._last_algo._push(...)`, then clear both fields.
   No-op when `_last_reached_goal is None`.
4. Initialize `self._all_goals: list[State] = []`,
   `self._last_reached_goal: State | None = None`,
   `self._last_algo: object | None = None` in `__init__`.
5. Set `self._all_goals = list(self.problem.goals)` at the
   top of `_run`; reset `_last_reached_goal` and
   `_last_algo` to None.
6. Inside `_handle_goal`, when an expansion succeeds:
   `self._last_reached_goal = goal`; `self._last_algo =
   algo`. On fast-path / unreachable: `self._last_reached_goal
   = None`.

## Why a mixin (and not on `AlgoOMSPP`)

`KAStarAgg`'s single-loop, Φ-aggregated structure does not
fit the per-goal sub-search shape. Adding `extend()` to
AGG requires Φ-mode-gated soundness analysis and a Φ-refresh
over OPEN under a re-grown active set — out of today's scope.
Keeping `extend()` on a mixin keeps AGG's API surface honest
(`hasattr(agg, 'extend') is False`).

Three of the four OMSPP algos *could* compose this mixin:

| algo | composes today | rationale |
|---|---|---|
| `KAStarInc` | yes | per-goal sub-search loop |
| `KAStarAgg` | no | single-loop Φ-aggregated; extend semantics not settled |
| `KBFS` | no (yet) | shape fits; deferred until demand |
| `KDijkstra` | no (yet) | shape fits; deferred until demand |

## Composition example

```python
from f_hs.algo.i_1_omspp.i_0_base.main import AlgoOMSPP
from f_hs.algo.i_1_omspp.mixins.extendable import (
    ExtendableOMSPP,
)

class KAStarInc(Generic[State],
                AlgoOMSPP[State],
                ExtendableOMSPP[State]):

    def __init__(self, problem, h, ...):
        AlgoOMSPP.__init__(self, problem=problem, h=h, ...)
        self._shared_state = None
        self._all_goals: list[State] = []
        self._last_reached_goal: State | None = None
        self._last_algo: AStar[State] | None = None

    def _run(self) -> SolutionOMSPP:
        self._shared_state = None
        self._all_goals = list(self.problem.goals)
        self._last_reached_goal = None
        self._last_algo = None
        for i, goal in enumerate(self._all_goals):
            self._handle_goal(goal, i)
        return SolutionOMSPP(self._solutions)

    def _handle_goal(self, goal, idx):
        # ... fast-paths, transition, sub-search, on_goal,
        #     lazy re-push if non-last, bookkeeping update ...

    def _repush_last_reached_goal(self):
        if self._last_reached_goal is None:
            return
        self._last_algo._push(state=self._last_reached_goal)
        self._last_reached_goal = None
        self._last_algo = None
```

## Dependencies

- `f_hs.algo.i_1_omspp.i_0_base.main.PHASE_SEARCH`
- `f_hs.solution.main.SolutionOMSPP`
- `f_hs.state.i_0_base.main.StateBase`

Plus runtime composition with `AlgoOMSPP` (reads
`_elapsed`, `_is_timing`, `_phase`, `_t_phase_start`,
`_solutions`; calls `_flush_phase_timer`,
`_sync_frontier_counters`, `_sync_memory_snapshot`).
