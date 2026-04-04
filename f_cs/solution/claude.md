# SolutionAlgo

## Purpose
Abstract base class for algorithm solutions. Packages the result
of an algorithm execution: validity, elapsed time, problem reference,
and optional recorded events.

## Public API

### Constructor
```python
def __init__(self,
             name_algo: str,
             problem: Problem,
             is_valid: bool,
             elapsed: float = 0,
             recorder: Recorder | None = None) -> None
```

### Properties
| Property | Type | Description |
|----------|------|-------------|
| `name_algo` | `str` | Name of the algorithm that produced this |
| `problem` | `Problem` | The problem this solution solves |
| `elapsed` | `float` | Execution time in seconds |
| `recorder` | `Recorder` | Recorded events (empty if not recording) |

### Inherited
- `__bool__` returns `is_valid` (from Validatable)

## Type Parameters
- `Problem` — bounded by `ProblemAlgo`

## Inheritance
```
Validatable + Generic[Problem]
    └── SolutionAlgo
```

## Dependencies
- `f_core.mixins.validatable.Validatable`
- `f_core.recorder.Recorder`
- `f_cs.problem.ProblemAlgo`
