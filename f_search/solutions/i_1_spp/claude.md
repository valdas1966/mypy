# SolutionSPP - Solution for One-to-One Shortest Path Problem

## Purpose
Encapsulates the result of solving a One-to-One Shortest Path Problem. Extends `SolutionSearch` with a solution path, optimal goal cost, and heuristic quality metric.

## Public API

### `__init__(self, name_algo: str, problem: Problem, is_valid: bool, path: Path = None, g_goal: int = None, stats: StatsSearch = None) -> None`
Initializes the solution. Delegates `name_algo`, `problem`, `is_valid`, and `stats` to `SolutionSearch`. Stores `path` and `g_goal` locally. Defaults `stats` to a fresh `StatsSearch()` if not provided.

### `name_algo` (property) -> `str`
Returns the algorithm's name (inherited from `SolutionAlgo`).

### `problem` (property) -> `Problem`
Returns the problem instance (inherited from `SolutionAlgo`).

### `is_valid` (property) -> `bool`
Returns whether the solution is valid (inherited from `Validatable`).

### `stats` (property) -> `StatsSearch`
Returns the performance statistics (inherited from `SolutionAlgo`).

### `path` (property) -> `Path`
Returns the solution path from start to goal.

### `g_goal` (property) -> `int | None`
Returns the optimal cost to reach the goal. `None` if not set.

### `quality_h` (property) -> `float | None`
Returns heuristic quality as `h(start) / g(goal)` in [0, 1]. Returns `None` if the solution is invalid or `g_goal` is 0 or `None`.

## Inheritance (Hierarchy)

```
Validatable
  └── SolutionAlgo[Problem, Stats]
        └── SolutionSearch[Problem, Stats]
              └── SolutionSPP
```

| Base | Responsibility |
|------|---------------|
| `Validatable` | `is_valid` property and `__bool__` support |
| `SolutionAlgo[Problem, Stats]` | `name_algo`, `problem`, `stats` storage and properties |
| `SolutionSearch[Problem, Stats]` | Binds type bounds to `ProblemSearch` and `StatsSearch` |
| `SolutionSPP` | Adds `path`, `g_goal`, and `quality_h` for SPP results |

### Type Parameters
- `Problem` bound to `ProblemSPP` (via import alias)
- `Stats` bound to `StatsSearch`

## Dependencies

| Import | Used For |
|--------|----------|
| `f_search.solutions.i_0_base.SolutionSearch` | Direct parent class |
| `f_search.problems.ProblemSPP` | Problem type (aliased as `Problem`) |
| `f_search.stats.StatsSearch` | Default statistics type |
| `f_search.ds.path.Path` | Solution path data structure |

## Usage Example

```python
from f_search.solutions.i_1_spp import SolutionSPP

# Via Factory
valid = SolutionSPP.Factory.valid()
invalid = SolutionSPP.Factory.invalid()

# Check result and access path
if valid.is_valid:
    print(f"Path: {valid.path}")
    print(f"Goal cost: {valid.g_goal}")
    print(f"Heuristic quality: {valid.quality_h}")
    print(f"Explored: {valid.stats.explored}")
```
