# ProblemAlgo Module

> **Location:** `f_cs/problem.py`
> **Purpose:** Abstract base class for algorithm problems

---

## Quick Reference

| Component | Description |
|-----------|-------------|
| `ProblemAlgo` | Base class for algorithm input problems |
| Inherits | HasRecord |
| Used By | [Algo](./algo.claude.md) as input type |
| Related | [SolutionAlgo](./solution.claude.md), [StatsAlgo](./stats.claude.md) |

---

## Architecture

```
HasRecord
    └── ProblemAlgo ──── (this module)
             │
             └── Input to Algo
```

### CS Algorithm Pattern

```
┌─────────────┐      ┌───────────┐      ┌──────────────┐
│ ProblemAlgo │ ──▶  │   Algo    │ ──▶  │ SolutionAlgo │
│   (input)   │      │ (process) │      │   (output)   │
└─────────────┘      └───────────┘      └──────────────┘
                           │
                           ▼
                     ┌───────────┐
                     │ StatsAlgo │
                     └───────────┘
```

---

## ProblemAlgo Class

### Definition

```python
class ProblemAlgo(HasRecord):
    pass
```

A minimal base class that:
- Inherits `HasRecord` for record/serialization support
- Serves as a type constraint for [Algo](./algo.claude.md)'s `Problem` type parameter

### From HasRecord

| Member | Description |
|--------|-------------|
| `record` | Property for serialization |
| `RECORD_SPEC` | Override to define record fields |
| `name` | From HasName (through HasRecord) |

---

## Usage Examples

### Define a Problem

```python
from f_cs.problem import ProblemAlgo

class SortingProblem(ProblemAlgo):
    RECORD_SPEC = {'size': lambda o: len(o.data)}

    def __init__(self, data: list[int]):
        super().__init__(name='SortingProblem')
        self.data = data

problem = SortingProblem(data=[5, 2, 8, 1, 9])
```

### Use with Algo

```python
from f_cs.algo import Algo
from f_cs.solution import SolutionAlgo

class SortingAlgo(Algo[SortingProblem, SortingSolution]):
    def _run(self) -> None:
        sorted_data = sorted(self.problem.data)
        self._output = SortingSolution(
            is_valid=True,
            stats=self._stats,
            result=sorted_data
        )

algo = SortingAlgo(problem=SortingProblem([5, 2, 8, 1, 9]))
solution = algo.run()
```

---

## Related Classes

| Class | Location | Relationship |
|-------|----------|--------------|
| [Algo](./algo.claude.md) | `f_cs/algo.py` | Consumes ProblemAlgo as input |
| [SolutionAlgo](./solution.claude.md) | `f_cs/solution.py` | Algo's output type |
| [StatsAlgo](./stats.claude.md) | `f_cs/stats.py` | Tracks algorithm metrics |

---

## Dependencies

**Inherits:**
- `f_core.mixins.has.record.HasRecord`

**Through HasRecord:**
- `f_core.mixins.has.name.HasName`
