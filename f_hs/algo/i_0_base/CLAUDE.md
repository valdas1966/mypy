# AlgoSPP

## Purpose
Abstract base class for SPP search algorithms. Implements the
classical search loop with eager deletion. Recording is automatic
inside `_push`, `_pop`, and `_decrease_g`.

## Public API

### Constructor
```python
def __init__(self,
             problem: ProblemSPP[State],
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
while FRONTIER not empty:
    n ← FRONTIER.pop_min()
    if n is goal: return cost
    CLOSED ← CLOSED ∪ {n}
    for each child of n:
        if child in CLOSED: skip
        w ← problem.w(n, child)
        if child not in FRONTIER: insert
        else if new_g < g(child): decrease_g
```

## Event Recording
Recording is automatic inside `_push`, `_pop`, `_decrease_g`.
Three event types, duration in nanoseconds:

| Event | Details |
|-------|---------|
| `push` | state, g, parent, w |
| `pop` | state, g |
| `decrease_g` | state, g, parent, w |

`g`, `parent`, `w` are auto-populated from internal state.
AStar enriches with `h` and `f`.

## Internal Data
| Attribute | Type | Description |
|-----------|------|-------------|
| `_g` | `dict[State, float]` | g-values |
| `_parent` | `dict[State, State\|None]` | Best predecessors |
| `_closed` | `set[State]` | Expanded states |
| `_goal_reached` | `State\|None` | Goal found |
| `_goals_set` | `set[State]` | Goal set for lookup |

## Frontier Hooks (subclass must implement)
| Hook | Must Override | Description |
|------|---------------|-------------|
| `_frontier_push(state)` | Yes | Add to frontier |
| `_frontier_pop()` | Yes | Get next from frontier |
| `_has_frontier()` | Yes | Frontier not empty? |
| `_in_frontier(state)` | No (default=False) | State in frontier? |
| `_frontier_decrease(state)` | No (default=no-op) | Update priority |
| `_is_goal(state)` | No | Goal check |
| `_init_search()` | No | Override to clear frontier |

## Dependencies
- `f_cs.algo.Algo`
- `f_hs.problem.ProblemSPP`
- `f_hs.solution.SolutionSPP`
- `f_hs.state.StateBase`
