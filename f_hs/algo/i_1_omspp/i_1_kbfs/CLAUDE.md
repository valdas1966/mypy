# KBFS — k-BFS for OMSPP

## Purpose

Solves OMSPP via a **single inner BFS pass** that observes each goal at the moment it is popped. Sibling of `KAStarInc` / `KAStarAgg` / `KDijkstra` under `AlgoOMSPP` — independent frame, NOT a KAStarInc subclass.

The BFS expansion order from a single source is goal-independent (FIFO depth-by-depth), so a per-goal sub-search restart with shared state would do exactly the same work as a single pass that observes goal-pops as they occur. KBFS implements the simpler model: one inner BFS, multi-goal early-exit hook.

## Public API

### Constructor
```python
KBFS(problem: ProblemSPP[State],
     name: str = 'KBFS',
     is_recording: bool = False,
     is_timing: bool = True)
```
No `h` kwarg — BFS has no heuristic. The `AlgoOMSPP` base requires `h`, so a dummy `lambda s, g: 0` is passed internally and never invoked.

### Inheritance
```
AlgoOMSPP[State]
    └── KBFS[State]

# inner (private):
AlgoSPP[State]
    └── BFS[State]
            └── _MultiGoalBFS[State]
```

### Methods
| Method | Description |
|---|---|
| `run() -> SolutionOMSPP` | Algo lifecycle entry point |
| `reconstruct_path(goal) -> list[State]` | Walk the inner BFS's parents back to start |

### Properties
| Property | Description |
|---|---|
| `solutions`, `counters`, `elapsed`, `elapsed_search`, `elapsed_update`, `phase`, `recorder`, `name`, `problem` | Inherited from `AlgoOMSPP` |
| `search_state` | The inner BFS's `SearchStateSPP` bundle (own property) |

### Counters

| counter | KBFS |
|---|:---:|
| `cnt_h_search` | 0 (no heuristic) |
| `cnt_h_update` | 0 (no heuristic) |
| `cnt_phi_search` | 0 (no Φ aggregation) |
| `cnt_phi_update` | 0 (no Φ aggregation) |
| `cnt_push` | ✓ (frontier-sourced) |
| `cnt_pop` | ✓ (frontier-sourced) |
| `cnt_pop_stale` | 0 (no lazy stale-pop) |
| `cnt_decrease` | 0 (FIFO's decrease is a no-op) |

Sourced from the inner `_MultiGoalBFS`'s `FrontierFIFO` via `_sync_frontier_counters()` at end-of-run.

### Within/between elapsed split

`elapsed_update == 0.0` by construction — the structural phase never flips to `PHASE_UPDATE`. There is no inter-sub-search work to time (single pass).

### Recording event schema

In addition to the standard `BFS` events (`push`, `pop`):

| event | when |
|---|---|
| `on_goal` | per goal-pop (during search) or per unreachable-goal at end. `reason ∈ {expanded, unreachable}`. The `'already_closed'` reason is unused — KBFS observes each goal exactly once at its pop, so the "noticed too late" branch doesn't exist. |

NO `update_heuristic` (no h), NO `update_frontier` (no per-goal sub-search restarts), NO `decrease_g` (FIFO no-op).

## Algorithm

```
goal_indices = {g → [input positions]}  # handles duplicate goals
remaining = set(goal_indices.keys())

inner = _MultiGoalBFS(
    problem=self.problem,
    remaining=remaining,
    on_goal_pop=callback,
)
inner._recorder = self._recorder
inner.run()

# unreachable goals (set non-empty when frontier exhausted)
for state in remaining:
    self._solutions[state] = SolutionSPP(cost=inf)
    emit on_goal(reason='unreachable')
```

The inner `_MultiGoalBFS`:
- Overrides `_is_goal` to always return False (KBFS controls termination).
- Overrides `_early_exit(state)`:
  - If `state in remaining`: invoke `on_goal_pop(state, g[state])`, remove from `remaining`. Return SolutionSPP if `remaining` is empty (terminate).
  - Else: return None (continue).

The orchestrator `on_goal_pop` callback records the solution and emits `on_goal` events (one per `goal_index` for duplicates).

## Discovery order

`on_goal` events fire in the order goals are popped from the FIFO — the genuine BFS-discovery order. Each event carries `goal_index` for the goal's position in `problem.goals`, preserving identifiability for duplicates and giving downstream tools both axes (event order = discovery, `goal_index` = input).

## Correctness preconditions

1. **Uniform edge weights** — BFS depth equals optimal cost only on unit-cost graphs. For non-uniform non-negative weights, use `KDijkstra`.
2. Inherits `ProblemSPP` correctness conditions otherwise.

## Factory

| Method | Description |
|---|---|
| `graph_abc_two_goals()` | A → B → C with goals=[B, C]; both expanded |
| `graph_abc_cached_at_b_first()` | A → B → C with goals=[C, B]; B is observed first (lower depth) |

## Tests

| File | Scope | Count |
|---|---|---|
| `_tester.py` | lifecycle (single-goal, two-goals, discovery-order semantics, no-transition recording schema, counter zeros (graph), elapsed_update zero, cross-algo equivalence vs. independent BFS, path reconstruction) | 8 |
| `_tester_counters.py` | full 8-counter dict pin on canonical OMSPP (14 push / 14 pop, six zeros); per-goal optimal costs pin (`(0,3)=7, (3,0)=3, (3,3)=6`) | 2 |
| `_tester_recording.py` | FULL event-stream pin on canonical OMSPP — 14 push / 14 pop with 3 INTERLEAVED `on_goal` events at discovery order. Subsumes event-type counts, pop sequence, and h/f schema invariants via the dict-list diff | 1 |

## Dependencies

- `f_hs.algo.i_1_omspp.i_0_base.AlgoOMSPP` — base class.
- `f_hs.algo.i_0_oospp.i_1_bfs.BFS` — inner sub-algo (subclassed as `_MultiGoalBFS`).
- `f_hs.algo.i_0_oospp.i_0_base._search_state.SearchStateSPP` — bundle (per inner instance).
- `f_hs.solution.SolutionOMSPP`, `f_hs.solution.SolutionSPP`.
