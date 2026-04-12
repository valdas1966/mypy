# AStar

## Purpose
A* Search Algorithm using QueueIndexed (indexed min-heap with
decrease_key). Matches classical textbook pseudocode — no lazy
deletion, each state appears at most once in OPEN.

## Public API

### Constructor
```python
def __init__(self,
             problem: ProblemSPP[State],
             h: Callable[[State], float],
             name: str = 'AStar',
             is_recording: bool = False) -> None
```

## Tie-Breaking
Priority is `(f, -g)`:
- **f = g + h**: total estimated cost
- **-g**: prefer deeper nodes (closer to goal)

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
- `f_ds.queues.i_1_indexed.QueueIndexed`
