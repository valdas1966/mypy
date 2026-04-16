# f_hs/algo — Search Algorithms

## Purpose
Search algorithms for Shortest-Path-Problem. Built on top of
`AlgoSPP`, which owns the classical search loop and composes a
`FrontierBase` via constructor injection. Subclasses pick a
frontier (`FrontierFIFO` for BFS, `FrontierPriority` for A*) and
override `_priority(state)` if needed.

## Architecture
```
AlgoSPP (loop + data + recording + path + Frontier)
├── BFS                                      — FrontierFIFO
└── AStar (_priority → (f, -g))              — FrontierPriority
    └── Dijkstra (h = 0)                     — inherits AStar
```

## Module Structure
```
algo/
├── __init__.py          AlgoSPP, BFS, AStar, Dijkstra
├── i_0_base/            AlgoSPP — abstract base
├── i_1_bfs/             BFS — breadth-first search
├── i_1_astar/           AStar — A* with heuristic
└── i_2_dijkstra/        Dijkstra — A* with h=0
```

## Classical Search Loop (in AlgoSPP)
```
FRONTIER ← {start}
while FRONTIER:
    n ← FRONTIER.pop_min()
    if n is goal: return cost
    CLOSED ← CLOSED ∪ {n}
    for each child of n:
        if child in CLOSED: skip
        w ← problem.w(n, child)
        if child not in FRONTIER: insert
        else if new_g < g(child): decrease
```

## Subclass Differences
| | BFS | A* | Dijkstra |
|--|-----|-----|----------|
| Frontier | FrontierFIFO | FrontierPriority | FrontierPriority |
| `_priority(state)` | None (default) | `(g+h, -g)` | `(g, 0)` |
| Heuristic | none | provided | h=0 |

## Edge Costs
`problem.w(parent, child)` returns the edge cost. Default 1.0.
Subclasses of `ProblemSPP` override for weighted graphs.
