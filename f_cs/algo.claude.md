# Algo Module

> **Location:** `f_cs/algo.py`
> **Purpose:** Generic base class for computer science algorithms

---

## Quick Reference

| Component | Description |
|-----------|-------------|
| `Algo[Problem, Solution]` | Generic algorithm base class |
| Type Parameters | `Problem` bound to [ProblemAlgo](./problem.claude.md), `Solution` bound to [SolutionAlgo](./solution.claude.md) |
| Inherits | [ProcessIO](../f_core/processes/i_2_io/claude.md) |
| Uses | [StatsAlgo](./stats.claude.md) for metrics |

---

## Architecture

```
ProcessIO[Problem, Solution]
    │
    └── Algo[Problem, Solution] ──── (this module)
            │
            ├── problem (property) → alias for input
            ├── _stats (StatsAlgo instance)
            └── cls_stats (class attribute for custom stats)
```

### CS Algorithm Pattern

```
┌─────────────┐      ┌───────────┐      ┌──────────────┐
│ ProblemAlgo │ ──▶  │   Algo    │ ──▶  │ SolutionAlgo │
│   (input)   │      │ (process) │      │   (output)   │
└─────────────┘      └─────┬─────┘      └──────┬───────┘
                           │                   │
                           ▼                   │
                     ┌───────────┐             │
                     │ StatsAlgo │ ◀───────────┘
                     │  (metrics)│   contains
                     └───────────┘
```

---

## Algo Class

### Type Parameters

```python
Problem = TypeVar('Problem', bound=ProblemAlgo)
Solution = TypeVar('Solution', bound=SolutionAlgo)
```

### Constructor

```python
def __init__(self,
             problem: Problem,
             name: str = 'Algorithm') -> None
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `problem` | `Problem` | *required* | The problem to solve |
| `name` | `str` | `'Algorithm'` | Algorithm name |

### Class Attributes

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `cls_stats` | `type[StatsAlgo]` | `StatsAlgo` | Stats class to instantiate |

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `problem` | `Problem` | Alias for `self.input` |
| `input` | `Problem` | From ProcessIO |
| `elapsed` | `int \| None` | From ProcessABC |
| `name` | `str` | From HasName |

### Instance Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `_stats` | `StatsAlgo` | Stats instance created in `__init__` |
| `_output` | `Solution \| None` | Set in `_run()` |

---

## Lifecycle

### Automatic Stats Population

```python
def _run_post(self) -> None:
    super()._run_post()
    self._stats.elapsed = self.elapsed  # Auto-populate elapsed time
```

### Execution Flow

```
algo.run()
    │
    ├── _run_pre()      # Reset timing
    │
    ├── _run()          # YOUR LOGIC: set self._output
    │
    ├── _run_post()     # Calculate elapsed, set _stats.elapsed
    │
    └── return self._output  # Return Solution
```

---

## Usage Examples

### Basic Algorithm

```python
from f_cs.algo import Algo
from f_cs.problem import ProblemAlgo
from f_cs.solution import SolutionAlgo
from f_cs.stats import StatsAlgo

class SortingProblem(ProblemAlgo):
    def __init__(self, data: list[int]):
        super().__init__(name='SortingProblem')
        self.data = data

class SortingSolution(SolutionAlgo[StatsAlgo]):
    def __init__(self, is_valid: bool, stats: StatsAlgo, result: list[int]):
        super().__init__(is_valid=is_valid, stats=stats)
        self._result = result

    @property
    def result(self) -> list[int]:
        return self._result

class SortingAlgo(Algo[SortingProblem, SortingSolution]):
    def _run(self) -> None:
        sorted_data = sorted(self.problem.data)
        self._output = SortingSolution(
            is_valid=True,
            stats=self._stats,
            result=sorted_data
        )

# Execute
problem = SortingProblem(data=[5, 2, 8, 1, 9])
algo = SortingAlgo(problem=problem, name='QuickSort')
solution = algo.run()

print(f"Input: {algo.problem.data}")
print(f"Output: {solution.result}")
print(f"Time: {solution.stats.elapsed}s")
```

### With Custom Stats

```python
class SortingStats(StatsAlgo):
    def __init__(self):
        super().__init__()
        self._comparisons = 0
        self._swaps = 0

    @property
    def comparisons(self) -> int:
        return self._comparisons

    @comparisons.setter
    def comparisons(self, value: int):
        self._comparisons = value

    @property
    def swaps(self) -> int:
        return self._swaps

    @swaps.setter
    def swaps(self, value: int):
        self._swaps = value

class BubbleSortAlgo(Algo[SortingProblem, SortingSolution]):
    cls_stats = SortingStats  # Use custom stats

    def _run(self) -> None:
        data = list(self.problem.data)
        n = len(data)

        for i in range(n):
            for j in range(0, n - i - 1):
                self._stats.comparisons += 1
                if data[j] > data[j + 1]:
                    data[j], data[j + 1] = data[j + 1], data[j]
                    self._stats.swaps += 1

        self._output = SortingSolution(
            is_valid=True,
            stats=self._stats,
            result=data
        )

# Execute
algo = BubbleSortAlgo(problem=SortingProblem([5, 2, 8, 1, 9]))
solution = algo.run()

print(f"Comparisons: {solution.stats.comparisons}")
print(f"Swaps: {solution.stats.swaps}")
print(f"Elapsed: {solution.stats.elapsed}s")
```

### Validity Checking

```python
solution = algo.run()

if solution:  # Calls __bool__() on SolutionAlgo
    print(f"Valid solution: {solution.result}")
else:
    print("Algorithm failed to find valid solution")
```

---

## Related Classes

| Class | Location | Relationship |
|-------|----------|--------------|
| [ProblemAlgo](./problem.claude.md) | `f_cs/problem.py` | Algo's input type |
| [SolutionAlgo](./solution.claude.md) | `f_cs/solution.py` | Algo's output type |
| [StatsAlgo](./stats.claude.md) | `f_cs/stats.py` | Metrics tracking |
| ProcessIO | `f_core/processes/i_2_io` | Parent class |

---

## Dependencies

**Inherits:**
- `f_core.processes.i_2_io.ProcessIO`

**Uses:**
- [f_cs.problem.ProblemAlgo](./problem.claude.md)
- [f_cs.solution.SolutionAlgo](./solution.claude.md)
- [f_cs.stats.StatsAlgo](./stats.claude.md)

---

## Design Patterns

1. **Generic Programming** - `Algo[Problem, Solution]` with bounded type variables
2. **Template Method** - Inherits lifecycle from ProcessIO
3. **Strategy Pattern** - `cls_stats` allows custom stats classes
4. **Alias Pattern** - `problem` property aliases `input` for clarity
