# AlgoOMSPP — One-to-Many SPP base

## Purpose

Abstract base for OMSPP algorithms (`KAStarInc`, `KAStarAgg`,
future `KDijkstra`). Inherits the standard f_cs `Algo`
lifecycle (so `elapsed`, `recorder`, `name`, `problem` are all
provided), plus a unified 8-counter scaffold (composed via
`f_core.counters.Counters`) for cross-algorithm benchmark
comparison.

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
             is_recording: bool = False,
             is_timing: bool = True) -> None
```

`is_timing` — when True (default), the `phase` property setter
calls `time.perf_counter()` on every flip to accumulate
`elapsed_search` / `elapsed_update`. Set False to skip the
`perf_counter` call (plain field write only) for distortion-free
wall-clock measurements at large k. Both timing properties stay
at 0.0 when off.

### Properties
| Property | Type | Description |
|---|---|---|
| `problem` | `ProblemSPP[State]` | Inherited from `Algo`; alias for `self.input` |
| `name` | `str` | Inherited from `HasName` |
| `recorder` | `Recorder` | Inherited from `ProcessBase` |
| `elapsed` | `float \| None` | Inherited from `ProcessBase`; auto-set in `_run_post()` |
| `solutions` | `dict[State, SolutionSPP]` | Per-goal map populated by `_run()` |
| `counters` | `Counters` | Per-run 8-counter snapshot (Mapping protocol — `c[name]`, `dict(c)`, `c == {...}` all work; `print(c)` shows an aligned grouped block) |
| `elapsed_search` | `float` | Wall-clock seconds in the **search** structural phase (sub-search loop bodies + force-expand + AGG-lazy inline refresh). 0.0 when `is_timing=False`. |
| `elapsed_update` | `float` | Wall-clock seconds in the **update** structural phase (Inc: `_emit_frontier_transition` + `algo.refresh_priorities`; AGG-eager: `_refresh_all_F`). **AGG-lazy reports 0.0 by construction** — no between-phase moment exists. 0.0 when `is_timing=False`. |
| `phase` | `str` | Current structural phase (`'search'` / `'update'`). Mutate via the property setter only — direct `_phase = X` writes bypass the time-bucket flush and are forbidden. |

### Lifecycle (inherited from `Algo` / `ProcessBase`)
| Method | Description |
|---|---|
| `run()` | Public entry. Calls `_run_pre()` → `_run()` → `_run_post()`; returns a `SolutionOMSPP` |
| `_run_pre()` | Resets `_elapsed`, then resets the 8 counters and `_solutions` (overridden in this base) |
| `_run()` | **Subclass override.** Execute the algorithm, populate `self._solutions`, return `SolutionOMSPP(self._solutions)` |
| `_run_post()` | Records `_elapsed = time_finish - time_start` |

## The 8 counters

Held in `self._counters` (a `f_core.counters.Counters`
instance, exposed through the read-only `counters` property).
Each name is also the key when consumers index the Counters or
convert it to a dict. Subclasses increment whichever subset
they support; unsupported counters stay at 0 with a documented
reason.

The 8 names are declared in 3 visual groups (h-calls,
phi-calls, frontier ops) so `print(algo.counters)` renders
with blank-line separators between groups for fast scanning.

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
| `cnt_push` | ✓ (frontier-sourced) | ✓ (frontier-sourced) |
| `cnt_pop` | ✓ (frontier-sourced) | ✓ (frontier-sourced) |
| `cnt_pop_stale` | ✓ (lazy only) | N/A (no lazy stale-pop) |
| `cnt_decrease` | ✓ (frontier-sourced) | ✓ (frontier-sourced) |

KAStarInc tracks `cnt_h_search` / `cnt_h_update` by wrapping
the h-callable handed to each inner AStar; phase tracking
(`'search'` during sub-search execution, `'update'` during
inter-sub-search priority refresh) routes increments to the
right counter.

### Phase + within/between time bucketing

Two structural phases — `PHASE_SEARCH` and `PHASE_UPDATE`
(module-level constants on `i_0_base/main.py`) — drive the
`elapsed_search` / `elapsed_update` split. Semantics are
**structural**, not work-typed:

- `PHASE_SEARCH` = inside a sub-search loop body (Inc:
  `algo.run`/`algo.resume` + force-expand; AGG: main best-first
  loop, including any inline lazy stale-pop re-checks).
- `PHASE_UPDATE` = explicit between-sub-search work (Inc:
  `_emit_frontier_transition` + `algo.refresh_priorities`;
  AGG-eager: `_refresh_all_F` calls).

**AGG-lazy reports `elapsed_update == 0.0`** by design — its
refresh work happens inline at pop time and is structurally
part of search. The `cnt_h_update` / `cnt_phi_update` counters
*do* increment for that work (they tag the work TYPE), so
counters and time buckets tell complementary stories:

| metric | what it measures |
|---|---|
| `cnt_*_update` | refresh-typed *work* (regardless of when) |
| `elapsed_update` | refresh-typed *time spent in a between-phase block* |

Mutation is via the `phase` property setter (typo-guarded with
`ValueError` on unknown values; idempotent on same-value).
Direct `_phase = X` writes bypass the time-bucket flush and
are forbidden.

Per-algo flip sites:
- **KAStarInc** — flips around `_emit_frontier_transition`
  and the explicit `algo.refresh_priorities`. Force-expand
  stays in SEARCH (Stern's framing).
- **KAStarAgg-eager** — flips around the `_refresh_all_F`
  call after each goal-find.
- **KAStarAgg-lazy** — does NOT flip (zero phase-flip
  overhead at any k).

### Counter sourcing — `_sync_frontier_counters` hook

`cnt_push` / `cnt_pop` / `cnt_decrease` are owned by the
underlying `FrontierPriority` (single source of truth — no
mirroring at increment time, no drift risk). At end-of-run,
`AlgoOMSPP._run_post` calls the subclass hook
`_sync_frontier_counters()` which mirrors the final tally
into `self._counters` via `Counters.assign`. Subclasses
override the hook to point at the right frontier:

- KAStarAgg → `self._frontier.counters` (owns its frontier
  directly).
- KAStarInc → `self._shared_state.frontier.counters` (the
  same `FrontierPriority` accumulates across all k
  sub-searches via the shared `SearchStateSPP` bundle, so a
  single read gives total push/pop/decrease for the whole
  INC run).

Default hook is a no-op — subclasses that don't expose a
frontier (or that don't want to surface its counts) leave it
alone.

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
6. Increment counters via `self._counters.inc('cnt_X')` in
   the algorithm body wherever the operation occurs (raises
   `KeyError` on a typo'd name — typo guard is intentional).

A subclass MAY:

- Override `_run_pre()` if additional reset is needed; call
  `super()._run_pre()` first.
- Override `_run_post()` if additional teardown is needed;
  call `super()._run_post()` first (which records `_elapsed`
  and triggers the `_sync_frontier_counters()` hook).
- Override `_sync_frontier_counters()` to mirror frontier
  heap-op counts into `self._counters` (call
  `self._counters.assign(name, value)` for each).
- Add its own properties / methods (e.g., `KAStarInc.search_state`,
  `KAStarAgg.is_lazy`).
- Add subclass-specific counters or events; keep the base
  8-counter set canonical.

## Dependencies

- `f_cs.algo.Algo` — lifecycle scaffold.
- `f_core.counters.Counters` — 8-counter scaffold composed
  into `self._counters`.
- `f_hs.problem.i_0_base.ProblemSPP` — problem with multiple
  goals.
- `f_hs.solution.SolutionOMSPP` — per-goal solution wrapper.
- `f_hs.solution.SolutionSPP` — per-goal cost holder.
- `f_hs.state.i_0_base.StateBase` — generic state bound.
