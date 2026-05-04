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

`AlgoOMSPP` provides an 8-counter scaffold. KAStarInc populates
five of the eight; the remaining three (`cnt_phi_*`,
`cnt_pop_stale`) stay at 0 with documented reasons:

| counter | KAStarInc semantics |
|---|---|
| `cnt_h_search` | h(state, goal) calls during sub-search execution. Routed by phase tag (default `'search'`); incremented inside the wrapped h-callable. |
| `cnt_h_update` | h(state, goal) calls during inter-sub-search transitions. The orchestrator flips `self._phase = 'update'` around `_emit_frontier_transition` (prev_h+new_h per frontier state) AND the explicit `algo.refresh_priorities()` call (one h-call per frontier state). All such calls land here. |
| `cnt_push` | total `frontier.push` calls across the whole INC run — includes initial seed push, child-handling pushes, force-expand pushes, and the explicit `algo.refresh_priorities()` drain-and-rebuild pushes. Sourced from the shared `FrontierPriority` (single instance accumulates across all k sub-searches). |
| `cnt_pop` | total `frontier.pop` calls. Frontier-sourced. |
| `cnt_decrease` | total `frontier.decrease` calls (decrease-key during child handling). Frontier-sourced. |
| `cnt_phi_*` | always 0 — Inc has no Φ aggregation. |
| `cnt_pop_stale` | always 0 — Inc has no lazy stale-pop branch. |

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
| Around `_emit_frontier_transition` (iterations 1+) | SEARCH → UPDATE → SEARCH (auto on next loop iter) | h-calls for `prev_h+new_h` per frontier state belong to between-phase work |
| Before explicit `algo.refresh_priorities()` | SEARCH → UPDATE | drain-and-rebuild + h-calls per frontier state |
| Before `algo.resume()` | UPDATE → SEARCH | resumed sub-search loop is search work |
| Force-expand | (no flip — stays in SEARCH) | Stern's framing — still part of sub-search i |

At k=200, ~4(k−1) = ~800 active flips × ~150 ns = **120 µs**
overhead. Negligible vs. typical Inc runtimes (100 ms+).

### Always-evaluate during transition

`_emit_frontier_transition` evaluates `prev_h(s)` and `new_h(s)`
for every frontier state **even when `is_recording=False`**.
This keeps `cnt_h_update` consistent between recording and
non-recording runs — important for benchmarks that disable
recording for performance but still need accurate counter
totals.

## Algorithm

```
shared = None
for i, goal_i in enumerate(problem.goals):
    if shared and goal_i in shared.closed:
        # Fast-path: goal already expanded by an earlier
        # sub-search. Its g is optimal under consistent h.
        emit on_goal(reason='already_closed')
        continue

    if shared is not None:
        emit update_frontier(num_nodes=len(shared.frontier))
        for state in shared.frontier:
            emit update_heuristic(state, h_{i-1}(state), h_i(state))
        shared.goal_reached = None

    algo = AStar(sub_problem(goal_i), h=h_i, search_state=shared)
    algo._recorder = self._recorder     # share the event log
    sol = algo.run() if i == 0 else algo.resume()

    if sol reachable:
        # Force-expand the goal (AStar returned before
        # closing/expanding it). Necessary so future sub-
        # searches can reach beyond this goal.
        shared.closed.add(goal_i)
        for child in successors(goal_i):
            algo._handle_child(parent=goal_i, child=child)

    emit on_goal(reason=reached ? 'expanded' : 'unreachable')
    shared = algo.search_state
```

## Recording — event schema

In addition to the standard AStar events (`push`, `pop`,
`decrease_g`), KAStarInc emits three meta-events:

### `on_goal`
```
{type: 'on_goal',
 state: <goal>,
 g: int | float('inf'),
 reason: 'expanded' | 'already_closed' | 'unreachable',
 goal_index: int}
```
One per goal, at sub-search termination. `goal_index` is the
0-based position in `problem.goals`, preserving identifiability
for duplicate goals.

### `update_frontier`
```
{type: 'update_frontier',
 num_nodes: int,
 next_goal_index: int}
```
Boundary marker before priority refresh on sub-search
transition (iterations 1+). Not emitted before iteration 0
(no transition) nor before a fast-path iteration (no refresh
needed).

### `update_heuristic`
```
{type: 'update_heuristic',
 state: <state>,
 h_old: int,
 h_new: int}
```
One per frontier state, emitted in a cluster after
`update_frontier`. Documents the heuristic swap from the
previous goal's h to the current goal's h. Emitted for EVERY
frontier state (not only those whose h changed) — research
visibility over minimalism, per this class's analytical use
case.

## Interaction with existing machinery

| Mechanism | Role in kA*_inc |
|---|---|
| `SearchStateSPP` | The shared bundle passed between sub-searches |
| `AStar.resume()` | How iterations 1+ continue without reinit |
| `AlgoSPP.refresh_priorities()` | Auto-invoked on first resume() via `_frontier_dirty=True`; rebuilds the heap with the new heuristic |
| `_frontier_dirty` flag | Set by `AStar(search_state=...)`; cleared on first refresh |
| Recorder sharing | `algo._recorder = self._recorder` override — all AStar sub-instances write to KAStarInc's Recorder |

## Force-expand of reached goals

AStar's `_search_loop` returns on goal-pop WITHOUT closing the
goal or expanding its successors (standard A* — the goal is
the search's output, not an intermediate node). For kA*_inc's
state-sharing to be useful, the reached goal must be in CLOSED
and its successors on the frontier before the next sub-search
begins.

KAStarInc performs this force-expand explicitly after each
sub-search returns with `expanded`:
```
shared.closed.add(goal)
for child in successors(goal):
    algo._handle_child(parent=goal, child=child)
```
The `_handle_child` call emits standard `push` / `decrease_g`
events, so the force-expand is visible in the event log.

## Factory

| Method | Description |
|---|---|
| `graph_abc_two_goals()` | A→B→C with goals=[B, C]; both expanded |
| `graph_abc_cached_at_b_first()` | goals=[C, B]; B hits already_closed fast-path |

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
