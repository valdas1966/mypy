# SolutionAlgo

## Purpose
Minimal base class for algorithm solutions. Serves as a type marker
and validity contract — domain subclasses add domain-specific data
(problem, path, stats, etc.).

## Public API

### Constructor
```python
def __init__(self, is_valid: bool) -> None
```

### Inherited
- `is_valid` property (from Validatable)
- `__bool__` returns `is_valid` (from Validatable)

## Inheritance
```
Validatable
    └── SolutionAlgo
```

## Design Decisions
- **Minimal by design** — only `is_valid` is universal to all
  algorithm solutions. Properties like `problem`, `elapsed`,
  `recorder`, and `name_algo` belong on domain-specific subclasses
  or on the `Algo` object itself (via `ProcessBase`).
- **Type marker** — exists as a bound for `Algo[Problem, Solution]`
  generic parameter, distinguishing algorithm outputs from any
  other `Validatable` object.

## Dependencies
- `f_core.mixins.validatable.Validatable`
