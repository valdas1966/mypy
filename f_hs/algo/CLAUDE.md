# f_hs/algo — Search Algorithms

## Purpose
Search algorithms for Shortest-Path-Problem. Built on top of
AlgoSPP base class which provides the classical search loop
with eager deletion and automatic event recording.

## Architecture
```
AlgoSPP (abstract: loop + data + recording + path)
├── BFS (FIFO deque frontier)
└── AStar (QueueIndexed, f = g + h)
    └── Dijkstra (h = 0)
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
while FRONTIER not empty:
    n ← FRONTIER.pop_min()
    if n is goal: return cost
    CLOSED ← CLOSED ∪ {n}
    for each child of n:
        if child in CLOSED: skip
        w ← problem.w(n, child)
        if child not in FRONTIER: insert
        else if new_g < g(child): decrease_g
```

## Subclass Differences
| | BFS | A* | Dijkstra |
|--|-----|-----|----------|
| Frontier | deque (FIFO) | QueueIndexed (by f) | QueueIndexed (by g) |
| Priority | insertion order | f = g + h | f = g |
| Heuristic | none | provided | h=0 |
| decrease_g | not needed | via QueueIndexed | via QueueIndexed |

## Edge Costs
`problem.w(parent, child)` returns the edge cost. Default 1.0.
Subclasses of ProblemSPP override for weighted graphs.
