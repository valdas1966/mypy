# SolutionSearch - Base Solution for Search Problems

## Purpose
Base solution class for all search algorithm results. Stores the algorithm name, problem reference, validity status, and performance statistics. The problem is stored as-is; pickle exclusion of heavy data (e.g., grid) is handled by the problem's own `__getstate__`.

## Public API

### `__init__(self, name_algo: str, problem: Problem, is_valid: bool, stats: Stats) -> None`
Delegates to `SolutionAlgo.__init__` with all four parameters.

### `name_algo` (property) -> `str`
Returns the algorithm's name (inherited from `SolutionAlgo`).

### `problem` (property) -> `Problem`
Returns the problem instance stored as-is (inherited from `SolutionAlgo`).

### `stats` (property) -> `Stats`
Returns the statistics object (inherited from `SolutionAlgo`).

### `is_valid` (property) -> `bool`
Returns whether the solution is valid (inherited from `Validatable` via `SolutionAlgo`).

## Inheritance (Hierarchy)

```
Validatable
  └── SolutionAlgo[Problem, Stats]
        └── SolutionSearch[Problem, Stats]
```

| Base | Responsibility |
|------|---------------|
| `Validatable` | `is_valid` property and `__bool__` support |
| `SolutionAlgo[Problem, Stats]` | `name_algo`, `problem`, `stats` storage and properties |
| `SolutionSearch[Problem, Stats]` | Binds type bounds to `ProblemSearch` and `StatsSearch` |

### Type Parameters
- `Problem` bounded to `ProblemSearch`
- `Stats` bounded to `StatsSearch`

## Dependencies

| Import | Used For |
|--------|----------|
| `f_cs.solution.SolutionAlgo` | Direct parent class |
| `f_search.problems.ProblemSearch` | Type bound for `Problem` |
| `f_search.stats.StatsSearch` | Type bound for `Stats` |
| `typing.Generic`, `TypeVar` | Generic type parameterization |

## Usage Example

```python
from f_search.solutions.i_0_base import SolutionSearch
from f_search.stats import StatsSearch

# Via Factory
valid = SolutionSearch.Factory.zero_valid()
invalid = SolutionSearch.Factory.zero_invalid()

# Check result
if valid.is_valid:
    print(f"Algo: {valid.name_algo}")
    print(f"Explored: {valid.stats.explored}")
```

### Key Design Note
`SolutionSearch.__init__` stores the problem as-is (no `to_light()` call). The problem's `__getstate__` method handles excluding heavy data (like the grid) during pickle serialization.
