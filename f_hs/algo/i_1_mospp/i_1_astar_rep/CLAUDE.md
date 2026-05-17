# AStarRepMOSPP — Repetitive k×A* (MOSPP paper baseline)

## Purpose

Solves the Many-to-One Shortest Path Problem (MOSPP) by
running **k independent A* sub-searches** — one per start,
NO state sharing across sub-searches. Each sub-search
starts at a different state, searches forward toward the
**shared single goal**, builds its own `SearchStateSPP`
from scratch, and is then discarded.

Mirror of `KxAStarOMSPP` (OMSPP scope). Same structural
shape; axis swapped (k starts instead of k goals).

## Public API

### Constructor

```python
AStarRepMOSPP(problem: ProblemSPP[State],
             h: Callable[[State, State], int],
             name: str = 'AStarRepMOSPP',
             is_recording: bool = False,
             is_timing: bool = True)
```

- `problem.starts` provides the start list `[s₁, ..., sₖ]`.
- `problem.goals` must have **exactly one** goal (else
  `ValueError`).
- `h(state, goal) -> int` — bi-arg heuristic. The goal is
  fixed, so the counter-wrapped h is built once in
  `__init__` and reused across every sub-search.
- **Admissible** h is sufficient.

### Methods

| Method | Description |
|---|---|
| `run() -> SolutionMOSPP` | Orchestrates k independent A*s, one per start. |
| `extend(new_starts) -> SolutionMOSPP` | Append starts; run A* only on genuinely-new starts. From `ExtendableMOSPP` mixin. |
| `run_nested(problems, h, ...)` *(classmethod)* | Convenience for a prefix-extending sequence of MOSPP problems. From mixin. |
| `reconstruct_path(start) -> list[State]` | Returns `[]` by design — kxA* discards each sub-search's parent pointers. |

### Counter scaffold

| counter | semantics |
|---|---|
| `cnt_h_search` | h(state, goal) calls during sub-search execution. |
| `cnt_push` | Cumulative `frontier.push` across all sub-searches. |
| `cnt_pop` | Cumulative `frontier.pop`. |
| `cnt_decrease` | Cumulative `frontier.decrease`. |
| `cnt_expanded` | Cumulative expanded states. |
| `cnt_generated` | Cumulative first-time pushes. |
| `mem_open` / `mem_closed` | **Peak** memory snapshot across sub-searches. |

`cnt_h_update` is **absent** — no PHASE_UPDATE in kxA*.

### Elapsed split

| metric | value for kxA*-MOSPP |
|---|---|
| `elapsed_search` | wall-clock across all sub-search loop bodies |
| `elapsed_update` | **always 0.0** — no PHASE_UPDATE flips |

## Composition with `ExtendableMOSPP`

`AStarRepMOSPP(Generic[State], AlgoMOSPP[State],
ExtendableMOSPP[State])` — composes the
`ExtendableMOSPP` capability mixin, gaining `extend()` and
`run_nested()`.

**Mixin value bounded to one axis**: the `already_reached`
fast-path skip. Submitting a start that's already in
`self._solutions` skips A* entirely. The deeper
state-sharing axes (lazy re-push, already_closed,
PHASE_UPDATE refresh) are **structurally inert** here.

## Recording — event schema

Subset of the canonical MOSPP 5-event set:

| event | emitted by | when |
|---|---|---|
| `push` | inner AStar | first-time push |
| `pop` | inner AStar | per pop |
| `decrease_g` | inner AStar | per decrease-key |
| `on_start` | AStarRepMOSPP | per start at sub-search end; `reason ∈ {expanded, already_reached, unreachable}` |
| `update_frontier` | — | **NOT EMITTED** (no transition) |

The `on_start` event is the MOSPP analog of OMSPP's
`on_goal` — semantically correct since the START is
MOSPP's variable axis. Payload: `state=start, g=cost,
reason, start_index`. The `already_closed` reason is never
emitted (no shared CLOSED set).

## Algorithm

```
h_wrapped = wrap(h, goal=problem.goals[0])  # once
for i, start_i in enumerate(problem.starts):
    if start_i in self._solutions:
        emit on_start(reason='already_reached')   # fast-path
        continue

    algo = AStar(single_start_view(start_i), h=h_wrapped)
    algo._recorder = self._recorder              # share event log
    sol = algo.run()                             # FROM SCRATCH

    accumulate algo.counters into self._counters
    track peak (mem_open, mem_closed)

    emit on_start(reason=reached ? 'expanded' : 'unreachable')
    self._solutions[start_i] = sol
```

## Factory

| Method | Description |
|---|---|
| `graph_abc_two_starts()` | A→B→C with starts=[A, B], goal=C; both expanded. |
| `graph_abc_repeated_start()` | starts=[A, A], goal=B; sub-search 1 expands A, sub-search 2 fast-paths. |

## Tests

| File | Scope | Count |
|---|---|---|
| `_tester.py` | lifecycle, fast-path (duplicate), no-already_closed, no-update_frontier, scaffold honesty, elapsed_update=0, multi-goal rejection, fixed-h-callable, empty reconstruct_path, canonical-grid cost parity | 12 |
| `_tester_extend.py` | capability, preconditions, baseline parity, already_reached skip, three-call chain, cumulative counters, inert repush, run_nested | 9 |
| `_tester_counters.py` | 6-counter pin on canonical `grid_4x4_obstacle_mospp` (recording OFF); per-start-costs pin (7 / 3 / 6) | 2 |
| `_tester_recording.py` | full normalized event-stream pin on canonical MOSPP (3 starts, 57 events) AND on the 2-start `grid_4x4_obstacle` variant (45 events) | 2 |

## Assumptions & limitations

1. **Admissible h required**; consistency NOT required.
2. **Exactly one goal** — `ValueError` at construction if
   `len(problem.goals) != 1`.
3. **No state sharing** — by definition. Comparable
   expansion count is the upper bound that state-sharing
   MOSPP algos (future) beat.
4. **Path reconstruction not supported** — sub-search
   bundles discarded.

## Dependencies

- `f_hs.algo.i_1_mospp.i_0_base.AlgoMOSPP`
- `f_hs.algo.i_1_mospp.mixins.extendable.ExtendableMOSPP`
- `f_hs.algo.i_0_oospp.i_1_astar.AStar`
- `f_hs.algo.i_1_mospp._single_start_view._SingleStartView`
- `f_hs.problem.i_0_base.ProblemSPP`
- `f_hs.solution.SolutionMOSPP`, `f_hs.solution.SolutionSPP`
