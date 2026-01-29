# SolutionAlgo Module

> **Location:** `f_cs/solution.py`
> **Purpose:** Generic base class for algorithm solutions (output)

---

## Quick Reference

| Component | Description |
|-----------|-------------|
| `SolutionAlgo[Stats]` | Generic base class for algorithm output |
| Type Parameter | `Stats` bound to [StatsAlgo](./stats.claude.md) |
| Inherits | ValidatablePublic, HasRecord |
| Used By | [Algo](./algo.claude.md) as output type |
| Related | [ProblemAlgo](./problem.claude.md), [StatsAlgo](./stats.claude.md) |

---

## Architecture

```
ValidatablePublic ─┬─ SolutionAlgo[Stats] ──── (this module)
                   │       │
HasRecord ─────────┘       ├── is_valid (from ValidatablePublic)
                           ├── stats property
                           └── record property
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

## SolutionAlgo Class

### Type Parameter

```python
Stats = TypeVar('Stats', bound=StatsAlgo)
```

### Constructor

```python
def __init__(self,
             is_valid: bool,
             stats: Stats,
             name: str = 'SolutionAlgo') -> None
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `is_valid` | `bool` | *required* | Whether the solution is valid |
| `stats` | `Stats` | *required* | Algorithm statistics |
| `name` | `str` | `'SolutionAlgo'` | Solution name |

### Properties

| Property | Type | Source | Description |
|----------|------|--------|-------------|
| `stats` | `Stats` | SolutionAlgo | Algorithm statistics |
| `is_valid` | `bool` | ValidatablePublic | Solution validity |
| `record` | `dict` | HasRecord | Serialization |

### RECORD_SPEC

```python
RECORD_SPEC = {
    'is_valid': lambda o: bool(o),
    'stats': lambda o: o.stats.record
}
```

---

## Usage Examples

### Basic Solution

```python
from f_cs.solution import SolutionAlgo
from f_cs.stats import StatsAlgo

stats = StatsAlgo(elapsed=5)
solution = SolutionAlgo(
    is_valid=True,
    stats=stats,
    name='MySolution'
)

print(bool(solution))  # True
print(solution.stats.elapsed)  # 5
```

### Custom Solution with Results

```python
class SortingSolution(SolutionAlgo[SortingStats]):
    RECORD_SPEC = {
        'is_valid': lambda o: bool(o),
        'stats': lambda o: o.stats.record,
        'result': lambda o: o.result
    }

    def __init__(self,
                 is_valid: bool,
                 stats: SortingStats,
                 result: list[int]):
        super().__init__(is_valid=is_valid, stats=stats, name='SortingSolution')
        self._result = result

    @property
    def result(self) -> list[int]:
        return self._result
```

### Use in Algorithm

```python
from f_cs.algo import Algo

class SortingAlgo(Algo[SortingProblem, SortingSolution]):
    cls_stats = SortingStats

    def _run(self) -> None:
        sorted_data = sorted(self.problem.data)

        self._output = SortingSolution(
            is_valid=True,
            stats=self._stats,
            result=sorted_data
        )

# Execute
algo = SortingAlgo(problem=SortingProblem([5, 2, 8]))
solution = algo.run()

if solution:  # Calls __bool__() -> is_valid
    print(f"Sorted: {solution.result}")
    print(f"Time: {solution.stats.elapsed}s")
```

---

## Validity Checking

From `ValidatablePublic`, solutions support boolean evaluation:

```python
solution = SortingSolution(is_valid=True, stats=stats, result=[1, 2, 3])

if solution:  # True
    print("Valid solution")

# Set validity
solution.is_valid = False

if not solution:  # True
    print("Invalid solution")
```

---

## Serialization

The `record` property returns a dict for serialization:

```python
solution = SortingSolution(
    is_valid=True,
    stats=SortingStats(),
    result=[1, 2, 3]
)

print(solution.record)
# {
#     'is_valid': True,
#     'stats': {'elapsed': 0, 'comparisons': 0, 'swaps': 0},
#     'result': [1, 2, 3]
# }
```

---

## Related Classes

| Class | Location | Relationship |
|-------|----------|--------------|
| [Algo](./algo.claude.md) | `f_cs/algo.py` | Produces SolutionAlgo as output |
| [ProblemAlgo](./problem.claude.md) | `f_cs/problem.py` | Algo's input type |
| [StatsAlgo](./stats.claude.md) | `f_cs/stats.py` | Contained in SolutionAlgo |

---

## Dependencies

**Inherits:**
- `f_core.mixins.validatable_public.ValidatablePublic`
- `f_core.mixins.has.record.HasRecord`

**Uses:**
- [f_cs.stats.StatsAlgo](./stats.claude.md)

---

## Design Patterns

1. **Generic Programming** - `SolutionAlgo[Stats]` with bounded type variable
2. **Multiple Inheritance** - Combines ValidatablePublic + HasRecord
3. **Property Pattern** - `stats` wraps `_stats`
4. **Record Pattern** - `RECORD_SPEC` for serialization
