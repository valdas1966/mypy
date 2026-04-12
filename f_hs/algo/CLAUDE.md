# f_hs/algo — Search Algorithms

## Purpose
Search algorithms for Shortest-Path-Problem. Built on top of
AlgoSPP base class which provides the classical search loop
with eager deletion.

## Architecture
```
AlgoSPP (abstract: loop + data + path reconstruction)
├── BFS (FIFO deque frontier)
└── AStar (QueueIndexed, f = g + h)
    └── Dijkstra (h = 0)
```

## Module Structure
```
algo/
├── __init__.py          AlgoSPP, BFS, AStar, Dijkstra
├── i_0_base/            AlgoSPP — abstract base with search loop
├── i_1_bfs/             BFS — breadth-first search
├── i_1_astar/           AStar — A* with heuristic
└── i_2_dijkstra/        Dijkstra — A* with h=0
```

## Classical Search Loop (in AlgoSPP)
```
OPEN ← {start}
while OPEN not empty:
    n ← OPEN.pop_min()
    if n is goal: return cost
    CLOSED ← CLOSED ∪ {n}
    for each child of n:
        if child in CLOSED: skip
        if child not in OPEN: insert
        else if new_g < g(child): decrease_key
```

## Subclass Differences
| | BFS | A* | Dijkstra |
|--|-----|-----|----------|
| Frontier | deque (FIFO) | QueueIndexed (by f) | QueueIndexed (by g) |
| Priority | insertion order | f = g + h | f = g |
| Heuristic | none | provided | h=0 |
| decrease_key | not needed | via QueueIndexed | via QueueIndexed |
