# Dijkstra

## Purpose
Dijkstra's Algorithm. A* with h=0 (no heuristic).
Optimal for non-negative edge costs.

## Public API

### Constructor
```python
def __init__(self,
             problem: ProblemSPP[State],
             name: str = 'Dijkstra',
             is_recording: bool = False) -> None
```

## Factory
| Method | Returns | Description |
|--------|---------|-------------|
| `graph_abc()` | `Dijkstra` | Linear A -> B -> C |
| `graph_no_path()` | `Dijkstra` | No path to goal |
| `graph_start_is_goal()` | `Dijkstra` | Start == Goal |
| `graph_diamond()` | `Dijkstra` | Diamond graph |

## Inheritance
```
AlgoSPP[State]
    └── AStar[State]
        └── Dijkstra[State]
```

## Dependencies
- `f_hs.algo.i_1_astar.AStar`
