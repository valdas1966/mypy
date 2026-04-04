# Algo

## Purpose
Base class for algorithms in Computer Science. Orchestrates problem
input, solution output, and execution lifecycle. Inherits timing
(`elapsed`) and event recording (`recorder`) from ProcessBase.

## Public API

### Constructor
```python
def __init__(self,
             problem: Problem,
             name: str = 'Algorithm',
             is_recording: bool = False) -> None
```

### Properties
| Property | Type | Description |
|----------|------|-------------|
| `problem` | `Problem` | The input problem (alias for `self.input`) |
| `elapsed` | `float` | Execution time (inherited from ProcessBase) |
| `recorder` | `Recorder` | Event recorder (inherited from ProcessBase) |
| `name` | `str` | Algorithm name (inherited from HasName) |

### Lifecycle (inherited from ProcessBase)
| Method | Description |
|--------|-------------|
| `run()` | Entry point — returns Solution |
| `_run_pre()` | Reset timing |
| `_run()` | Override with algorithm logic |
| `_run_post()` | Record elapsed time |

## Type Parameters
- `Problem` — bounded by `ProblemAlgo`
- `Solution` — bounded by `SolutionAlgo`

## Inheritance
```
ProcessIO[Problem, Solution]
    └── Algo[Problem, Solution]
```

## Dependencies
- `f_core.processes.i_2_io.ProcessIO`
- `f_cs.problem.ProblemAlgo`
- `f_cs.solution.SolutionAlgo`
