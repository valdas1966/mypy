# AlgoSPP

## Purpose
Abstract base class for SPP search algorithms. Implements the
classical search loop with eager deletion. Subclasses provide
frontier management.

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
OPEN ← {start}
while OPEN not empty:
    n ← OPEN.pop_min()
    if n is goal: return cost
    CLOSED ← CLOSED ∪ {n}
    for each child of n:
        if child in CLOSED: skip
        if child not in OPEN: insert
        else if new_g < g(child): decrease_key
```

## Event Recording
When `is_recording=True`, the recorder captures:

| Event | Details | Elapsed |
|-------|---------|---------|
| `push` | state, g, parent | nanoseconds |
| `pop` | state, g | nanoseconds |
| `generate` | parent, child, edge_cost, new_g, old_g, relaxed | nanoseconds |
| `decrease_key` | state, g, parent | nanoseconds |
| `goal_found` | state, cost | nanoseconds |
| `reconstruct_path` | goal, path_length | nanoseconds |

## Internal Data
| Attribute | Type | Description |
|-----------|------|-------------|
| `_g` | `dict[State, float]` | g-values |
| `_parent` | `dict[State, State\|None]` | Best predecessors |
| `_closed` | `set[State]` | Expanded states |
| `_goal_reached` | `State\|None` | Goal found |
| `_goals_set` | `set[State]` | Goal set for lookup |

## Hooks for Subclasses
| Hook | Must Override | Description |
|------|---------------|-------------|
| `_push(state)` | Yes | Add to frontier |
| `_pop()` | Yes | Get next from frontier |
| `_has_open()` | Yes | Frontier not empty? |
| `_in_open(state)` | No (default=False) | State in frontier? |
| `_decrease_key(state)` | No (default=no-op) | Update priority |
| `_edge_cost(p, c)` | No (default=1) | Edge weight |
| `_is_goal(state)` | No | Goal check |
| `_init_search()` | No | Override to clear frontier |

## Dependencies
- `f_cs.algo.Algo`
- `f_hs.problem.ProblemSPP`
- `f_hs.solution.SolutionSPP`
- `f_hs.state.StateBase`
