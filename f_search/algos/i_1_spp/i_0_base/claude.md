# AlgoSPP - Base for One-to-One Shortest Path Problem Algorithms

## Purpose
Abstract base class for algorithms solving One-to-One Shortest Path Problems (SPP). Specializes `AlgoBestFirst` with `ProblemSPP` and `SolutionSPP` types, and implements the core `_run()` loop with goal-cost extraction via `g_goal`.

## Public API

### Constructor
```python
def __init__(self,
             problem: ProblemSPP,
             data: Data,
             name: str = 'AlgoSPP') -> None:
```
Initializes with an SPP problem, a best-first data structure, and an optional name.

### `_run(self) -> SolutionSPP`
Runs the best-first search loop:
1. Discovers the start state if the frontier is empty.
2. Loops: selects best, checks termination, explores best.
3. On valid termination, extracts `g_goal = self._data.dict_g[self.problem.goal]`.
4. If `_need_path` is set, reconstructs the path via `self._data.path_to(state=goal)`.
5. Returns `SolutionSPP` with `name_algo`, `problem`, `is_valid`, `path`, `g_goal`, and `stats`.

### `_can_terminate(self) -> bool`
Returns `True` when the current best state equals the problem's goal.

## Inheritance (Hierarchy)

```
Algo
  └── AlgoSearch
        └── AlgoBestFirst[Problem, Solution, State, Data]
              └── AlgoSPP[State, Data]
```

| Base | Responsibility |
|------|----------------|
| `Algo` | Generic algorithm lifecycle (`run`, `_pre_run`, `_post_run`) |
| `AlgoSearch` | Search-specific base (`_need_path`, `cls_stats`) |
| `AlgoBestFirst` | Best-first infrastructure (`_data`, `_should_continue`, `_select_best`, `_explore_best`) |
| `AlgoSPP` | SPP-specific `_run()` loop, `_can_terminate()`, constructs `SolutionSPP` with `g_goal` |

## Dependencies

| Import | Purpose |
|--------|---------|
| `f_search.algos.i_0_base.AlgoBestFirst` | Parent class providing best-first search infrastructure |
| `f_search.ds.state.StateBase` | Bound for the `State` type variable |
| `f_search.ds.data.DataBestFirst` | Bound for the `Data` type variable; holds `dict_g`, `frontier`, `path_to()` |
| `f_search.problems.ProblemSPP` | Problem type with `start`, `goal` properties |
| `f_search.solutions.SolutionSPP` | Solution type accepting `path`, `g_goal`, `stats` |

## Usage Example

```python
from f_search.algos.i_1_spp.i_1_astar import AStar
from f_search.problems import ProblemSPP

# Create a problem
problem = ProblemSPP.Factory.without_obstacles()

# Run an SPP algorithm (AStar extends AlgoSPP)
astar = AStar(problem=problem)
solution = astar.run()

# Access results
if solution.is_valid:
    print(solution.g_goal)   # Optimal cost to reach goal
    print(solution.path)     # Path from start to goal
```
