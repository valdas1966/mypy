# MyPy Framework — Coding Conventions

## Project Structure

### Top-Level Modules
Framework modules use the `f_` prefix: `f_core`, `f_ds`, `f_search`, `f_google`, `f_utils`, `f_gui`, `f_cs`, etc.

### Module Internal Hierarchy
Modules use `i_X_name/` folders to express inheritance depth:
```
f_search/algos/
├── i_0_base/i_0_search/        # Level 0 — abstract root (AlgoSearch)
├── i_1_spp/                    # Level 1 — SPP family
│   ├── i_0_base/               # Level 1→0 — abstract SPP base
│   ├── i_1_astar/              # Level 1→1 — AStar
│   └── i_2_dijkstra/           # Level 1→2 — Dijkstra (extends AStar)
└── i_2_omspp/                  # Level 2 — One-to-Many family
```
The number after `i_` indicates the inheritance level within that scope. `i_0_` is always the abstract base.

### Standard Files Per Module
Every class module contains a subset of these files:
| File | Required | Purpose |
|------|----------|---------|
| `main.py` | Yes | Primary class implementation |
| `__init__.py` | Yes | Public exports; wires `Factory` onto the class |
| `_factory.py` | If testable | Factory class for creating common instances |
| `_tester.py` | If testable | pytest unit tests |
| `_study.py` | No | Exploratory / research scripts |
| `CLAUDE.md` | No | Module-specific docs for Claude Code |

Files prefixed with `_` are internal/private and not imported externally.

---

## Naming Conventions

### Folders
| Prefix | Meaning | Example |
|--------|---------|---------|
| `f_` | Framework module | `f_search`, `f_core`, `f_google` |
| `i_X_` | Inheritance level X | `i_0_base`, `i_1_astar`, `i_2_dijkstra` |
| (none) | Domain grouping | `algos/`, `problems/`, `solutions/`, `ds/` |

### Files
| Prefix | Meaning | Example |
|--------|---------|---------|
| `u_` | Utility module (functions, no classes) | `u_dict.py`, `u_file.py`, `u_datetime.py` |
| `c_` | Component / service wrapper | `c_loguru.py`, `c_timer.py` |
| `_` | Internal / private | `_factory.py`, `_tester.py` |
| (none) | Public module | `main.py` |

### Classes
- **PascalCase**: `AlgoSearch`, `CellBase`, `AStar`, `ProblemSPP`
- **Base classes**: named `*Base` or placed in `i_0_base/`
- **Mixins**: named as adjectives/capabilities — `Comparable`, `Printable`, `HasRowCol`, `ValidatableMutable`
- **Enums**: `TypeComparison`, `ServiceAccount`

### Functions and Methods
- **snake_case**: `_discover()`, `_handle_successor()`, `_need_relax()`
- **Private**: single `_` prefix — `_init_add_atts()`, `_pre_run()`
- **Factory statics**: short names for test objects — `a()`, `b()`, `gen()`

### Variables
- **Instance attributes**: `self._name` (single `_` for protected)
- **Local aliases**: short names in method bodies — `data = self._data`
- **Dict attributes**: descriptive prefixed names — `dict_g`, `dict_h`
- **Constants**: `_UPPER_CASE` — `_SCOPES = [...]`

### Type Variables
- PascalCase, descriptive, with bound:
```python
State = TypeVar('State', bound=StateBase)
Problem = TypeVar('Problem', bound=ProblemSearch)
Item = TypeVar('Item')
```

---

## Docstring Conventions

### Class Docstrings
Wrapped in `=` separator lines (until max-width of 80 chars per line):
```python
class AStar(Generic[State], AlgoSPP[State, DataHeuristics]):
    """
    ============================================================================
     AStar (A*) Algorithm.
    ============================================================================
    """
```

### Method Docstrings
Same separator style, brief single-line description:
```python
def _discover(self, state: State) -> None:
    """
    ========================================================================
     Discover the given State.
    ========================================================================
    """
```

### Inline Comments
Short, above the line they describe:
```python
# Aliases
data = self._data
# Set State's Parent
data.set_best_to_be_parent_of(state=state)
```

---

## Code Style

### Type Annotations
- Annotate all function parameters and return types.
- Use `-> None` for methods that return nothing.
- Use modern union syntax: `type | None` (not `Optional`).
- Use lowercase generics: `dict[str, any]`, `tuple[int, int]`, `list[str]`.

```python
def __init__(self,
             row: int,
             col: int,
             name: str = 'CellBase') -> None:

@property
def key(self) -> tuple[int, int]:
```

### Formatting
- **Indentation**: 4 spaces, no tabs.
- **Line length**: 80 characters.
- **Multi-line params**: align with opening parenthesis.
- **Blank lines**: 2 between top-level definitions, 1 between methods, none inside short methods.
- **Strings**: f-strings preferred — `f'{self.name}({self.row},{self.col})'`.
- **Named arguments** in calls: `data.set_best_to_be_parent_of(state=state)`.

### Class Definition Order
1. Class docstring
2. Class-level attributes (`Factory: type = None`, `cls_stats: type = ...`)
3. `__init__`
4. Properties (`@property`)
5. Public methods
6. Private methods (`_method`)
7. Dunder methods (`__str__`, `__repr__`, `__lt__`)

---

## Design Patterns

### Factory Pattern
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

### Mixin Composition
Prefer mixins over deep single inheritance. Mixins are adjectives:
```python
class CellBase(HasRowCol, HasName):
class CellMap(CellBase, ValidatableMutable):
class ProblemSPP(ProblemSearch, HasStart, HasGoal):
```

### Template Method (Lifecycle Hooks)
Base classes define hooks; subclasses override:
```python
def _pre_run(self) -> None: ...
def _post_run(self) -> None: ...
def _init_add_atts(self) -> None: ...
```

### Generics
Classes are parameterized with `Generic[...]`:
```python
class AlgoSearch(Generic[Problem, Solution], Algo[Problem, Solution]):
class AStar(Generic[State], AlgoSPP[State, DataHeuristics]):
```

### Total Ordering
For comparable classes, only implement `__lt__` with `@total_ordering`:
```python
@total_ordering
class Comparable(Equatable):
    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Comparable):
            return NotImplemented
        return self.key < other.key
```

---

## Testing Conventions

Tests live in `_tester.py` alongside `main.py`. Use pytest with fixtures that call Factory methods:
```python
import pytest

@pytest.fixture
def a() -> Comparable:
    """
    ========================================================================
     Create a Comparable object with the value 'A'.
    ========================================================================
    """
    return Comparable.Factory.a()

def test_lt(a: Comparable, b: Comparable) -> None:
    """
    ========================================================================
     Test the __lt__() method.
    ========================================================================
    """
    assert a < b
    assert not (b < a)
```

- Test functions: `test_<method_name>()`.
- Fixtures: short names matching Factory methods (`a`, `b`, `gen`).
- Each test has a docstring with `=` separators.

---

## __init__.py Convention

Public exports and Factory wiring only:
```python
from f_class.main import MyClass
from f_class._factory import Factory

MyClass.Factory = Factory
```

Never put logic in `__init__.py`.

---

## Domain Abbreviations

| Abbreviation | Meaning |
|-------------|---------|
| SPP | Shortest Path Problem (one-to-one) |
| OMSPP | One-to-Many Shortest Path Problem |
| DS | Data Structures |
| CS | Computer Science |

---

## Environment

- Python 3.13+ (Conda)
- Testing: pytest
- Logging: loguru
- No linter config — follows PEP 8 by convention
- Package name: `MyPy`
