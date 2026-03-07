# ProblemAlgo

## Purpose
Abstract base class representing a problem definition for an algorithm.
Provides a named, equatable identity so problems can be compared and
identified.

## Public API

### `__init__(self, name: str = 'ProblemAlgo') -> None`
Initialize with a name (passed to `HasName`).

### `key -> SupportsEquality` (property)
Abstract. Subclasses must return a value used for equality comparison.
Raises `NotImplementedError`.

### Inherited from `HasName`
- `name -> str` (property): the problem's name.

### Inherited from `Equatable`
- `__eq__(self, other: object) -> bool`
- `__ne__(self, other: object) -> bool`
- `__hash__(self) -> int`

## Inheritance

```
HasName
    \
     ProblemAlgo
    /
Equatable
```

| Base | Responsibility |
|------|---------------|
| `HasName` | `name` property |
| `Equatable` | `__eq__`, `__ne__`, `__hash__` via `key` |

## Dependencies

| Import | Used For |
|--------|----------|
| `f_core.mixins.Equatable` | Equality based on `key` |
| `f_core.mixins.has.name.HasName` | `name` property |
| `f_core.protocols.equality.SupportsEquality` | Return type of `key` |

## Usage Example

```python
from f_cs.problem import ProblemAlgo

class MyProblem(ProblemAlgo):
    def __init__(self, data: list, name: str = 'MyProblem') -> None:
        super().__init__(name=name)
        self._data = data

    @property
    def key(self) -> str:
        return self.name

problem = MyProblem(data=[1, 2, 3])
print(problem.name)  # 'MyProblem'
```
