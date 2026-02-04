# SolutionAlgo Module

## Overview

**Location:** `f_cs/solution/main.py`

**Purpose:** Abstract base class representing the solution output of an algorithm, including the problem reference, validity status, and execution statistics.

| Aspect | Details |
|--------|---------|
| Class | `SolutionAlgo` |
| Package | `f_cs.solution` |
| Export | `from f_cs.solution import SolutionAlgo` |
| Inherits | `Validatable`, `Generic[Problem, Stats]` |

## Architecture

```
┌─────────────────────────────────────┐
│          Validatable                │
│       (f_core.mixins)               │
└───────────────┬─────────────────────┘
                │
                ▼
┌─────────────────────────────────────┐
│   SolutionAlgo[Problem, Stats]      │
├─────────────────────────────────────┤
│  _problem: Problem                  │
│  _stats: Stats                      │
│  _is_valid: bool (inherited)        │
├─────────────────────────────────────┤
│  + problem (property)               │
│  + stats (property)                 │
│  + is_valid (inherited)             │
└─────────────────────────────────────┘
         │               │
         │ uses          │ uses
         ▼               ▼
┌─────────────────┐ ┌─────────────────┐
│   ProblemAlgo   │ │    StatsAlgo    │
│  (f_cs.problem) │ │   (f_cs.stats)  │
└─────────────────┘ └─────────────────┘
```

## Components

### SolutionAlgo

Generic base class for algorithm solutions, parameterized by problem and stats types.

**Type Parameters:**
- `Problem` - bounded by `ProblemAlgo`
- `Stats` - bounded by `StatsAlgo`

**Constructor:**
```python
def __init__(self,
             problem: Problem,
             is_valid: bool,
             stats: Stats) -> None
```

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `problem` | `Problem` | The problem this solution solves |
| `stats` | `Stats` | Algorithm execution statistics |
| `is_valid` | `bool` | Whether solution is valid (inherited); `bool(solution)` works |

## Usage Examples

```python
from f_cs.solution import SolutionAlgo
from f_cs.problem import ProblemAlgo
from f_cs.stats import StatsAlgo

# Create problem and stats
problem = ProblemAlgo(name='MyProblem')
stats = StatsAlgo(elapsed=10)

# Create solution
solution = SolutionAlgo(problem=problem, is_valid=True, stats=stats)

# Access properties
print(solution.problem.name)  # 'MyProblem'
print(solution.stats.elapsed) # 10

# Check validity - bool(solution) is enough
if solution:
    print('Valid solution')
```

## Inheritance Hierarchy

```
Validatable (f_core.mixins)
    │
    └── SolutionAlgo[Problem, Stats]
            │
            └── (concrete solution implementations)
```

## Design Patterns

| Pattern | Usage |
|---------|-------|
| Generic Class | Parameterized by Problem and Stats types |
| Composition | Contains ProblemAlgo and StatsAlgo instances |

## Dependencies

| Dependency | Purpose |
|------------|---------|
| `f_core.mixins.validatable.Validatable` | Provides is_valid property |
| `f_cs.problem.main.ProblemAlgo` | Problem type bound |
| `f_cs.stats.main.StatsAlgo` | Stats type bound |
| `typing.Generic`, `TypeVar` | Generic type support |
