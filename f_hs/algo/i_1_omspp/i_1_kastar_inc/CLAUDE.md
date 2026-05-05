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
          is_recording: bool = False)
```
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

### Counters (`self.counters`)

KAStarInc declares its own scaffold via `_COUNTER_NAMES`,
extending the `AlgoOMSPP` base with the heuristic group.
`cnt_phi_*` and `cnt_pop_stale` are **absent** — Inc has no
Φ aggregation and no lazy stale-pop branch, so those names
are not in the counter dict at all.

| counter | KAStarInc semantics |
|---|---|
| `cnt_h_search` | h(state, goal) calls during sub-search execution. Routed by phase tag (default `'search'`); incremented inside the wrapped h-callable. |
| `cnt_h_update` | h(state, goal) calls during inter-sub-search transitions. The orchestrator flips `self._phase = 'update'` around the explicit `algo.refresh_priorities()` call (one h-call per frontier state during the drain-and-rebuild). All such calls land here. |
| `cnt_push` | total `frontier.push` calls across the whole INC run — includes initial seed push, child-handling pushes, lazy re-push of reached non-last goals, and the explicit `algo.refresh_priorities()` drain-and-rebuild pushes. Sourced from the shared `FrontierPriority` (single instance accumulates across all k sub-searches). |
| `cnt_pop` | total `frontier.pop` calls. Frontier-sourced. |
| `cnt_decrease` | total `frontier.decrease` calls (decrease-key during child handling). Frontier-sourced. |
| `mem_open` / `mem_closed` | post-run memory snapshot of the shared `SearchStateSPP` bundle. |

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
        algo._push(state=goal_i)

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

## Interaction with existing machinery

| Mechanism | Role in kA*_inc |
|---|---|
| `SearchStateSPP` | The shared bundle passed between sub-searches |
| `AStar.resume()` | How iterations 1+ continue without reinit |
| `AlgoSPP.refresh_priorities()` | Auto-invoked on first resume() via `_frontier_dirty=True`; rebuilds the heap with the new heuristic |
| `_frontier_dirty` flag | Set by `AStar(search_state=...)`; cleared on first refresh |
| Recorder sharing | `algo._recorder = self._recorder` override — all AStar sub-instances write to KAStarInc's Recorder |

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
    algo._push(state=goal)         # re-enter OPEN with optimal g
```

The re-push emits a standard `push` event. The `_push` call
uses the current sub-search's h_i for the priority computation;
the next transition's `refresh_priorities()` will re-key it
under h_{i+1}, alongside the rest of the frontier.

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
