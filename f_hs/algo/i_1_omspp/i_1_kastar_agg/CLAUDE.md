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
| `cnt_h_search` | h call during PHASE_SEARCH (= inside the main search loop): start seed, first-time push (in `_handle_child`), decrease-g, lazy pop-time staleness check, AND the eager goal re-push at goal-find. Under `store_vector=True`, counts only the first-encounter h calls (later reads hit the vector cache). |
| `cnt_h_update` | h call during PHASE_UPDATE — strictly the body of `_refresh_priorities` (eager-only). The just-re-pushed goal is skipped via `just_re_pushed_state` (2026-05-09). **Lazy: always 0** — lazy never enters PHASE_UPDATE; its active-set-change response runs inside the search loop at pop time. Always 0 when `store_vector=True`. |
| `cnt_phi_search` | `_compute_F` during PHASE_SEARCH (parallel to `cnt_h_search`: first-encounter, decrease-g, lazy stale-pop, eager goal re-push). |
| `cnt_phi_update` | `_compute_F` during PHASE_UPDATE (eager refresh body only). **Lazy: always 0**. Independent of `store_vector` (Φ runs even when h is cached). |
| `cnt_push` | every `frontier.push` (incl. lazy re-insertions, eager bulk re-push). Frontier-sourced — mirrored from `self._frontier.counters` at end-of-run by `_sync_frontier_counters`. |
| `cnt_pop` | every `frontier.pop`. Frontier-sourced. |
| `cnt_decrease` | every `frontier.decrease`. Frontier-sourced. |
| `cnt_expanded` | popped state whose successors were generated (Stern-style "expansions"). Incremented inside the main loop. |
| `cnt_generated` | first-time push (state newly enters OPEN; excludes refresh re-pushes, lazy-re-pushed goals, decrease-key). |
| `mem_open` | post-run snapshot — frontier struct + g/parent slots in OPEN. Strict bucket: does NOT include the AGG aux structures (those live in `mem_aux`). |
| `mem_closed` | post-run snapshot — `closed` set + g/parent slots in CLOSED. Strict bucket. |
| `mem_aux` | post-run snapshot — bytes carried by AGG's auxiliary per-state structures that live OUTSIDE OPEN/CLOSED: `_F_stored` (always), `_h_vector` (only when `store_vector=True`), `_responsible` (only when `is_opt=True`). Computed by the overridden `_sync_memory_snapshot` after `super()` fills `mem_open`/`mem_closed`. Shallow `sys.getsizeof` accounting consistent with the base. |

Stale pops are NOT a separate counter — they share the same heap-op cost as real pops (both do one `frontier.pop`), and their additional re-push contribution lives in `cnt_push`. The stale subset is derivable: `stale_pops = cnt_pop − cnt_expanded − #on_goal_events`.

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
search. Under Path D (2026-05-11) the counter axis mirrors
this structural reality exactly: `cnt_*_search` counts h / Φ
work done in PHASE_SEARCH (including the lazy pop-time
staleness check and the eager goal re-push), and
`cnt_*_update` counts work in PHASE_UPDATE (eager refresh
body only). **Lazy mode reports `cnt_*_update = 0`** — both
the counter and elapsed axes agree it does no work between
sub-search segments.

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
| `pop` | state, g, h, f | non-stale pop only (real expansion or goal-find). Lazy stale pops are silent. Stream's `pop`-event count = `cnt_pop − stale_pops` where `stale_pops = cnt_pop − cnt_expanded − #on_goal`. |
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
| `is_lazy=True`  | no `update_frontier` markers; `cnt_pop > cnt_expanded + #on_goal` (stale-pop derivation > 0) |
| `is_opt`        | not visible in events — only via counter deltas (`cnt_phi_update` / `cnt_h_update` drop in eager; `cnt_phi_search` / `cnt_h_search` drop in lazy) |
| `store_vector`  | not visible in events — only via counter deltas (`cnt_h_search` falls to first-encounter floor; `cnt_h_update` falls to 0) |

**Refresh-internal events removed.** `update_heuristic`,
`pop_stale`, `h_calc`, `phi_calc`, `responsible_set`,
`refresh_skip` were dropped (2026-05-06) for INC-consistency
and recorder-overhead reduction at large k. The aggregate
counters `cnt_h_search` / `cnt_h_update` / `cnt_phi_search` /
`cnt_phi_update` preserve the work-type observability; stale
pops are derivable from `cnt_pop − cnt_expanded − #on_goal`.

**Goal force-expand replaced with lazy re-push (2026-05-07).**
Previously the goal-find branch added the goal to closed and
generated its successors before emitting `on_goal`
(force-expand). The new flow defers expansion: the goal is
re-pushed and only close+expanded on natural re-pop. Saves
last-goal expansions and any non-last goal whose successors
are reached via other paths. Symmetric to KAStarInc's
`algo._push(state=goal)` lazy re-push.

**Eager refresh skips the just-re-pushed goal
(2026-05-09).** `_refresh_priorities` accepts a new
`just_re_pushed_state` parameter; for that state the
F-recompute is skipped (the value was already computed
under the new active set at the re-push site). Rationale:
the goal re-push and the bulk refresh are independent
code paths that previously both recomputed F on the just-
re-pushed goal — yielding identical values. Saves 2
h-calls + 1 Φ-call per non-last goal-find in `is_opt=False`
configs (the `is_opt=True` case already skipped via the
responsible-set rule). All cross-config search-phase
invariants preserved at the time of landing.

