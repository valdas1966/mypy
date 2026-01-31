# f_cs - Computer Science Algorithm Framework

> **Location:** `f_cs/`
> **Purpose:** Base classes for implementing algorithms with problems, solutions, and statistics

---

## Quick Reference

| Component | File | Description |
|-----------|------|-------------|
| `Algo[Problem, Solution]` | `algo.py` | Base class for all algorithms |
| `ProblemAlgo` | `problem.py` | ABC marker for algorithm problems |
| `SolutionAlgo[Stats]` | `solution.py` | ABC for algorithm solutions |
| `StatsAlgo` | `stats.py` | ABC for algorithm statistics |

---

## Architecture

```
ProcessIO[Input, Output] (f_core)
    │
    └── Algo[Problem, Solution]
            │
            ├── problem: Problem (input)
            ├── _stats: StatsAlgo
            └── run() → Solution (output)

ProblemAlgo ──────── Input to algorithm
SolutionAlgo[Stats] ── Output from algorithm
StatsAlgo ─────────── Performance metrics
```

### Data Flow

```
ProblemAlgo ──→ Algo ──→ SolutionAlgo
                │              │
                └── StatsAlgo ─┘
```

---

## Files

| File | Purpose |
|------|---------|
| `algo.py` | Core `Algo[Problem, Solution]` class |
| `problem.py` | `ProblemAlgo` ABC marker class |
| `solution.py` | `SolutionAlgo[Stats]` with validity and stats |
| `stats.py` | `StatsAlgo` with elapsed time tracking |
| `experiments.py` | Experiment runner utilities |
| `experiments_example.py` | Example experiment usage |

---

## Algo Class

### Type Parameters

```python
Problem = TypeVar('Problem', bound=ProblemAlgo)
Solution = TypeVar('Solution', bound=SolutionAlgo)
```

### Inheritance

```python
class Algo(Generic[Problem, Solution], ProcessIO[Problem, Solution])
```

Inherits from `ProcessIO`, treating:
- **Input** = `Problem`
- **Output** = `Solution`

### Constructor

```python
def __init__(self, problem: Problem, name: str = 'Algorithm') -> None
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `problem` | `Problem` | *required* | The problem instance to solve |
| `name` | `str` | `'Algorithm'` | Algorithm name for identification |

### Class Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `cls_stats` | `type[StatsAlgo]` | Stats class to instantiate (override in subclasses) |

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `problem` | `Problem` | Read-only access to the problem (alias for `input`) |

### Private Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `_stats` | `StatsAlgo` | Statistics object for tracking performance |

### Lifecycle Methods

| Method | Description |
|--------|-------------|
| `_run_post()` | Records elapsed time to `_stats.elapsed` after execution |

---

## ProblemAlgo Class

Marker class for algorithm problems. Empty ABC that serves as a type bound.

```python
class ProblemAlgo:
    """ABC for Algorithm's Problem."""
    pass
```

Subclass this to define specific problem types with their own attributes.

---

## SolutionAlgo Class

### Type Parameters

```python
Stats = TypeVar('Stats', bound=StatsAlgo)
```

### Inheritance

```python
class SolutionAlgo(Generic[Stats], ValidatablePublic)
```

### Constructor

```python
def __init__(self, is_valid: bool, stats: Stats, name: str = 'SolutionAlgo') -> None
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `is_valid` | `bool` | *required* | Whether the solution is valid |
| `stats` | `Stats` | *required* | Statistics from the algorithm run |
| `name` | `str` | `'SolutionAlgo'` | Solution name |

### Class Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `RECORD_SPEC` | `dict` | Specification for serializing to record format |

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `is_valid` | `bool` | From `ValidatablePublic` - solution validity |
| `stats` | `Stats` | Algorithm performance statistics |

---

## StatsAlgo Class

### Constructor

```python
def __init__(self, elapsed: int = 0) -> None
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `elapsed` | `int` | `0` | Elapsed time in seconds |

### Properties

| Property | Type | Access | Description |
|----------|------|--------|-------------|
| `elapsed` | `int` | get/set | Execution time in seconds |

---

## Usage Examples

### Basic Algorithm

```python
from f_cs.algo import Algo
from f_cs.problem import ProblemAlgo
from f_cs.solution import SolutionAlgo
from f_cs.stats import StatsAlgo

class MyProblem(ProblemAlgo):
    def __init__(self, data: list[int]):
        self.data = data

class MySolution(SolutionAlgo[StatsAlgo]):
    def __init__(self, result: int, stats: StatsAlgo):
        super().__init__(is_valid=True, stats=stats)
        self.result = result

class SumAlgo(Algo[MyProblem, MySolution]):
    def _run(self) -> None:
        result = sum(self.problem.data)
        self._output = MySolution(result=result, stats=self._stats)

# Usage
problem = MyProblem(data=[1, 2, 3, 4, 5])
algo = SumAlgo(problem=problem, name='Sum')
solution = algo.run()
print(solution.result)        # 15
print(solution.stats.elapsed) # execution time
```

### Custom Statistics

```python
class MyStats(StatsAlgo):
    def __init__(self):
        super().__init__()
        self.iterations = 0
        self.nodes_explored = 0

class SearchAlgo(Algo[MyProblem, MySolution]):
    cls_stats = MyStats  # Override stats class

    def _run(self) -> None:
        stats: MyStats = self._stats
        # Algorithm logic...
        stats.iterations = 100
        stats.nodes_explored = 500
```

---

## Inheritance Hierarchy

```
f_core.ProcessIO[Problem, Solution]
    │
    └── f_cs.Algo[Problem, Solution]
            │
            ├── f_search.AlgoSearch
            │       ├── AlgoSPP (A*, Dijkstra)
            │       └── AlgoOMSPP (K×A*)
            │
            └── (your algorithms)
```

---

## Design Patterns

1. **Template Method** - Lifecycle hooks (`_run_pre`, `_run`, `_run_post`)
2. **Generic Programming** - Type-safe Problem/Solution pairs
3. **Factory Pattern** - `cls_stats` class attribute for stats instantiation
4. **Marker Interface** - `ProblemAlgo` as type bound

---

## Dependencies

**Inherits:**
- [f_core.processes.i_2_io.ProcessIO](../f_core/processes/i_2_io/claude.md)

**Uses:**
- [f_core.mixins.validatable_public.ValidatablePublic](../f_core/mixins/validatable_public/claude.md)

**Standard Library:**
- `typing.Generic`, `typing.TypeVar`

---

## Comparison with ProcessIO

| Aspect | ProcessIO | Algo |
|--------|-----------|------|
| Type Params | `[Input, Output]` | `[Problem, Solution]` |
| Input Access | `self.input` | `self.problem` |
| Statistics | None | `self._stats` |
| Post-run | Basic | Records elapsed time |
| Purpose | Generic I/O | Algorithm framework |
