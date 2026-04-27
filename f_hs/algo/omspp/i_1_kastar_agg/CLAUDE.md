# KAStarAgg

## 1) Purpose

Aggregative kA* (kA*_agg) for the One-to-Many Shortest Path
Problem. One best-first search toward all `k` goals
simultaneously, using a heuristic aggregation function `Φ`
(MIN / MAX / AVG / RND / PROJECTION or a callable):

```
F(n) = g(n) + Φ(h_i(n) for i in active_goals)
```

Active-goal set shrinks as goals are found; F values of OPEN
nodes may go stale. Stern et al. 2021, Algorithm 3 (§5.1,
§5.1.1).

## 2) Public API

### Constructor

```python
def __init__(self,
             problem: ProblemSPP[State],
             h: Callable[[State, State], int],
             agg: str | Callable[[list[int]], int] = 'MIN',
             is_lazy: bool = True,
             is_opt: bool = False,
             store_vector: bool = False,
             name: str = 'KAStarAgg',
             is_recording: bool = False) -> None
```

Three orthogonal switches × `agg` define 8 + 1 configs:

| param | values | effect |
|---|---|---|
| `is_lazy` | True / False | Defer F refresh to pop time vs. eager batch refresh after every goal-find |
| `is_opt` | True / False | Stern §5.1.1 responsible-goal tracking; skips refresh when `n.responsible ∈ A`. Requires `agg ∈ {MIN, MAX}` |
| `store_vector` | True / False | Cache `[h_1(n), ..., h_k(n)]` per node (only for goals active at first encounter; closed goals get `None` sentinel and are never read) vs. recompute h's on each `_compute_F` |

`ValueError` raised if `is_opt=True` with `agg` not in MIN/MAX.

### Properties

| Property | Type | Description |
|---|---|---|
| `problem` | `ProblemSPP[State]` | Underlying problem |
| `name` | `str` | Algorithm name |
| `recorder` | `Recorder` | Event recorder (active iff `is_recording=True`) |
| `solutions` | `dict[State, SolutionSPP]` | Goal → solution after `run()` |
| `agg` | `str` | Φ name ('MIN', 'MAX', ..., 'CUSTOM') |
| `is_lazy` | `bool` | |
| `is_opt` | `bool` | |
| `store_vector` | `bool` | |
| `counters` | `dict[str, int]` | Per-run op counters (see below) |

### Methods

```python
def run(self) -> dict[State, SolutionSPP]
def reconstruct_path(self, goal: State) -> list[State]
```

`run()` resets all per-run state (including counters), then
executes the kA*_agg loop. `reconstruct_path(goal)` walks
parent-pointers; `[]` if goal was never reached.

### Counters (`self.counters`)

Reset on every `run()` call. Runtime decomposition for the
8-config benchmark.

| counter | when incremented |
|---|---|
| `cnt_h_search` | h call in normal flow (start seed, push, decrease-g). Under `store_vector=True`, counts only the first-encounter h calls for goals that were active at that moment. |
| `cnt_h_update` | h call in refresh flow (lazy pop-recompute, eager `_refresh_all_F`). Always 0 when `store_vector=True` (vector cached). |
| `cnt_phi_search` | `_compute_F` from search flow |
| `cnt_phi_update` | `_compute_F` from refresh flow |
| `cnt_push` | every `frontier.push` (incl. lazy re-insertions, eager bulk re-push) |
| `cnt_pop` | every `frontier.pop` |
| `cnt_pop_stale` | subset of `cnt_pop`: stale-F re-insertions (lazy only) |
| `cnt_decrease` | every `frontier.decrease` |

### Recording schema

Event types emitted when `is_recording=True`:

