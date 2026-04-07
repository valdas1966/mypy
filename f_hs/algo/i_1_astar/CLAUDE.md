# AStar

## Purpose
A* Search Algorithm. Uses priority queue ordered by f = g + h.
Heuristic function provided as a callable parameter.

## Public API

### Constructor
```python
def __init__(self,
             problem: ProblemSPP[State],
             h: Callable[[State], float],
             name: str = 'AStar',
             is_recording: bool = False) -> None
```

## Factory
| Method | Returns | Description |
|--------|---------|-------------|
| `graph_abc()` | `AStar` | Linear graph, admissible h |
| `graph_no_path()` | `AStar` | No path, h=0 |
| `graph_start_is_goal()` | `AStar` | Start == Goal, h=0 |
| `graph_diamond()` | `AStar` | Diamond graph, admissible h |

## Inheritance
```
AlgoSPP[State]
    └── AStar[State]
        └── Dijkstra[State]
```

## Dependencies
- `f_hs.algo.i_0_base.AlgoSPP`
