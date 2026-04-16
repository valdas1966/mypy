# AStar

## Purpose
A* Search Algorithm using `FrontierPriority` (backed by
`QueueIndexed` — indexed min-heap with decrease_key). Matches
classical textbook pseudocode — eager deletion, each state
appears at most once in FRONTIER.

## Public API

### Constructor
```python
def __init__(self,
             problem: ProblemSPP[State],
             h: Callable[[State], float],
             name: str = 'AStar',
             is_recording: bool = False) -> None
```
Injects `FrontierPriority[State]()` into `AlgoSPP` and stores `h`.

## Priority / Tie-Breaking
```python
def _priority(self, state: State) -> tuple:
    g = self._g[state]
    return (g + self._h(state), -g)
```
- **f = g + h**: total estimated cost
- **-g**: prefer deeper nodes (closer to goal)

## Event Enrichment
AStar overrides `_enrich_event` to add `h` and `f` to all
push, pop, and decrease_g events.

## Factory
| Method | Returns | Description |
|--------|---------|-------------|
| `graph_abc()` | `AStar` | Linear graph, admissible h |
| `graph_no_path()` | `AStar` | No path, h=0 |
| `graph_start_is_goal()` | `AStar` | Start == Goal, h=0 |
| `graph_diamond()` | `AStar` | Diamond graph, admissible h |
| `grid_3x3()` | `AStar` | Open grid, Manhattan h |
| `grid_3x3_obstacle()` | `AStar` | Grid with obstacle |
| `grid_3x3_no_path()` | `AStar` | Grid with wall |
| `grid_3x3_start_is_goal()` | `AStar` | Grid where start == goal |

## Inheritance
```
AlgoSPP[State]
    └── AStar[State]
        └── Dijkstra[State]
```

## Dependencies
- `f_hs.algo.i_0_base.AlgoSPP`
- `f_hs.frontier.i_1_priority.FrontierPriority`
