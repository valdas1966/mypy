# AStarCached - A* with Cached/Bounded Heuristic Tiebreaking

## Purpose
Extends `AStarReusable` to prioritize states with cached (exact) heuristic values over bounded (lower-bound) and unbounded (Manhattan) heuristics. Uses `PriorityGHFlags` for flag-aware frontier ordering and early termination when a state with a cached heuristic is selected as best.

## Public API

### `__init__(self, problem: Problem, heuristics: HeuristicsProtocol[State] = None, data_heuristics: DataHeuristics[State] = None, data_cached: DataCached[State] = None, need_path: bool = False, name: str = 'AStarCached') -> None`
Initialize AStarCached with an SPP problem and optional cached/bounded data.

### `reached_goal -> bool` (property)
Return `True` if the search terminated by reaching the goal (not by cached early termination).

### `distances_to_goal(self) -> dict[State, int]`
Return exact distances to the goal for all states on the optimal path. Computed as `g(goal) - g(state)`.

### `bounds_to_goal(self) -> dict[State, int]`
Return lower bounds on distance to the goal for explored states not on the optimal path.

### `list_explored(self) -> list[dict[str, any]]`
Return a list of dicts for each explored state containing: `row`, `col`, `f`, `is_cached`, `is_bounded`, `g`, `h`.

### `run(self) -> SolutionSPP` (inherited, calls `_run`)
Execute the algorithm and return the solution.

### `_run(self) -> SolutionSPP` (override)
Run the search loop. Terminates when the best state is the goal or has a cached (exact) heuristic. On valid termination, computes `g_goal`: if `best == goal`, uses `dict_g[best]`; if terminated via cached heuristic (`best != goal`), computes `g_goal = dict_g[best] + dict_cached[best]`. Optionally reconstructs the path through cached parent chain. Returns `SolutionSPP` with validity, path, `g_goal`, and stats.

## Inheritance (Hierarchy)

```
AlgoSearch
  └─ AlgoSPP
       └─ AStar
            └─ AStarReusable
                 └─ AStarCached
```

| Base | Responsibility |
|------|----------------|
| `AlgoSearch` | Core data structures, lifecycle hooks, stats tracking |
| `AlgoSPP` | SPP-specific solution creation, stats specialization |
| `AStar` | A* loop: discover, explore, relax, Manhattan heuristic |
| `AStarReusable` | Allows external data/heuristics injection for chaining |
| `AStarCached` | Flag-aware priority (cached > bounded > unbounded), early termination on cached hit, g_goal computation |

## Dependencies

| Import | Purpose |
|--------|---------|
| `AStarReusable` | Parent class providing reusable A* infrastructure |
| `ProblemSPP` | One-to-one shortest path problem definition |
| `SolutionSPP` | Solution container with path, g_goal, and stats |
| `HeuristicsProtocol` | Protocol for heuristic callables |
| `DataHeuristics` | Core search data (frontier, g/h dicts, parent) |
| `DataCached` | Cached/bounded heuristic dictionaries and parent chain |
| `Path` | Ordered sequence of states forming a path |
| `PriorityGHFlags` | Priority with `is_cached`/`is_bounded` flags for tiebreaking |

## Usage Examples

### Without cache (behaves like standard A*)
```python
from f_search.algos.i_1_spp.i_3_astar_cached import AStarCached
from f_search.problems import ProblemSPP

problem = ProblemSPP.Factory.for_cached()
algo = AStarCached(problem=problem)
sol = algo.run()
# sol.stats.explored == 22
```

### With cached exact distances
```python
from f_search.algos.i_1_spp.i_3_astar_cached import AStarCached
from f_search.problems import ProblemSPP
from f_search.ds.data.cached import DataCached

problem = ProblemSPP.Factory.for_cached()
data_cached = DataCached.Factory.six_cached()
algo = AStarCached(problem=problem, data_cached=data_cached)
sol = algo.run()
# sol.stats.explored == 10  (fewer states explored)
# sol.g_goal contains the computed goal distance
```

### With bounded heuristics (even fewer explorations)
```python
problem = ProblemSPP.Factory.for_cached()
data_cached = DataCached.Factory.six_bounded()
algo = AStarCached(problem=problem, data_cached=data_cached)
sol = algo.run()
# sol.stats.explored == 8
```

## Tests (`_tester.py`)

| Test | Description |
|------|-------------|
| `test_without_cache` | Explored count without cache (22) |
| `test_with_cache` | Explored count with cached heuristics (10) |
| `test_with_bounded` | Explored count with bounded heuristics (8) |
| `test_with_bounded_depth_1` | Explored count with depth-1 bounds (5) |
| `test_with_bounded_depth_2` | Explored count with depth-2 bounds (4) |
| `test_g_goal_without_cache` | `g_goal == 13` when goal reached directly |
| `test_g_goal_with_cache` | `g_goal == 13` via cached early termination |
| `test_g_goal_with_bounded` | `g_goal == 13` via bounded early termination |
| `test_quality_h` | `quality_h == 5/13` consistent across all cache variants |
