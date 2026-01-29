# StatsAlgo Module

> **Location:** `f_cs/stats.py`
> **Purpose:** Base class for algorithm statistics and metrics

---

## Quick Reference

| Component | Description |
|-----------|-------------|
| `StatsAlgo` | Base class for tracking algorithm metrics |
| Default Metric | `elapsed` - execution time in seconds |
| Used By | [Algo](./algo.claude.md), [SolutionAlgo](./solution.claude.md) |
| Related | [ProblemAlgo](./problem.claude.md) |

---

## Architecture

```
StatsAlgo ──── (this module)
    │
    ├── Used by Algo (tracks metrics during execution)
    │
    └── Stored in SolutionAlgo (returned with solution)
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

## StatsAlgo Class

### Constructor

```python
def __init__(self, elapsed: int = 0) -> None
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `elapsed` | `int` | `0` | Initial elapsed time in seconds |

### Properties

| Property | Type | Access | Description |
|----------|------|--------|-------------|
| `elapsed` | `int` | read/write | Execution time in seconds |

### Implementation

```python
class StatsAlgo:
    def __init__(self, elapsed: int = 0) -> None:
        self._elapsed = elapsed

    @property
    def elapsed(self) -> int:
        return self._elapsed

    @elapsed.setter
    def elapsed(self, elapsed: int) -> None:
        self._elapsed = elapsed
```

---

## Usage Examples

### Basic Usage

```python
from f_cs.stats import StatsAlgo

stats = StatsAlgo()
print(stats.elapsed)  # 0

stats.elapsed = 5
print(stats.elapsed)  # 5
```

### Extend with Custom Metrics

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
    def comparisons(self, value: int) -> None:
        self._comparisons = value

    @property
    def swaps(self) -> int:
        return self._swaps

    @swaps.setter
    def swaps(self, value: int) -> None:
        self._swaps = value

    @property
    def record(self) -> dict:
        return {
            'elapsed': self.elapsed,
            'comparisons': self.comparisons,
            'swaps': self.swaps
        }
```

### Use in Algorithm

```python
from f_cs.algo import Algo

class SortingAlgo(Algo[SortingProblem, SortingSolution]):
    cls_stats = SortingStats  # Use custom stats class

    def _run(self) -> None:
        data = list(self.problem.data)

        # Track metrics during execution
        for i in range(len(data)):
            for j in range(i + 1, len(data)):
                self._stats.comparisons += 1
                if data[i] > data[j]:
                    data[i], data[j] = data[j], data[i]
                    self._stats.swaps += 1

        self._output = SortingSolution(
            is_valid=True,
            stats=self._stats,
            result=data
        )
```

---

## Integration with Algo

The [Algo](./algo.claude.md) class automatically:

1. Creates a `StatsAlgo` instance in `__init__`
2. Sets `elapsed` after execution in `_run_post`

```python
class Algo(ProcessIO[Problem, Solution]):
    cls_stats: type[StatsAlgo] = StatsAlgo  # Override for custom stats

    def __init__(self, problem: Problem, name: str = 'Algorithm') -> None:
        super().__init__(input=problem, name=name)
        self._stats: StatsAlgo = self.cls_stats()  # Create stats instance

    def _run_post(self) -> None:
        super()._run_post()
        self._stats.elapsed = self.elapsed  # Set elapsed time
```

---

## Related Classes

| Class | Location | Relationship |
|-------|----------|--------------|
| [Algo](./algo.claude.md) | `f_cs/algo.py` | Creates and populates StatsAlgo |
| [SolutionAlgo](./solution.claude.md) | `f_cs/solution.py` | Contains StatsAlgo instance |
| [ProblemAlgo](./problem.claude.md) | `f_cs/problem.py` | Algo's input type |

---

## Design Patterns

1. **Property Pattern** - Encapsulates `_elapsed` with getter/setter
2. **Template for Extension** - Override `cls_stats` in Algo for custom metrics
3. **Metrics Aggregation** - Collects runtime statistics for analysis
