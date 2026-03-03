# ProcessInput

## Purpose
Generic process with a typed input parameter. Extends `ProcessBase`
with an `input` property, enabling type-safe data flow into process
logic. Subclass, override `_run()`, and access `self.input`.

## Public API

### Type Parameter
```python
Input = TypeVar('Input')
```

### Constructor
```python
def __init__(self,
             input: Input,
             name: str = 'Process Input') -> None
```
Stores `input` as `_input`, then delegates to `ProcessBase.__init__`.

### Properties
```python
@property
def input(self) -> Input
```
Read-only access to the input data.

### Inherited (from ProcessBase)
```python
def run(self) -> None
def _run(self) -> None          # override this
def _run_pre(self) -> None
def _run_post(self) -> None
def seconds_since_last_call(self) -> int
@property
def elapsed(self) -> int
@property
def name(self) -> str
def __str__(self) -> str
def __eq__(self, other: object) -> bool
def __lt__(self, other: object) -> bool
def __hash__(self) -> int
def __bool__(self) -> bool
```

## Inheritance (Hierarchy)

```
Equatable
 └── Comparable
      └── HasName
           └── ProcessBase ─── run(), elapsed, timing
                │
                └── ProcessInput[Input] ─── input property
                     │
                     └── ValidatableMutable ── __bool__()
```

| Base | Responsibility |
|------|----------------|
| `ProcessBase` | Template Method lifecycle, timing |
| `HasName` | `name` as `key`, `str`, comparison, hash |
| `ValidatableMutable` | `__bool__`, mutable `_is_valid` |

## Dependencies

| Import | Purpose |
|--------|---------|
| `f_core.processes.i_0_base.ProcessBase` | Parent class with lifecycle |
| `typing.Generic` | Generic class support |
| `typing.TypeVar` | `Input` type variable |

## Usage Examples

### Basic Subclass
```python
from f_core.processes.i_1_input import ProcessInput

class DataLoader(ProcessInput[str]):
    def _run(self) -> None:
        filepath = self.input
        print(f'Loading: {filepath}')

loader = DataLoader(input='/data/file.csv', name='Loader')
loader.run()
print(loader.elapsed)
```

### With Integer Input
```python
class Doubler(ProcessInput[int]):
    def _run(self) -> None:
        print(self.input * 2)

Doubler(input=5, name='Doubler').run()  # prints 10
```

### Factory
```python
from f_core.processes.i_1_input import ProcessInput

Proc = ProcessInput.Factory.a()
proc = Proc(input=1)
proc.run()
print(proc.input)  # 1
```
