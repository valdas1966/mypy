# KAStarInc — Incremental kA*

## Purpose

Solves the One-to-Many Shortest Path Problem (OMSPP): finds `k`
shortest paths from a shared start `s` to each of `k` goal
states `[t₁, ..., tₖ]`, one per goal.

Runs `k` sequential A* sub-searches. Each sub-search reuses
the `SearchStateSPP` bundle (OPEN, CLOSED, g-values, parent
pointers) produced by earlier sub-searches. Only the heuristic
changes between iterations — one priority refresh per
transition.

Based on Stern et al. "Heuristic Search for OMSPP and MOSPP"
(Algorithm kA*_inc). Under consistent heuristics, kA*_inc
expands the same set of nodes as kA*_min up to tie-breaking
while computing only **one** heuristic per node per sub-search
(vs `k` for kA*_min).

## Public API

### Constructor
```python
KAStarInc(problem: ProblemSPP[State],
          h: Callable[[State, State], int],
          name: str = 'KAStarInc',
          is_recording: bool = False,
          is_timing: bool = True,
          is_tracing: bool = False)
```
- `is_tracing` — opt-in survival instrument (default off →
  one bool check per transition, zero benchmark overhead).
  See **Survival instrument** below.
- `problem.goals` provides the goal list `[t₁, ..., tₖ]`.
- `h(state, goal) -> int` — bi-arg heuristic. Each sub-search
  closes over its goal via default-arg idiom (no late-binding
  pitfall).
- Assumes **consistent heuristics** — required for the
  "same-nodes-as-kA*_min" guarantee and the already-closed
  fast-path's correctness.

### Methods
| Method | Description |
|---|---|
| `run() -> SolutionOMSPP` | Inherited from `Algo`; orchestrates k sub-searches via `_run()`. Returns a `SolutionOMSPP` (Mapping over `{goal: SolutionSPP}`). |
| `extend(new_goals) -> SolutionOMSPP` | Resume the orchestrator with additional goals appended to the sequence solved by `run()` (or any prior `extend()`). Reuses `_shared_state`, `_solutions`, `_counters`, `_recorder`. Returns a `SolutionOMSPP` over the FULL set of goals seen so far. Provided by `ExtendableOMSPP` mixin. |
| `run_nested(problems, h, ...)` *(classmethod)* | Convenience wrapper: solves a prefix-extending sequence of problems via `run(problems[0])` then chained `extend()` calls. Provided by `ExtendableOMSPP` mixin. |
| `reconstruct_path(goal) -> list[State]` | Walk parents back to start for any goal (expanded or fast-path). |

