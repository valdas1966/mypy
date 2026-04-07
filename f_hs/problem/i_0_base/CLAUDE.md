# ProblemSPP

## Purpose
Shortest-Path-Problem covering all four variants (OO, OM, MO, MM)
via `starts` and `goals` lists. Domain subclasses implement
`successors()` for their specific search space.

## Public API

### Constructor
```python
def __init__(self, starts: list[State], goals: list[State],
             name: str = 'ProblemSPP') -> None
```

### Properties
| Property | Type | Description |
|----------|------|-------------|
| `starts` | `list[State]` | All start states |
| `goals` | `list[State]` | All goal states |
| `start` | `State` | First start (convenience) |
| `goal` | `State` | First goal (convenience) |

### Abstract Methods
| Method | Description |
|--------|-------------|
| `successors(state)` | Domain-specific neighbors |

## Factory
Uses `_ProblemGraph` — concrete subclass with dict adjacency.
| Method | Description |
|--------|-------------|
| `graph_abc()` | A -> B -> C (cost 2) |
| `graph_no_path()` | A -> B, C isolated |
| `graph_start_is_goal()` | Start == Goal |
| `graph_diamond()` | A -> B -> D, A -> C -> D |

## Dependencies
- `f_cs.problem.ProblemAlgo`
- `f_hs.state.i_0_base.StateBase`
