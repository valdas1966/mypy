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

| Property | Type | Description | Source |
|---|---|---|---|
| `problem` | `ProblemSPP[State]` | Underlying problem | `Algo` |
| `name` | `str` | Algorithm name | `HasName` |
| `recorder` | `Recorder` | Event recorder (active iff `is_recording=True`) | `ProcessBase` |
| `elapsed` | `float \| None` | Wall-clock seconds for the most recent `run()` | `ProcessBase` |
| `solutions` | `dict[State, SolutionSPP]` | Goal → solution after `run()` | `AlgoOMSPP` |
| `counters` | `Counters` | Per-run op counters (Mapping; `c == {...}` and `dict(c)` work) | `AlgoOMSPP` |
| `agg` | `str` | Φ name ('MIN', 'MAX', ..., 'CUSTOM') | own |
| `is_lazy` | `bool` | | own |
| `is_opt` | `bool` | | own |
| `store_vector` | `bool` | | own |

### Methods

```python
def run(self) -> SolutionOMSPP        # inherited from Algo
def reconstruct_path(self, goal: State) -> list[State]
```

`run()` (inherited) resets per-run state (counters and
`_solutions` via `AlgoOMSPP._run_pre`; bookkeeping via
`_reset_search_state`), executes the kA*_agg loop in `_run()`,
records `elapsed` in `_run_post`. The returned
`SolutionOMSPP` is a `Mapping[State, SolutionSPP]` — indexing
and `.items()` work as on a dict. The same per-goal map is
also available as `algo.solutions`.
`reconstruct_path(goal)` walks parent-pointers; `[]` if goal
was never reached.

### Counters (`self.counters`)

KAStarAgg declares its own scaffold via `_COUNTER_NAMES`,
extending the `AlgoOMSPP` base with the heuristic, Φ, and
lazy-stale-pop groups. All counters listed below are
present on `algo.counters` (KAStarAgg uses every mechanism).
Reset on every `run()` call. Runtime decomposition for the
8-config benchmark.

| counter | when incremented |
|---|---|
| `cnt_h_search` | h call in normal flow (start seed, push, decrease-g). Under `store_vector=True`, counts only the first-encounter h calls for goals that were active at that moment. |
| `cnt_h_update` | h call in refresh flow (lazy pop-recompute, eager `_refresh_priorities`). Always 0 when `store_vector=True` (vector cached). |
| `cnt_phi_search` | `_compute_F` from search flow |
| `cnt_phi_update` | `_compute_F` from refresh flow |
| `cnt_push` | every `frontier.push` (incl. lazy re-insertions, eager bulk re-push). Frontier-sourced — mirrored from `self._frontier.counters` at end-of-run by `_sync_frontier_counters`. |
| `cnt_pop` | every `frontier.pop`. Frontier-sourced. |
| `cnt_pop_stale` | subset of `cnt_pop`: stale-F re-insertions (lazy only). Algo-level (the frontier can't see staleness — it's a g/F semantic). |
| `cnt_decrease` | every `frontier.decrease`. Frontier-sourced. |

### Within/between elapsed split

KAStarAgg accepts `is_timing: bool = True` and exposes
`elapsed_search` / `elapsed_update` (inherited from
`AlgoOMSPP`). Phase-flip sites by mode:

| mode | flip site | result |
|---|---|---|
| **eager** | around `_refresh_priorities` after each goal-find | `elapsed_update > 0` |
| **lazy** | (no flips) | `elapsed_update == 0.0` by design |

**Why lazy reports zero `elapsed_update`:** lazy mode chose to
defer refresh into the search loop (pop-time stale checks)
rather than batch it between phases. Structurally there *is*
no between-phase moment — only one continuous best-first
search. The lazy stale-pop branch's wall-clock falls into
`elapsed_search` (where the work happens). The work-type
counters (`cnt_h_update`, `cnt_phi_update`, `cnt_pop_stale`)
still increment to record that refresh-typed work occurred —
they tag the WORK TYPE; the elapsed buckets tag the
STRUCTURAL PHASE. Two complementary axes.

**Overhead:** at k=200, eager has ~2k = 400 flips × ~150 ns =
**60 µs**. Lazy has 0 flips → **0 overhead**. Both are
invisible against typical Agg runtimes.

### Recording schema

**Minimal, INC-aligned: 5 event types.** Every concrete OMSPP
algorithm (KAStarInc, KAStarAgg, KBFS, KDijkstra) emits the
same `push` / `pop` / `decrease_g` / `on_goal` /
`update_frontier` set, so cross-algo recording-stream
comparisons line up directly.