### Properties
| Property | Type | Description | Source |
|---|---|---|---|
| `problem` | `ProblemSPP` | Input OMSPP problem | `Algo` |
| `name` | `str` | Algorithm name | `HasName` |
| `recorder` | `Recorder` | Shared event stream across all sub-searches | `ProcessBase` |
| `elapsed` | `float \| None` | Wall-clock seconds for the most recent `run()` | `ProcessBase` |
| `solutions` | `dict[State, SolutionSPP]` | Per-goal solutions after `run()` | `AlgoOMSPP` |
| `counters` | `Counters` | Per-run op counters (Mapping; `c == {...}` and `dict(c)` work) | `AlgoOMSPP` |
| `search_state` | `SearchStateSPP \| None` | Shared bundle for post-hoc inspection | own |
| `is_tracing` | `bool` | Whether the survival instrument is active | own |
| `survival` | `dict[State, int]` | Per-node `{node: #transitions in OPEN}` (= node's `cnt_h_update` h-calls). Empty when `is_tracing=False`. A copy. | own |
| `survival_histogram` | `dict[int, int]` | `{survival_count: num_nodes}`, ascending. The report visual. Empty when `is_tracing=False`. | own |

### Counters (`self.counters`)

KAStarInc declares its own scaffold via `_COUNTER_NAMES`,
extending the `AlgoOMSPP` base with the heuristic group.
`cnt_phi_*` and `cnt_pop_stale` are **absent** — Inc has no
Φ aggregation and no lazy stale-pop branch, so those names
are not in the counter dict at all.

| counter | KAStarInc semantics |
|---|---|
| `cnt_h_search` | h(state, goal) calls during sub-search execution. Routed by phase tag (default `'search'`); incremented inside the wrapped h-callable. **Excludes the lazy goal re-push**: `_lazy_repush` pushes with the exact `(g, -g, goal)` priority and does NOT call h (for consistent h, `h_i(goal, goal) = 0`; the value is overwritten by the next transition's refresh before any pop). |
| `cnt_h_update` | h(state, goal) calls during inter-sub-search transitions. The orchestrator flips `self._phase = 'update'` around the explicit `algo.refresh_priorities()` call (one h-call per frontier state during the drain-and-rebuild). All such calls land here. |
| `cnt_push` | total `frontier.push` calls across the whole INC run — includes initial seed push, child-handling pushes, lazy re-push of reached non-last goals, and the explicit `algo.refresh_priorities()` drain-and-rebuild pushes. Sourced from the shared `FrontierPriority` (single instance accumulates across all k sub-searches). |
| `cnt_pop` | total `frontier.pop` calls. Frontier-sourced. |
| `cnt_decrease` | total `frontier.decrease` calls (decrease-key during child handling). Frontier-sourced. |
| `mem_open` / `mem_closed` | post-run memory snapshot of the shared `SearchStateSPP` bundle. `mem_open` uses the shared `FrontierPriority.max_size` (rule-2 + rule-3: same frontier accumulates across all k sub-searches, so `max_size` is the cross-sub-search lifetime peak). |
| `mem_total` | `Σ mem_*` — conservative upper-bound coincident peak. |

Frontier-sourced values are mirrored into `self._counters` at
end-of-run by `_sync_frontier_counters()` (called automatically
by `AlgoOMSPP._run_post`). The frontier is the single source of
truth for heap-op counts; INC reads `self._shared_state.frontier.counters`
once per run and copies into the algo's 8-counter scaffold via
`Counters.assign`.

### Within/between elapsed split

KAStarInc accepts `is_timing: bool = True` and exposes
`elapsed_search` / `elapsed_update` (inherited from
`AlgoOMSPP`). Phase-flip sites in `_run`:

| site | flip | reason |
|---|---|---|
| Around `_emit_frontier_transition` + `refresh_priorities` (iterations 1+) | SEARCH → UPDATE → SEARCH (auto on next loop iter) | drain-and-rebuild + h-calls per frontier state belong to between-phase work |
| Before `algo.resume()` | UPDATE → SEARCH | resumed sub-search loop is search work |
| Lazy re-push of reached non-last goal | (no flip — stays in SEARCH) | the re-push completes the just-finished sub-search's goal handling |

At k=200, ~4(k−1) = ~800 active flips × ~150 ns = **120 µs**
overhead. Negligible vs. typical Inc runtimes (100 ms+).

### Recording-independence of `cnt_h_update`

`refresh_priorities()` runs whether or not `is_recording=True`
(it's not gated on the recorder), and the per-state h-calls
it triggers are routed to `cnt_h_update` via the phase tag.
So `cnt_h_update` is consistent between recording and
non-recording runs — important for benchmarks that disable
recording for performance but still need accurate counter
totals.

## Algorithm

```
shared = None
for i, goal_i in enumerate(problem.goals):
    if goal_i in self._solutions:
        # Fast-path A: was a previous sub-search's goal.
        emit on_goal(reason='already_reached')
        continue
    if shared and goal_i in shared.closed:
        # Fast-path B: popped+closed as collateral by an
        # earlier sub-search. g is optimal under consistent h.
        emit on_goal(reason='already_closed')
        continue

    if shared is not None:
        emit update_frontier(num_nodes=len(shared.frontier))
        algo.refresh_priorities()  # silent re-keying under h_i
        shared.goal_reached = None

    algo = AStar(sub_problem(goal_i), h=h_i, search_state=shared)
    algo._recorder = self._recorder     # share the event log
    sol = algo.run() if i == 0 else algo.resume()

    emit on_goal(reason=reached ? 'expanded' : 'unreachable')
    self._solutions[goal_i] = sol

    if reached and i < len(goals) - 1:
        # Lazy re-push: goal re-enters OPEN with optimal g
        # so the next sub-search's natural close+expand fires
        # if/when its f under h_{i+1} clears C_{i+1}. The
        # last goal is NOT re-pushed — no future sub-search
        # would consume the work.
        self._lazy_repush(algo, goal_i)   # h-free re-push

    shared = algo.search_state
```

## Recording — event schema

In addition to the standard AStar events (`push`, `pop`,
`decrease_g`), KAStarInc emits two meta-events:

### `on_goal`
```
{type: 'on_goal',
 state: <goal>,
 g: int | float('inf'),
 reason: 'expanded' | 'already_reached' | 'already_closed'
       | 'unreachable',
 goal_index: int}
```
One per goal, at sub-search termination. `goal_index` is the
0-based position in `problem.goals`, preserving identifiability
for duplicate goals.

Reason values:
- `expanded` — was the active sub-search's goal; A* popped it
  and finalized g.
- `already_reached` — was a prior sub-search's goal (in
  `self._solutions`). Under the lazy re-push design, the goal
  may be on OPEN with finalized g but not in CLOSED, so this
  reason is distinct from `already_closed`.
- `already_closed` — was popped+closed as collateral by an
  earlier sub-search (in `shared.closed` but never a sub-
  search's goal). Consistent h ⇒ g is optimal.
- `unreachable` — A* exhausted OPEN without reaching the goal.

### `update_frontier`
```
{type: 'update_frontier',
 num_nodes: int,
 next_goal_index: int}
```
Boundary marker at the sub-search transition (iterations 1+).
`num_nodes` is the frontier size at the moment of refresh.
Not emitted before iteration 0 (no transition) nor before a
fast-path iteration (no refresh needed).

The per-state `update_heuristic` cluster was removed — the
actual h-value re-keying happens via `refresh_priorities()`
and is observable through `cnt_h_update` (one h-call per
frontier state per transition) and the silent re-push
activity that drains and rebuilds the heap. Recording
overhead at large k drops substantially (was ~k × |frontier|
events per transition; now 1).

## Prefix-extending the goal sequence: `extend()`

`KAStarInc` composes the `ExtendableOMSPP` mixin (at
`f_hs/algo/i_1_omspp/mixins/extendable/`). The mixin
contributes:

- `algo.extend(new_goals)` — resume the orchestrator with
  `new_goals` appended to the sequence already solved.
  Returns a `SolutionOMSPP` over the full sequence.
- `KAStarInc.run_nested(problems, h, ...)` — classmethod
  convenience for a prefix-extending list of problems.

**The per-goal loop body is shared** between `_run()` and
`extend()` via the `_handle_goal(goal, idx)` method. `_run`
sets `self._all_goals = list(self.problem.goals)` and
iterates; `extend` appends to `self._all_goals` and iterates
at the offset. The lazy-re-push decision (`idx <
len(self._all_goals) - 1`) automatically tracks the new
"last goal" boundary.

**Trailing reached goal re-push.** After the last goal of a
run/extend, lazy re-push is *skipped* (no consumer for the
work). When `extend()` arrives, that previously-last goal
now has consumers — `_repush_last_reached_goal()` performs
the deferred re-push (also h-free, via `_lazy_repush`)
before the new goal loop's first transition. The transition's
own `refresh_priorities()` then re-keys the re-pushed entry
under the new goal's `h`.

**Bookkeeping (set by `_handle_goal`):**

| field | semantics |
|---|---|
| `_all_goals: list[State]` | Full sequence: original goals + every extend's appended goals. |
| `_last_reached_goal: State \| None` | Most recent successfully-expanded goal (None after unreachable / fast-path / on-completed-re-push). |
| `_last_algo: AStar \| None` | The sub-search algo instance for `_last_reached_goal` (its `_h` is closed over that goal; used by `_repush_last_reached_goal`). |

**Counters / elapsed / recorder are cumulative across
calls.** `algo.counters` after `extend()` reports the total
work since the original `run()`; same for `algo.elapsed`,
`algo.recorder.events`, and `algo.solutions`. The phase
buckets (`elapsed_search` / `elapsed_update`) likewise
accumulate. To get a per-call breakdown, snapshot
`dict(algo.counters)` and `algo.elapsed` before and after
each `extend()`.

**Preconditions:** `run()` must have completed at least once
(else `RuntimeError`); `new_goals` must be non-empty (else
`ValueError`). Duplicate goals (already in `_solutions` or
`shared.closed`) are handled by the existing fast-paths and
emit `already_reached` / `already_closed` events as during
`_run`.

## Interaction with existing machinery

| Mechanism | Role in kA*_inc |
|---|---|
| `SearchStateSPP` | The shared bundle passed between sub-searches |
| `AStar.resume()` | How iterations 1+ continue without reinit |
| `AlgoSPP.refresh_priorities()` | Auto-invoked on first resume() via `_frontier_dirty=True`; rebuilds the heap with the new heuristic |
| `_frontier_dirty` flag | Set by `AStar(search_state=...)`; cleared on first refresh |
| Recorder sharing | `algo._recorder = self._recorder` override — all AStar sub-instances write to KAStarInc's Recorder |

## Survival instrument (`is_tracing`)

Opt-in, off by default. Answers the question a sceptic
raises about `cnt_h_total`: *"the `cnt_h_search` gap is
definitional (INC computes h once per node, AGG ≈|A|≈k
times) — but couldn't INC's `cnt_h_update` be just as bad?
If a node sits in OPEN across all k sub-searches, the
per-transition refresh re-prices it every time → ≈k h-calls
for that node too."* The instrument shows that worst case
is essentially empty.

**Definition.** `survival[n]` = number of inter-sub-search
transitions at which `n` was in OPEN. The transition
refresh (`AlgoSPP.refresh_priorities()`) re-prices every
OPEN node exactly once (one h-call each, counted as
`cnt_h_update`). Therefore:

```
survival[n] == n's cnt_h_update h-calls
sum(survival.values())
  == sum(s * cnt for s, cnt in survival_histogram.items())
  == counters['cnt_h_update']        # exact invariant
```

A node expanded within its own sub-search never sits
through a refresh → survival 0 → absent from the dict
(it costs zero `cnt_h_update`). `survival_histogram` =
`{survival_count: num_nodes}` is the report visual: almost
all mass at low counts; the tail near k (the AGG-like
≈k-per-node regime) is ≈empty — that is *why*
`cnt_h_update` stays small (empirically avg |OPEN| at a
transition ≈ 1.3 % of explored states at k=200).

**Implementation.** A `dict[State, int]` bumped once per
node in the `_handle_goal` transition block, snapshotting
OPEN immediately *before* `algo.refresh_priorities()` (the
same set refresh will h-recompute). Guarded by
`if self._is_tracing` → one bool test per transition when
off. Reset on `run()`, accumulated across `extend()` (same
lifecycle as counters / recorder).

**Not a benchmark counter.** A per-node histogram is not a
scalar work-count; it is deliberately kept OUT of
`_COUNTER_NAMES` / `algo.counters`, so the benchmark CSV
schema and every pinned counter dict are untouched. It is
exposed as its own `survival` / `survival_histogram`
properties — "a counter" in spirit, a separate structure
in implementation.

**AGG has no analogue.** AGG is a single best-first loop —
there are no sub-searches, so "survives k sub-searches" is
undefined. AGG's per-node h-cost is simply `n_h`≈|A|≈k at
first encounter, already recoverable from AGG's existing
`is_tracing` trace. No new AGG instrumentation was added.

## Lazy re-push of reached non-last goals

AStar's `_search_loop` returns on goal-pop WITHOUT closing the
goal or expanding its successors (standard A* — the goal is
the search's output, not an intermediate node). For kA*_inc's
state-sharing to be useful, *if a future sub-search needs to
traverse this goal*, then the goal must reach CLOSED and its
successors must reach OPEN before the future search expands
past it.

KAStarInc handles this **lazily**: after each non-last reached
goal, the orchestrator re-pushes the goal onto OPEN with its
optimal g. The next sub-search's standard A* loop then either:

- pops the re-pushed goal (when its f under h_{i+1} clears
  C_{i+1}), runs the standard close+expand → goal joins
  CLOSED, successors land on OPEN. Or
- never pops it (when its f stays above C_{i+1}) → goal sits
  on OPEN harmlessly until the orchestrator finishes.

```
if reached and i < len(goals) - 1:
    self._lazy_repush(algo, goal)  # re-enter OPEN, h-free
```

`_lazy_repush` pushes the goal back with priority
`(g, -g, goal)` **without** an h-call, then emits a standard
`push` event. This is exact, not an approximation: KAStarInc
requires a consistent (hence admissible) heuristic, so
`h_i(goal, goal) = 0` and the priority `AStar._priority`
would compute is exactly `(g + 0, -g, goal)`. The next
transition's `refresh_priorities()` drains the whole frontier
and re-keys this entry under h_{i+1} **before any pop can
observe it**, so the `h_i(goal)` value is provably discarded
regardless. Skipping it keeps a provably-zero, immediately-
overwritten h-call out of `cnt_h_search` (the
recording-off benchmark path). Frontier order and the
recorded `push` event (`h = 0`, `f = g` via `_enrich_event`)
are byte-identical to the prior `algo._push(state=goal)`
path; the ONLY observable delta is the lower `cnt_h_search`.

**Why lazy, not eager?**
- The last goal is *guaranteed* to have no consumer for its
  expansion. Eager force-expand at the last goal is pure
  waste; lazy avoids it by construction.
- For non-last goals, lazy expands only if a future search
  needs the goal. Eager always expands (cheap when neighbors
  are already known, but still ≥ 0 work).
- Per Stern et al. Theorem 1 (kA*_inc expands the same nodes
  as kA*_min up to tie-breaking), both designs are
  paper-compliant — the choice is implementation-level.

**Trade-off vs eager force-expand:**
- **Expansions:** lazy ≤ eager always; strictly < at the
  last goal and at any non-last goal whose neighbors no
  future search visits.
- **Heap ops:** lazy can be > eager when the goal's
  neighbors are already known *and* the re-pushed goal
  participates in subsequent `refresh_priorities()` calls
  (one extra silent push per re-push per remaining
  transition). On dense pre-explored grids, eager is
  cheaper on `cnt_push`; on sparse exploration, lazy wins.

**Fast-path predicate (CLOSED ∪ self._solutions).**
A goal can be "finalized" two distinct ways under the lazy
design:
- `goal in self._solutions` — was a prior sub-search's goal;
  fast-path emits `already_reached`.
- `goal in shared.closed` — was popped+closed as collateral;
  fast-path emits `already_closed`.

The two are disjoint at the moment of the check (a re-pushed
goal that gets re-popped during a later sub-search would join
CLOSED, but `self._solutions` is checked first).

## Factory

| Method | Description |
|---|---|
| `graph_abc_two_goals()` | A→B→C with goals=[B, C]; both expanded |
| `graph_abc_cached_at_b_first()` | goals=[C, B]; B hits `already_closed` fast-path (B was popped+expanded as collateral by sub-search 0 while seeking C) |

## Tests

| File | Scope | Count |
|---|---|---|
| `_tester.py` | lifecycle (single-goal, two-goals, fast-path, duplicates, frontier-transition events, recording, reconstruction, closure, search_state exposure, independent-A* equivalence) | 10 |
| `_tester_recording.py` | Full event-stream pins (one per scenario). Scenarios: canonical OMSPP (3 goals; transitions + fast-path), `grid_4x4_obstacle` 2-goal (1 transition + 4-state h-update cluster) | 2 |
| `_tester_counters.py` | full 8-counter dict pin on canonical OMSPP; per-goal optimal costs pin | 2 |
| `_tester_extend.py` | nested-extend manual counter pin on canonical OMSPP — `run([g0])` → `extend([g1])` → `extend([g2])`; at each stage the cumulative non-mem counter dict is asserted against hardcoded values (k=1, k=2, k=3). Drift in either the nested-extend logic or the underlying single-shot algorithm surfaces here. | 1 |
| `_tester_survival.py` | survival instrument: off-by-default inertness, canonical histogram pin (`{1:2, 2:4}`), the `sum(survival) == cnt_h_update` invariant (direct + via histogram), and accumulation across `run()` + `extend()`. | 4 |

## Assumptions & limitations (current scope)

1. **Consistent heuristics required.** Inconsistent h breaks
   Theorem 1's same-nodes guarantee and can invalidate the
   already-closed fast-path. Not enforced at runtime.
2. **Plain AStar internally** (not AStarLookup). Cache /
   bounds / BPMX not composable yet; add a sub-algo factory
   hook here when research demands it.
3. **Positive edge costs** required — inherits from `ProblemSPP`
   and Dijkstra-family correctness conditions.
4. **Shared state mutation.** The inner AStar mutates the
   shared `SearchStateSPP`; the KAStarInc orchestrator relies
   on that side-effect.

## Dependencies

- `f_hs.algo.i_1_omspp.i_0_base.AlgoOMSPP` — base class
  (lifecycle + 8-counter scaffold).
- `f_hs.algo.i_1_astar.AStar`
- `f_hs.algo.i_0_base._search_state.SearchStateSPP`
- `f_hs.algo.i_1_omspp._single_goal_view._SingleGoalView`
- `f_hs.problem.i_0_base.ProblemSPP`
- `f_hs.solution.SolutionOMSPP`, `f_hs.solution.SolutionSPP`
