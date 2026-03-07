# AStarIncrementalBackward

## with_bounds Explained

Controls what heuristic info is accumulated after each sub-search for
use in future sub-searches.

After each backward sub-search (from goal Gi toward start S):
- **Cached** (`dict_cached`): exact distances to goal for path states.
  Computed via `distances_to_goal()` as `g_goal - g[state]` for states
  on the optimal path. Always collected.
- **Bounded** (`dict_bounded`): lower bounds on distance to goal.
  Computed via `bounds_to_goal()`. Only collected when
  `with_bounds=True`.

### Why Path States Are Exact (Cached)

If state X is on the optimal path, then:
```
g[X] + dist(X, goal) = g_goal
```
So `dist(X, goal) = g_goal - g[X]` is exact.

### Why Explored Non-Path States Are Lower Bounds (Bounded)

A* guarantees `g[X]` is optimal from start. But X may not be on any
shortest path to goal — reaching goal through X may cost more than
`g_goal`. By the triangle inequality:
```
g_goal <= g[X] + dist(X, goal)
```
So `dist(X, goal) >= g_goal - g[X]` — only a lower bound.

**Example** (6x6 grid with wall at column 4, backward from (0,1) to
(0,5), g_goal=12):

| State | g | bound (12-g) | true dist | exact? |
|-------|---|-------------|-----------|--------|
| (2,3) | 4 | 8 (cached) | 8 | yes — on path |
| (2,2) | 3 | 9 | 9 | yes — on alt shortest path |
| (2,0) | 3 | 9 | 11 | no — off route |

State (2,0) is reachable from start in 3 steps, but going through it
to the goal costs 3 + 11 = 14 > 12. The bound (9) underestimates the
true remaining distance (11).

### with_bounds=False

**Cached**: path states with exact distances.
**Bounded**: nothing (`bounds_to_goal` not called).

Future sub-searches use exact h for path states, Manhattan for
everything else.

### with_bounds=True

**Cached**: path states with exact distances.
**Bounded**: all explored non-path states with `g_goal - g[state]`.

### Why No BFS Propagation

BFS propagation from explored states to unexplored neighbors (the old
`depth > 0` modes) was mathematically proved to never beat Manhattan
heuristic on unit-cost graphs with consistent heuristics. Each
propagated bound decays by 1 per hop, making it equal to or worse than
Manhattan distance. Therefore, the `depth_propagation` parameter was
simplified to a boolean `with_bounds`.

### Summary

| with_bounds | dict_cached (exact) | dict_bounded (lower bounds) |
|-------------|---------------------|-----------------------------|
| False       | path states         | —                           |
| True        | path states         | all explored non-path states|