| event | payload | when |
|---|---|---|
| `push` | state, g, h, f, parent | every `frontier.push` (initial seed, child handling, eager bulk re-push). Lazy stale re-push does NOT emit. |
| `pop` | state, g, h, f | every non-stale pop (after lazy refresh). Stale pops do NOT emit `pop`. |
| `decrease_g` | state, g, h, f, parent | every decrease-key |
| `on_goal` | state, g, reason, goal_index | goal expanded / unreachable |
| `update_frontier` | num_nodes, next_goal_index | eager refresh boundary (eager only) |
| `update_heuristic` | state, h_old, h_new | per-node F change during eager refresh OR lazy stale-pop re-insertion |
| `h_calc` | state, goal, value, phase | single h(state,goal) evaluation; `phase ∈ {search, update}` |
| `phi_calc` | state, value, phase | every `_compute_F` call; `value` = aggregated Φ (0 when no active goals) |
| `responsible_set` | state, responsible | `self._responsible[state]` assignment (is_opt only) |
| `refresh_skip` | state, reason | opt short-circuit; `reason ∈ {lazy_responsible_active, eager_responsible_unchanged}` |
| `pop_stale` | state, f_stored, f_recomputed | lazy pop found stale F (precedes the `update_heuristic` + lazy re-push) |

**Param → distinguishing events:**

| param | distinguishing events |
|---|---|
| `is_lazy` | `pop_stale` (lazy only); `update_frontier` (eager only) |
| `is_opt` | `responsible_set`, `refresh_skip` (opt only) |
| `store_vector` | `h_calc` count drops to 0 after each state's first `_compute_F`; first-encounter `h_calc` events only fire for goals active at that moment (closed goals are skipped) |

## 3) Inheritance (Hierarchy)

```
Generic[State]
    └── KAStarAgg[State]   (no further base; orchestrator class)
```

Composition over inheritance — does **not** extend `AlgoSPP`.
Owns its own search loop, frontier, and bookkeeping; reuses
`Recorder`, `FrontierPriority`, and `_aggregations.resolve_agg`.

## 4) Dependencies

- `f_core.recorder.Recorder` — event capture.
- `f_hs.algo.omspp._internal._aggregations.resolve_agg` —
  string-or-callable → (Φ, name) resolver (MIN / MAX / AVG /
  RND / PROJECTION / CUSTOM).
- `f_hs.frontier.i_1_priority.FrontierPriority` — indexed
  min-heap with `push` / `pop` / `decrease` / `clear` (all O(log n)).
- `f_hs.problem.i_0_base.ProblemSPP` — provides `starts`,
  `goals`, `successors`, `w`.
- `f_hs.solution.SolutionSPP` — cost-only solution holder.
- `f_hs.state.i_0_base.StateBase` — generic state bound.

## 5) Usage example

```python
from f_hs.algo.omspp.i_1_kastar_agg import KAStarAgg
from f_hs.problem.i_1_grid import ProblemGrid

p = ProblemGrid.Factory.grid_4x4_obstacle()
grid = p.grid
p._goals = [p._states[grid[0][3]], p._states[grid[3][3]]]

def manhattan(s, g):
    return (abs(s.key.row - g.key.row)
            + abs(s.key.col - g.key.col))

# Pareto-optimal config for Φ=MIN:
algo = KAStarAgg(problem=p, h=manhattan, agg='MIN',
                 is_lazy=True, is_opt=True, store_vector=True)
solutions = algo.run()
counts = algo.counters

# Sweep all 8 configs for a benchmark:
for is_lazy in (False, True):
    for is_opt in (False, True):
        for store_vector in (False, True):
            algo = KAStarAgg(problem=p, h=manhattan, agg='MIN',
                             is_lazy=is_lazy, is_opt=is_opt,
                             store_vector=store_vector)
            algo.run()
            print((is_lazy, is_opt, store_vector), algo.counters)
```

See `_tester.py` for canonical small problems (`_abc`,
`_diamond`, `grid_4x4_obstacle`) and `_factory.py` for
`KAStarAgg.Factory.*` constructors.
