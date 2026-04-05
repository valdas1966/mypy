# ProblemSPP

## Purpose
Shortest-Path-Problem covering all four variants (OO, OM, MO, MM)
via `starts` and `goals` lists. The variant is determined by
cardinality, not class type. Domain subclasses implement
`successors()` for their specific search space.

## Public API

### Constructor
```python
def __init__(self,
             starts: list[State],
             goals: list[State],
             name: str = 'ProblemSPP') -> None
```

### Properties
| Property | Type | Description |
|----------|------|-------------|
| `starts` | `list[State]` | All start states |
| `goals` | `list[State]` | All goal states |
| `start` | `State` | First start (convenience for single-start) |
| `goal` | `State` | First goal (convenience for single-goal) |
| `key` | `tuple` | `(tuple(starts), tuple(goals))` for equality |

### Abstract Methods
| Method | Signature | Description |
|--------|-----------|-------------|
| `successors` | `(state: State) -> list[State]` | Domain-specific neighbor generation |

### Inherited from ProblemAlgo
- `name: str` — problem name
- `__eq__`, `__hash__` — via `key` (from Equatable)

## Type Parameters
- `State` — bounded by `StateBase`

## Inheritance
```
HasName + Equatable
    └── ProblemAlgo
            └── ProblemSPP[State]
```

## SPP Variant Matrix
| Variant | starts | goals |
|---------|--------|-------|
| OOSPP | `[s]` | `[g]` |
| OMSPP | `[s]` | `[g1, g2, ...]` |
| MOSPP | `[s1, s2, ...]` | `[g]` |
| MMSPP | `[s1, s2, ...]` | `[g1, g2, ...]` |

## Design Decisions
- **One class for all variants** — the 4 configurations differ
  only in cardinality of starts/goals (a 2-bit boolean), not
  in structure. Separate classes would be over-engineering.
- **successors on Problem** — the Problem defines the search space
  (what the neighbors are). The Algorithm decides which states
  to expand; the Problem decides what neighbors exist.
- **Heuristic NOT on Problem** — heuristic functions are an
  algorithm/domain concern, not a problem definition concern.

## Dependencies
- `f_cs.problem.ProblemAlgo`
- `f_hs.state.StateBase`