**Path D — strictly temporal counter taxonomy + lazy goal-
repush skip (2026-05-11).** The counter axis is now
perfectly aligned with the structural `phase` axis:

  - `cnt_*_search` counts every h / Φ call done during
    PHASE_SEARCH (inside the main search loop): first-
    encounter, decrease-g, lazy pop-time staleness check,
    AND the eager goal re-push (which lives temporally in
    SEARCH — the structural flip to UPDATE happens around
    the bulk refresh, not the re-push). Reverts the
    2026-05-08 retag of the goal re-push as UPDATE.
  - `cnt_*_update` counts every h / Φ call done during
    PHASE_UPDATE — strictly the body of
    `_refresh_priorities` (eager-only). **Lazy mode never
    enters PHASE_UPDATE → `cnt_*_update = 0` always.** A
    parametrized invariant test pins this.

  In addition, the lazy branch at goal-find no longer
  computes F under the shrunken active set. It pushes the
  goal back with its STALE F (= popped F) and lets the
  lazy stale-pop machinery refresh it on the next pop.
  Embodies the lazy-mode contract: do no active-set-
  change-response work between sub-search segments —
  defer it to pop time. Cost on the canonical: +2 stale
  pops (one per non-last goal), so `cnt_pop` goes 16 → 18,
  `cnt_push` 20 → 22. The stale subset (derivable as
  `cnt_pop − cnt_expanded − #on_goal`) goes 4 → 6.

  Counter deltas on the canonical 8-config matrix vs.
  Path B (2026-05-10):

  - Removed counters: `cnt_h_pop_staleness`,
    `cnt_phi_pop_staleness`.
  - `cnt_h_search`: 34 invariant → eager nosv 37 / eager
    sv 34 / lazy_noopt_nosv 69 / lazy_noopt_sv 34 /
    lazy_opt_nosv 42 / lazy_opt_sv 34. No longer
    invariant — the lazy stale-pop and goal-re-push
    h-work now lives here. Cross-config differences are
    informative: cost of lazy stale-pop is now directly
    legible as `lazy_h_search − eager_h_search`.
  - `cnt_h_update`: 11 → 8 (eager_noopt_nosv, lost the 3
    goal-re-push h-calls); 8 → 5 (eager_opt_nosv); 0 (all
    sv + all lazy).
  - `cnt_phi_search`: 14 invariant → eager invariant at
    16 (= 14 + 2 goal re-pushes); lazy varies (lazy_noopt
    32; lazy_opt 20).
  - `cnt_phi_update`: 8 → 6 (eager_noopt); 6 → 4
    (eager_opt); 0 (all lazy).
  - Heap-op deltas (lazy only): see above.

  Recording stream impact: lazy goal-re-push push events
  now carry the stale F (h=0 for MIN since stored_f =
  g_state). The silent stale-pop refreshes them on the
  next pop. The `_LAZY_CANONICAL` recording fixture
  reflects this. Per-goal optimal costs are unchanged.

### Per-counter trace CSVs — `csvs/`

For each of the 8 param configs there is a folder
`csvs/{config}/` containing one CSV per non-invariant
counter (`cnt_h_search`, `cnt_h_update`, `cnt_phi_search`,
`cnt_phi_update`, `cnt_push`, `cnt_pop` = 6 files). Each
CSV lists every state that contributed to that counter in
process order. Schema: `order, event, state, phase`.

The `phase` column is `'search'` or `'update'` — mirrors
the structural `self.phase` axis (the same one
`elapsed_search` / `elapsed_update` use). Rows inside the
eager `_refresh_priorities` body show `'update'`; every
other site (main loop pop, first-time push, goal re-push,
lazy stale-pop) shows `'search'`. So `cnt_*_update.csv`
rows are uniformly `update`; lazy CSVs are uniformly
`search`; `cnt_push.csv` (eager) is the most informative —
mixes search-phase pushes (first-time, goal re-push) with
update-phase pushes (refresh body), so the
`search → update → search` transitions in `cnt_push`
directly mark where the bulk-refresh body ran.

The number of rows in each CSV equals the corresponding
counter value *only for invariance-1 counters* (where every
increment is +1 — i.e. `cnt_phi_*`, `cnt_push`, `cnt_pop`);
for `cnt_h_*` each row can contribute multiple h-calls
(one per active goal at call time), so the CSV's row count
is `cnt_phi_*` (= number of `_compute_F` invocations).

Regenerate after substantive algo changes:
```
python -m f_hs.algo.i_1_omspp.i_1_kastar_agg._dump_csvs
```
The dumper runs all 8 configs with `is_tracing=True` (an
opt-in constructor flag that populates `algo.traces`, off
by default → zero overhead). The in-memory `algo.traces`
events retain an `n` field (increment amount) for
programmatic cross-checks; the CSV view drops `n` in favor
of `phase`. To cross-check against the pinned counter
totals, sum `algo.traces` directly.

### Visual counter snapshot — `COUNTERS.html`

Dark-themed 9 × 8 table of counter values for all 8 param
configs on the canonical OMSPP problem (matches the pins in
`_tester_counters.py` exactly). Each counter row is followed
by a one-sentence explanation of why the values differ across
configs (or why the row is invariant), so the table doubles as
documentation of which axis affects which counter and why.
Layout: 3-level grouped header
(`is_lazy` > `is_opt` > `store_vector`); cells coloured green
for row-minimum.

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
