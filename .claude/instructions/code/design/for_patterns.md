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
Example compositions, base to derived:
```python
class CellBase(HasRowCol, HasName):
class CellMap(CellBase, ValidatableMutable):
class ProblemSPP(ProblemSearch, HasStart, HasGoal):
```

## Abstract Methods (ABCs)
A genuinely-abstract method is decorated `@abstractmethod` and its body
is `raise NotImplementedError` — **never `pass`**. The decorator blocks
construction of any subclass that omits it; the `raise` is the call-time
guard for the body that still runs on `super().method()` delegation or
ABC-bypass (where a `pass` body would silently return a wrong `None`):
```python
from abc import abstractmethod

class FrontierBase(Sizable):
    @abstractmethod
    def pop(self) -> State:
        raise NotImplementedError
```
Reserve bare `pass` / `...` for the **optional** Template-Method hooks
below — that keeps must-override and may-override visually distinct.
Exception: `typing.Protocol` members use `...` (idiomatic, never
instantiated); do not convert them to `raise`.

## Template Method (Lifecycle Hooks)
Base classes define **optional** hooks; subclasses override as needed.
The hook body is a no-op (`pass` / `...`), not `raise` — its absence in
a subclass is legal (unlike an `@abstractmethod`):
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
domain objects).

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
