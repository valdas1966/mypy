# BFS

## Purpose
Breadth-First Search. Optimal for unit-cost edges.
Uses FIFO deque as frontier.

## Public API

### Constructor
```python
def __init__(self,
             problem: ProblemSPP[State],
             name: str = 'BFS',
             is_recording: bool = False) -> None
```

## Factory
| Method | Returns | Description |
|--------|---------|-------------|
| `graph_abc()` | `BFS` | Linear A -> B -> C |
| `graph_no_path()` | `BFS` | No path to goal |
| `graph_start_is_goal()` | `BFS` | Start == Goal |
| `graph_diamond()` | `BFS` | Diamond graph |

## Inheritance
```
AlgoSPP[State]
    └── BFS[State]
```

## Dependencies
- `f_hs.algo.i_0_base.AlgoSPP`