| event | payload | when |
|---|---|---|
| `push` | state, g, h, f, parent | first-time push (initial seed + `_handle_child` first-encounter branch, one per `cnt_generated`) AND the lazy re-push of any non-last goal at goal-find. Eager bulk re-push and lazy stale re-push are silent. Stream's `push`-event count = `cnt_generated` + (number of non-last reached goals). |
| `pop` | state, g, h, f | non-stale pop only (real expansion or goal-find). Lazy stale pops are silent. Stream's `pop`-event count = `cnt_pop − cnt_pop_stale`. |
| `decrease_g` | state, g, h, f, parent | every decrease-key (one per `cnt_decrease`) |
| `on_goal` | state, g, reason, goal_index | goal expanded / unreachable. Emitted BEFORE the goal re-push (INC-symmetric ordering). |
| `update_frontier` | num_nodes, next_goal_index | eager refresh boundary (eager only — lazy mode does NOT emit; no between-phase moment). Emitted AFTER the goal re-push event. |

**Goal-handling order at every goal-find** (INC-symmetric
lazy re-push):

```
pop  →  on_goal  →  push (re-push, if non-last)
                 →  update_frontier (eager only)
```

The just-found goal is NOT force-expanded at goal-find. It
is removed from `active_goals` and re-pushed onto OPEN with
its g and a fresh F under the shrunken active set's Φ.
Successors of the goal are reached via other paths during
the search; if the goal's optimal-path-to-other-goal role
matters, the re-pushed entry will re-pop in priority order
and the standard close+expand fires (in the non-goal
branch). The last active goal is NEVER re-pushed (no
consumer for its expansion). The pattern is one-to-one
symmetric to KAStarInc's lazy re-push.

**Param → distinguishing event signal:**

| param | distinguishing signal |
|---|---|
| `is_lazy=False` | `update_frontier` markers fire (one per non-last goal-find) |
| `is_lazy=True`  | no `update_frontier` markers; `cnt_pop_stale > 0` (counter, not event) |
| `is_opt`        | not visible in events — only via counter deltas (`cnt_phi_update` / `cnt_h_update` drop) |
| `store_vector`  | not visible in events — only via counter deltas (`cnt_h_search`, `cnt_h_update`) |

**Refresh-internal events removed.** `update_heuristic`,
`pop_stale`, `h_calc`, `phi_calc`, `responsible_set`,
`refresh_skip` were dropped (2026-05-06) for INC-consistency
and recorder-overhead reduction at large k. The aggregate
counters `cnt_h_search` / `cnt_h_update` / `cnt_phi_search` /
`cnt_phi_update` / `cnt_pop_stale` preserve the work-type
observability.

**Goal force-expand replaced with lazy re-push (2026-05-07).**
Previously the goal-find branch added the goal to closed and
generated its successors before emitting `on_goal`
(force-expand). The new flow defers expansion: the goal is
re-pushed and only close+expanded on natural re-pop. Saves
last-goal expansions and any non-last goal whose successors
are reached via other paths. Symmetric to KAStarInc's
`algo._push(state=goal)` lazy re-push.

### Visual counter snapshot — `COUNTERS.html`

Dark-themed 10 × 8 table of counter values for all 8 param
configs on the canonical OMSPP problem (matches the pins in
`_tester_counters.py` exactly). Each counter row is followed
by a one-sentence explanation of why the values differ across
configs (or why the row is invariant), so the table doubles as
documentation of which axis affects which counter and why.
Layout: 3-level grouped header
(`is_lazy` > `is_opt` > `store_vector`); cells coloured green
for row-minimum, grey for invariant rows.

## 3) Inheritance (Hierarchy)

```
f_cs.algo.Algo[ProblemSPP[State], SolutionOMSPP]
    └── AlgoOMSPP[State]
            └── KAStarAgg[State]
```

Inherits the standard `Algo` lifecycle from `AlgoOMSPP`:
`run()` is the public entry, calls `_run_pre()` →
`_run()` → `_run_post()`. `_run()` is the override here —
it executes the kA*_agg loop and returns a `SolutionOMSPP`
wrapping `self._solutions`. `elapsed`, `recorder`, `name`,
`problem`, `counters`, `solutions` are all inherited.

Composition over `AlgoSPP` — does **not** extend the SPP
search loop. Owns its own loop, frontier, and bookkeeping;
reuses `Recorder` (via inherited `recorder`),
`FrontierPriority`, and `_aggregations.resolve_agg`.

## 4) Dependencies

- `f_hs.algo.i_1_omspp.i_0_base.AlgoOMSPP` — base class
  (lifecycle + 8-counter scaffold).
- `f_hs.algo.i_1_omspp.i_1_kastar_agg._aggregations.resolve_agg` —
  string-or-callable → (Φ, name) resolver (MIN / MAX / AVG /
  RND / PROJECTION / CUSTOM).
- `f_hs.frontier.i_1_priority.FrontierPriority` — indexed
  min-heap with `push` / `pop` / `decrease` / `clear` (all O(log n)).
- `f_hs.problem.i_0_base.ProblemSPP` — provides `starts`,
  `goals`, `successors`, `w`.
- `f_hs.solution.SolutionOMSPP` — Mapping-like wrapper of
  `{goal: SolutionSPP}` returned from `run()`.
- `f_hs.solution.SolutionSPP` — cost-only per-goal solution.
- `f_hs.state.i_0_base.StateBase` — generic state bound.

## 5) Usage example

```python
from f_hs.algo.i_1_omspp.i_1_kastar_agg import KAStarAgg
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
