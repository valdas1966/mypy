# KxAStarOMSPP — Repetitive k×A* (OMSPP paper baseline)

## Purpose

Solves the One-to-Many Shortest Path Problem (OMSPP) by
running **k independent A* sub-searches** — one per goal,
NO state sharing across sub-searches. Each sub-search
builds its own `SearchStateSPP` from scratch, expands its
own subset of the graph, and is then discarded.

This is the **paper baseline** (`kA*_min` / `kA*_rep` in
Stern et al.'s OMSPP/MOSPP submission) against which
state-sharing OMSPP algorithms (`KAStarInc`, `KAStarAgg`,
`KBFS`, `KDijkstra`) are compared.

## Public API

### Constructor

```python
KxAStarOMSPP(problem: ProblemSPP[State],
        h: Callable[[State, State], int],
        name: str = 'KxAStarOMSPP',
        is_recording: bool = False,
        is_timing: bool = True)
```

- `problem.goals` provides the goal list `[t₁, ..., tₖ]`.
- `h(state, goal) -> int` — bi-arg heuristic.
- **Admissible** h is sufficient; consistency is NOT
  required (no fast-path relies on it).

### Methods

| Method | Description |
|---|---|
| `run() -> SolutionOMSPP` | Orchestrates k independent A*s. |
| `extend(new_goals) -> SolutionOMSPP` | Append goals; run A* only on genuinely-new goals. From `ExtendableOMSPP` mixin. |
| `run_nested(problems, h, ...)` *(classmethod)* | Convenience for a prefix-extending sequence of problems. From mixin. |
| `reconstruct_path(goal) -> list[State]` | Returns `[]` by design — kxA* discards each sub-search's parent pointers. |

### Counter scaffold

| counter | semantics |
|---|---|
| `cnt_h_search` | h(state, goal) calls during sub-search execution. |
| `cnt_push` | Cumulative `frontier.push` across all sub-searches. |
| `cnt_pop` | Cumulative `frontier.pop`. |
| `cnt_decrease` | Cumulative `frontier.decrease`. |
| `cnt_expanded` | Cumulative expanded states. |
| `cnt_generated` | Cumulative first-time pushes. |
| `mem_open` / `mem_closed` | **Peak** memory snapshot across sub-searches (not the last sub-search, not the sum). Each sub-search probe uses that sub-search's `frontier.max_size` for the OPEN count. |
| `mem_total` | `Σ mem_*` — conservative upper-bound coincident peak. |

`cnt_h_update` is **absent** — kxA* has no PHASE_UPDATE
moment (no between-sub-search refresh). No structural zero
in the scaffold per the codebase's "honest counter set"
convention.

Heap-op counters are aggregated per-iteration inside
`_handle_goal` (each sub-search has its own frontier; no
end-of-run sync from a shared frontier).

### Elapsed split

| metric | value for kxA* |
|---|---|
| `elapsed_search` | wall-clock across all sub-search loop bodies |
| `elapsed_update` | **always 0.0** — no PHASE_UPDATE flips |

## Composition with `ExtendableOMSPP`

`KxAStarOMSPP(Generic[State], AlgoOMSPP[State],
ExtendableOMSPP[State])` — k×A* composes the
`ExtendableOMSPP` capability mixin, gaining `extend()` and
`run_nested()`.

**Mixin value for kxA* — bounded to one axis: the
`already_reached` fast-path**. Submitting a goal that's
already in `self._solutions` skips A* entirely. This is
the **only** state-reuse axis k×A* admits by design (the
algorithm is, by definition, repetitive — no shared
frontier, no shared CLOSED set, no lazy re-push).

**Mixin features that DO NOT help kxA*:**

| mixin feature | why inert here |
|---|---|
| Lazy re-push of trailing reached goal | No shared frontier to push into. `_repush_last_reached_goal` is a no-op. |
| `already_closed` fast-path | No shared CLOSED set. |
| PHASE_UPDATE transition + `refresh_priorities` | No shared frontier to refresh. `update_frontier` is NOT emitted. |

The mixin's API surface (extend + run_nested) is still
worth composing — it lets benchmark scaffolding treat
`KxAStarOMSPP`, `KAStarInc`, `KBFS`, `KDijkstra` uniformly via
`is_extendable(algo)`, with the per-algo efficiency
varying naturally.

## Recording — event schema

Subset of the canonical OMSPP 5-event set:

| event | emitted by | when |
|---|---|---|
| `push` | inner AStar | first-time push |
| `pop` | inner AStar | per pop |
| `decrease_g` | inner AStar | per decrease-key |
| `on_goal` | KxAStarOMSPP | per goal at sub-search end; `reason ∈ {expanded, already_reached, unreachable}` |
| `update_frontier` | — | **NOT EMITTED** (no transition) |

The `already_closed` reason is never emitted (no shared
CLOSED set).

## Algorithm

```
for i, goal_i in enumerate(problem.goals):
    if goal_i in self._solutions:
        emit on_goal(reason='already_reached')   # fast-path
        continue

    algo = AStar(sub_problem(goal_i), h=h_i)
    algo._recorder = self._recorder              # share event log
    sol = algo.run()                             # FROM SCRATCH

    accumulate algo.counters into self._counters
    track peak (mem_open, mem_closed)

    emit on_goal(reason=reached ? 'expanded' : 'unreachable')
    self._solutions[goal_i] = sol
```

## Factory

| Method | Description |
|---|---|
| `graph_abc_two_goals()` | A→B→C with goals=[B, C]; both expanded via independent A*s. |
| `graph_abc_repeated_goal()` | A→B→C with goals=[B, B]; sub-search 1 expands B, sub-search 2 fast-paths. |

## Tests

| File | Scope | Count |
|---|---|---|
| `_tester.py` | lifecycle, fast-path (duplicate), no-already_closed, no-update_frontier, counter scaffold, elapsed_update=0, cost parity vs KAStarInc, empty reconstruct_path | 9 |
| `_tester_extend.py` | capability, preconditions, single-shot baseline parity, already_reached skip via extend, three-call chain, cumulative counters, inert repush, run_nested | 9 |
| `_tester_counters.py` | 6-counter pin on the canonical `grid_4x4_obstacle_omspp` problem (recording OFF); per-goal-costs pin (7 / 3 / 6) | 2 |
| `_tester_recording.py` | full normalized event-stream pin on the canonical OMSPP (3 goals, 55 events) AND on the 2-goal `grid_4x4_obstacle` variant (43 events) | 2 |

## Assumptions & limitations

1. **Admissible h required**; consistency NOT required.
2. **No state sharing** — by definition the OMSPP paper
   baseline. Comparable expansion count is `k × <single
   A* expansion count>`, the upper bound that state-
   sharing algos beat.
3. **Path reconstruction not supported** — sub-search
   bundles are discarded. Use `KAStarInc` if per-goal
   paths are needed.

## Dependencies

- `f_hs.algo.i_1_omspp.i_0_base.AlgoOMSPP` — base class
  (lifecycle + counter scaffold).
- `f_hs.algo.i_1_omspp.mixins.extendable.ExtendableOMSPP`
  — capability mixin (extend + run_nested).
- `f_hs.algo.i_1_astar.AStar` — inner sub-search.
- `f_hs.algo.i_1_omspp._single_goal_view._SingleGoalView`
  — single-goal wrapper of a multi-goal `ProblemSPP`.
- `f_hs.problem.i_0_base.ProblemSPP`
- `f_hs.solution.SolutionOMSPP`, `f_hs.solution.SolutionSPP`
