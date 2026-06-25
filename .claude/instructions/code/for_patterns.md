# Instruction to AI Agent (Claude Code): Design Patterns

Canonical patterns used across the MyPy framework. Match the surrounding
code; use these forms unless a module documents its own variant.

## Factory Pattern
Each class declares `Factory: type = None`. The actual Factory is defined in `_factory.py` and wired in `__init__.py`:
```python
# main.py
class MyClass:
    Factory: type = None

# _factory.py
class Factory:
    @staticmethod
    def a() -> 'MyClass':
        ...

# __init__.py
from .main import MyClass
from ._factory import Factory
MyClass.Factory = Factory
```

## Mixin Composition
Prefer mixins over deep single inheritance. Mixins are adjectives:
```python
class CellBase(HasRowCol, HasName):
class CellMap(CellBase, ValidatableMutable):
class ProblemSPP(ProblemSearch, HasStart, HasGoal):
```

## Template Method (Lifecycle Hooks)
Base classes define hooks; subclasses override:
```python
def _pre_run(self) -> None: ...
def _post_run(self) -> None: ...
def _init_add_atts(self) -> None: ...
```

## Generics
Classes are parameterized with `Generic[...]`:
```python
class AlgoSearch(Generic[Problem, Solution], Algo[Problem, Solution]):
class AStar(Generic[State], AlgoSPP[State, DataHeuristics]):
```

## Comparison Operators
For comparable classes, implement all four operators explicitly for
performance (no `@total_ordering` overhead). Delegate to `key`:
```python
class Comparable(Equatable):
    def __lt__(self, other: object) -> bool:
        return self.key < other.key
    def __le__(self, other: object) -> bool:
        return self.key <= other.key
    def __gt__(self, other: object) -> bool:
        return self.key > other.key
    def __ge__(self, other: object) -> bool:
        return self.key >= other.key
```
Comparison/equality dunders keep `other: object` (they delegate to
`key` and nominally accept any object) — do **not** narrow them to
`Self`. `Self` is for same-type *domain* methods instead, e.g.
`distance(self, other: Self) -> int`.

## Dataclasses vs Manual `__init__`
Use `@dataclass` for **data-holder classes** with no business logic:
```python
@dataclass
class ResultTest:
    passed: int = 0
    failed: int = 0
    failures: list[str] = field(default_factory=list)
```
Use **manual `__init__`** for behavior-rich classes (mixins, algorithms,
domain objects). Do not use `attrs`.

## Error Handling
No custom exception classes — use built-in exceptions (`ValueError`,
`FileNotFoundError`, `TypeError`). For operations that can fail
partially, capture the error as a string:
```python
try:
    response = requests.get(url=url, timeout=timeout)
except Exception as e:
    exception = str(e)
```

## Async
Not used. The entire codebase is synchronous.
