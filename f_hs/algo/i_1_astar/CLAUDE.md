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
    g = self._search.g[state]
    return (g + self._h(state), -g, state)
```
Three-level priority, compared lexicographically by the min-heap:
- **f = g + h** (primary): total estimated cost.
- **-g** (secondary): prefer deeper nodes (closer to goal).
- **state** (tertiary): fall back to State's `Comparable` ordering
  (via `HasKey`). Makes expansion order deterministic and
  independent of heap-internal ordering — required for
  full-sequence recording tests where `(f, -g)` ties are common
  (tight admissible heuristics produce many equal-f states).

## Event Enrichment
AStar overrides `_enrich_event` to add `h` and `f` to all
push, pop, and decrease_g events. The `f` value stored on events
equals `event['g'] + h(state)`, not the priority tuple.

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
| `grid_4x4_obstacle()` | `AStar` | 4x4 grid with vertical wall, cost 7 |
| `graph_decrease()` | `AStar` | Weighted graph (S→A/B→X, w(B,X)=0), h=0 — forces `decrease_g` and exercises h/f enrichment on it |

## Inheritance
```
AlgoSPP[State]
    └── AStar[State]
        └── Dijkstra[State]
```

## Tests
Split into three files by concern (mirrors the BFS split).
No `@pytest.fixture` — each test calls `AStar.Factory.*`
directly, per the Factory-over-fixture rule.

| File | Scope | Count |
|------|-------|-------|
| `_tester.py` | Graph problems + lifecycle (incl. `search_state` + `resume`) | 7 |
| `_tester_grid.py` | Grid problems | 4 |
| `_tester_recording.py` | Full event-sequence assertion (incl. `decrease_g` + h/f enrichment on it) | 6 |

Run all three explicitly:
```
pytest f_hs/algo/i_1_astar/_tester.py \
       f_hs/algo/i_1_astar/_tester_grid.py \
       f_hs/algo/i_1_astar/_tester_recording.py
```

The recording tester covers `graph_abc`, `graph_diamond`
(tie-break via State Comparable), `grid_3x3`, `grid_3x3_obstacle`,
and `grid_4x4_obstacle` (same problem used by BFS, exercising
an admissible-but-loose Manhattan heuristic over a wall).

## Dependencies
- `f_hs.algo.i_0_base.AlgoSPP`
- `f_hs.frontier.i_1_priority.FrontierPriority`
