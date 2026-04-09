# AlgoSPP

## Purpose
Abstract base class for SPP search algorithms. Implements the
common search loop with event recording. Subclasses provide
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

## Event Recording
When `is_recording=True`, the recorder captures these events:

| Event | Details | Elapsed |
|-------|---------|---------|
| `push` | state, g, parent | since run start |
| `pop` | state, g, skipped | since run start |
| `generate` | parent, child, edge_cost, new_g, old_g, relaxed | since run start |
| `goal_found` | state, cost | since run start |
| `reconstruct_path` | goal, path_length | own duration |

Events are dicts stored via `Recorder`. No-op when inactive.

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
| `_edge_cost(p, c)` | No (default=1) | Edge weight |
| `_is_goal(state)` | No | Goal check |
| `_init_search()` | No | Override to clear frontier |

## Dependencies
- `f_cs.algo.Algo`
- `f_hs.problem.ProblemSPP`
- `f_hs.solution.SolutionSPP`
- `f_hs.state.StateBase`
