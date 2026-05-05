# KDijkstra — k-Dijkstra for OMSPP

## Purpose

Solves OMSPP via a **single inner Dijkstra pass** that observes each goal at the moment it is popped (in g-order, optimal under non-negative edge weights). Sibling of `KAStarInc` / `KAStarAgg` / `KBFS` under `AlgoOMSPP` — independent frame, NOT a KAStarInc subclass.

The Dijkstra expansion order from a single source is goal-independent under h≡0 (priority `(g, -g, state)` doesn't depend on any goal), so a per-goal sub-search restart with shared state would do the same work as a single pass that observes goal-pops as they occur. KDijkstra implements the simpler model: one inner Dijkstra, multi-goal early-exit hook.

## Public API

### Constructor
```python
KDijkstra(problem: ProblemSPP[State],
          name: str = 'KDijkstra',
          is_recording: bool = False,
          is_timing: bool = True)
```
No `h` kwarg — Dijkstra hardcodes h≡0. The `AlgoOMSPP` base requires `h`, so a dummy `lambda s, g: 0` is passed internally and never invoked.

### Inheritance
```
AlgoOMSPP[State]
    └── KDijkstra[State]

# inner (private):
AlgoSPP[State]
    └── AStar[State]
            └── Dijkstra[State]
                    └── _MultiGoalDijkstra[State]
```

### Methods
| Method | Description |
|---|---|
| `run() -> SolutionOMSPP` | Algo lifecycle entry point |
| `reconstruct_path(goal) -> list[State]` | Walk the inner Dijkstra's parents back to start |

### Properties
| Property | Description |
|---|---|
| `solutions`, `counters`, `elapsed`, `elapsed_search`, `elapsed_update`, `phase`, `recorder`, `name`, `problem` | Inherited from `AlgoOMSPP` |
| `search_state` | The inner Dijkstra's `SearchStateSPP` bundle (own property) |

### Counters

KDijkstra uses the base `AlgoOMSPP` scaffold unchanged — no
heuristic, no Φ, no lazy stale-pop, so no counters for those
mechanisms appear on `algo.counters`.

| counter | KDijkstra |
|---|:---:|
| `cnt_push` | ✓ (frontier-sourced) |
| `cnt_pop` | ✓ (frontier-sourced) |
| `cnt_decrease` | ✓ (frontier-sourced) |
| `mem_open` / `mem_closed` | ✓ (post-run snapshot) |

Mechanism-irrelevant counters (`cnt_h_*`, `cnt_phi_*`,
`cnt_pop_stale`) are **absent** from KDijkstra's scaffold by
design.

Sourced from the inner `_MultiGoalDijkstra`'s `FrontierPriority` via `_sync_frontier_counters()` at end-of-run.

### Within/between elapsed split

`elapsed_update == 0.0` by construction — phase never flips. No inter-sub-search work to time (single pass).

### Recording event schema

In addition to the standard `Dijkstra` events (`push`, `pop`, `decrease_g`; `Dijkstra._enrich_event` drops h and f so events schema-match BFS):

| event | when |
|---|---|
| `on_goal` | per goal-pop (during search) or per unreachable-goal at end. `reason ∈ {expanded, unreachable}`. The `'already_closed'` reason is unused. |

NO `update_heuristic` (h is constant), NO `update_frontier` (no per-goal sub-search restarts).

## Algorithm

Identical shape to `KBFS` — only the inner sub-algo class differs:

```
goal_indices = {g → [input positions]}
remaining = set(goal_indices.keys())

inner = _MultiGoalDijkstra(
    problem=self.problem,
    remaining=remaining,
    on_goal_pop=callback,
)
inner._recorder = self._recorder
inner.run()

# unreachable goals
for state in remaining:
    self._solutions[state] = SolutionSPP(cost=inf)
    emit on_goal(reason='unreachable')
```

The inner `_MultiGoalDijkstra`:
- Overrides `_is_goal` to always return False (KDijkstra controls termination).
- Overrides `_early_exit(state)`:
  - If `state in remaining`: invoke `on_goal_pop(state, g[state])`, remove from `remaining`. Return SolutionSPP if `remaining` is empty (terminate).
  - Else: return None (continue).

## Discovery order

`on_goal` events fire in g-order — the genuine order in which Dijkstra reaches each goal. Each carries `goal_index` for input position.

## Correctness preconditions

1. **Non-negative edge weights** required (Dijkstra-family).

## Factory

| Method | Description |
|---|---|
| `graph_abc_two_goals()` | A → B → C with goals=[B, C]; both expanded |
| `graph_abc_cached_at_b_first()` | A → B → C with goals=[C, B]; B is observed first (lower g) |

## Tests

| File | Scope | Count |
|---|---|---|
| `_tester.py` | lifecycle (single-goal, two-goals, discovery-order semantics, no-transition recording schema, inner sub-algo class), counter zeros (graph), elapsed_update zero, cross-algo equivalence (vs. independent Dijkstras, vs. KAStarInc with h ≡ 0) | 9 |
| `_tester_counters.py` | full 8-counter dict pin on canonical OMSPP (14 push / 14 pop, six zeros); per-goal optimal costs pin (`(0,3)=7, (3,0)=3, (3,3)=6`) | 2 |
| `_tester_recording.py` | FULL event-stream pin on canonical OMSPP — 14 push / 14 pop with 3 INTERLEAVED `on_goal` events at discovery order. Identical sequence to KBFS on uniform-cost grid; pinned independently so a future divergence in either algo's tiebreak surfaces in both testers | 1 |

## Dependencies

- `f_hs.algo.i_1_omspp.i_0_base.AlgoOMSPP` — base class.
- `f_hs.algo.i_0_oospp.i_2_dijkstra.Dijkstra` — inner sub-algo (subclassed as `_MultiGoalDijkstra`).
- `f_hs.algo.i_0_oospp.i_0_base._search_state.SearchStateSPP` — bundle (per inner instance).
- `f_hs.solution.SolutionOMSPP`, `f_hs.solution.SolutionSPP`.
