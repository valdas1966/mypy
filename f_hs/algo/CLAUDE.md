# f_hs/algo — Search Algorithms

## Purpose
Search algorithms for Shortest-Path-Problem. Built on top of
AlgoSPP base class which provides the common search loop.

## Architecture
```
AlgoSPP (abstract: loop + data + path reconstruction)
├── BFS (FIFO deque frontier)
└── AStar (heapq priority frontier, f = g + h)
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

## Common Search Loop (in AlgoSPP)
```
1. Init: g(start)=0, push start to frontier
2. While frontier not empty:
   a. Pop best state
   b. Skip if closed (lazy deletion)
   c. If goal → return SolutionSPP(cost)
   d. Close state
   e. For each successor: relax and push if improved
3. Return SolutionSPP(cost=inf)
```

## Subclass Differences
| | BFS | A* | Dijkstra |
|--|-----|-----|----------|
| Frontier | deque (FIFO) | heapq (by f) | heapq (by g) |
| Priority | insertion order | g + h | g |
| Heuristic | none | provided | h=0 |
