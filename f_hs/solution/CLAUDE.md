# SolutionSPP

## Purpose
Solution for Shortest-Path-Problem. Holds the optimal cost.
Path reconstruction is handled by the Algo (not the Solution),
because it requires the algorithm's internal data (parent pointers).

## Public API

### Constructor
```python
def __init__(self, cost: float) -> None
```

### Properties
| Property | Type | Description |
|----------|------|-------------|
| `cost` | `float` | The optimal path cost |

### Inherited from SolutionAlgo
| Member | Type | Description |
|--------|------|-------------|
| `is_valid` | `bool` | Derived from `cost < inf` |
| `__bool__` | | `bool(solution)` returns `is_valid` |

## Factory
| Method | Returns | Description |
|--------|---------|-------------|
| `valid()` | `SolutionSPP` | cost=5.0, is_valid=True |
| `invalid()` | `SolutionSPP` | cost=inf, is_valid=False |
| `zero()` | `SolutionSPP` | cost=0.0, is_valid=True |

## Design Decisions
- **Cost only** — path reconstruction belongs on the Algo.
- **is_valid derived from cost** — `cost < inf` means valid.

## Dependencies
- `f_cs.solution.SolutionAlgo`
