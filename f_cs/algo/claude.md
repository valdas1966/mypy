# Algo Module

## Overview

**Location:** `f_cs/algo/main.py`

**Purpose:** Base class for algorithms in Computer Science, orchestrating problem input, solution output, and execution statistics.

| Aspect | Details |
|--------|---------|
| Class | `Algo` |
| Package | `f_cs.algo` |
| Export | `from f_cs.algo import Algo` |
| Inherits | `ProcessIO[Problem, Solution]`, `Generic[Problem, Solution]` |

## Architecture

```
┌─────────────────────────────────────┐
│     ProcessIO[Problem, Solution]    │
│         (f_core.processes)          │
└───────────────┬─────────────────────┘
                │
                ▼
┌─────────────────────────────────────┐
│    Algo[Problem, Solution]          │
├─────────────────────────────────────┤
│  _stats: StatsAlgo                  │
│  cls_stats: type[StatsAlgo]         │
├─────────────────────────────────────┤
│  + problem (property)               │
│  + _run_post()                      │
└─────────────────────────────────────┘
         │           │           │
         │ uses      │ uses      │ uses
         ▼           ▼           ▼
┌─────────────┐ ┌──────────────┐ ┌─────────────┐
│ ProblemAlgo │ │ SolutionAlgo │ │  StatsAlgo  │
└─────────────┘ └──────────────┘ └─────────────┘
```

## Components

### Algo

Generic base class for algorithms, parameterized by problem and solution types.

**Type Parameters:**
- `Problem` - bounded by `ProblemAlgo`
- `Solution` - bounded by `SolutionAlgo`

**Constructor:**
```python
def __init__(self,
             problem: Problem,
             name: str = 'Algorithm') -> None
```

**Class Attributes:**

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `cls_stats` | `type[StatsAlgo]` | `StatsAlgo` | Stats class to instantiate |

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `problem` | `Problem` | The input problem (alias for `self.input`) |

**Methods:**

| Method | Description |
|--------|-------------|
| `_run_post()` | Post-execution hook; records elapsed time to stats |

## Usage Examples

```python
from f_cs.algo import Algo
from f_cs.problem import ProblemAlgo
from f_cs.solution import SolutionAlgo
from f_cs.stats import StatsAlgo

# Define concrete implementations
class MyProblem(ProblemAlgo):
    def __init__(self, data):
        super().__init__(name='MyProblem')
        self.data = data

class MySolution(SolutionAlgo):
    pass

class MyAlgo(Algo[MyProblem, MySolution]):
    def _run(self) -> MySolution:
        # Override _run(), not run()
        return MySolution(
            problem=self.problem,
            is_valid=True,
            stats=self._stats
        )

# Execute algorithm
problem = MyProblem(data=[1, 2, 3])
algo = MyAlgo(problem=problem)
solution = algo.run()
```

## Inheritance Hierarchy

```
ProcessIO[Problem, Solution] (f_core.processes.i_2_io)
    │
    └── Algo[Problem, Solution]
            │
            └── (concrete algorithm implementations)
```

## Design Patterns

| Pattern | Usage |
|---------|-------|
| Generic Class | Parameterized by Problem and Solution types |
| Template Method | `_run_post()` hook for subclasses |
| Factory Attribute | `cls_stats` for customizable stats instantiation |
| Composition | Contains StatsAlgo instance |

## Dependencies

| Dependency | Purpose | Documentation |
|------------|---------|---------------|
| `f_core.processes.i_2_io.ProcessIO` | Input/Output process base | [i_2_io/claude.html](../../f_core/processes/i_2_io/claude.html) |
| `f_cs.problem.main.ProblemAlgo` | Problem type bound | [problem/claude.html](../problem/claude.html) |
| `f_cs.solution.main.SolutionAlgo` | Solution type bound | [solution/claude.html](../solution/claude.html) |
| `f_cs.stats.main.StatsAlgo` | Stats class | [stats/claude.html](../stats/claude.html) |
| `typing.Generic`, `TypeVar` | Generic type support | - |

## Related Modules

- [StatsAlgo](../stats/claude.html) - Algorithm execution statistics
- [ProblemAlgo](../problem/claude.html) - Algorithm problem definition
- [SolutionAlgo](../solution/claude.html) - Algorithm solution output
