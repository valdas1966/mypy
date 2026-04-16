# AlgoSPP

## Purpose
Abstract base class for SPP search algorithms. Implements the
classical search loop with eager deletion. Composes a
`FrontierBase` via constructor injection — subclasses inject
the appropriate frontier (FIFO for BFS, Priority for A*).
Recording is automatic inside `_push`, `_pop`, and `_decrease_g`.

## Public API

### Constructor
```python
def __init__(self,
             problem: ProblemSPP[State],
             frontier: FrontierBase[State],
             name: str = 'AlgoSPP',
             is_recording: bool = False) -> None
```

### Methods
| Method | Signature | Description |
|--------|-----------|-------------|
| `run()` | `-> SolutionSPP` | Run search, return solution |
| `reconstruct_path()` | `(goal?) -> list[State]` | Trace parents |

### Inherited from Algo / ProcessBase
| Property | Type | Description |
|----------|------|-------------|
| `problem` | `ProblemSPP` | The input problem |
| `elapsed` | `float` | Execution time (seconds) |
| `recorder` | `Recorder` | Event recorder |
| `_record_event` | method | Inherited from ProcessBase |
| `_enrich_event` | method | Override hook (AStar adds h/f) |

## Search Loop (Classical Pseudocode)
```
FRONTIER ← {start}
while FRONTIER:
    n ← FRONTIER.pop_min()
    if n is goal: return cost
    CLOSED ← CLOSED ∪ {n}
    for each child of n:
        if child in CLOSED: skip
        w ← problem.w(n, child)
        if child not in FRONTIER: insert
        else if new_g < g(child): decrease
```

## Event Recording
Recording is automatic inside `_push`, `_pop`, `_decrease_g`.
Three event types, duration in nanoseconds:

| Event | Fields |
|-------|--------|
| `push` | state, g, parent, duration |
| `pop` | state, g, duration |
| `decrease_g` | state, g, parent, duration |

`g` is recorded as **`int`** (cast from internal float).
Assumption: edge costs are integer-valued — holds for all
current problems (unit-cost BFS/A*/Dijkstra). Revisit when
introducing fractional-weighted edges.

`parent` carries the `State` object (or `None` for starts).
AStar enriches all three event types with `h` and `f = g + h`.

### Recording Principle (framework-wide)

Each event records:
1. **What is newly determined at this event** (the value(s)
   decided or changed right now).
2. **What makes the event self-describing for its primary
   consumer** (the "answer" the event exists to deliver).

Events **never** record:
- values that are constant since the last related event
  (structural / unchanged info), or
- values that are derivable from the event log.

This gives **variable schemas per event type** — a pop event
has no `parent` key, not a `parent=None` key. The distinction
matters:

- `'parent' in event` → "this kind of event describes
  parenthood; here's its value (or `None` for a start)."
- `'parent' not in event` → "parenthood is not applicable
  to this kind of event."

Collapsing both into a uniform-schema with `parent=None`
would conflate "no parent (start state)" with "not applicable
(pop)" — and silently admits schema drift (e.g., accidentally
setting `parent` on a pop).

### Concrete field map for SPP search

| Concern | push | decrease_g | pop | Reason |
|---------|:----:|:----------:|:---:|--------|
| `state` | ✓ | ✓ | ✓ | subject |
| `g` (answer) | ✓ | ✓ | ✓ | answer at each event |
| `parent` | ✓ | ✓ | ✗ | structural — constant since last push/decrease_g |
| `w` | ✗ | ✗ | ✗ | derivable as `g(child) − g(parent)` |
| `h`, `f` (AStar) | ✓ | ✓ | ✓ | enriched on all three |
| `duration` | ✓ | ✓ | ✓ | generic, via `ProcessBase` |

Why `g` stays on every event (not "constant since push"):
it's the *answer* the algorithm delivers. The canonical
expansion-order query
`[(e['state'], e['g']) for e in events if e['type']=='pop']`
works without replaying the push/decrease_g log — a strong
consumer-convenience argument that overrides strict minimalism
for this one field.

`g` is recorded as **`int`** (cast from internal float).
Assumption: edge costs are integer-valued — holds for all
current problems. Revisit when introducing fractional weights.
Internal `self._g` stays float so `float('inf')` remains
usable for unreachable states.

### Future-proofing

If event types multiply (OMSPP `goal_reached`, incremental A*
`reopen`, bidirectional `frontier_id`, LPA* `recompute`), each
new type adds its *own* fields without touching existing ones.
When the number of event types or fields grows uncomfortable,
`TypedDict` per event type is the natural next step — pinning
schemas at the type level with zero runtime cost.

## Internal Data
| Attribute | Type | Description |
|-----------|------|-------------|
| `_frontier` | `FrontierBase[State]` | Injected frontier |
| `_g` | `dict[State, float]` | g-values |
| `_parent` | `dict[State, State\|None]` | Best predecessors |
| `_closed` | `set[State]` | Expanded states |
| `_goal_reached` | `State\|None` | Goal found |
| `_goals_set` | `set[State]` | Goal set for lookup |

## Hooks for Subclasses
| Hook | Default | Purpose |
|------|---------|---------|
| `_priority(state)` | `None` | Priority for frontier push/decrease |
| `_enrich_event(event)` | no-op | Add fields to recorded events |
| `_is_goal(state)` | `state in _goals_set` | Goal check |

Previously (pre-2026-04-16) AlgoSPP also required `_frontier_push`,
`_frontier_pop`, `_has_frontier`, `_in_frontier`,
`_frontier_decrease`. These are gone — `self._frontier` handles
them directly via its narrow interface.

## Dependencies
- `f_cs.algo.Algo`
- `f_hs.problem.ProblemSPP`
- `f_hs.solution.SolutionSPP`
- `f_hs.state.StateBase`
- `f_hs.frontier.FrontierBase`
