# ProcessIO

## Purpose
Generic process combining input and output capabilities.
Extends `ProcessInput[Input]` and `ProcessOutput[Output]`
via multiple inheritance. Subclass, override `_run()` to read
`self.input` and **return** the output, then call `run()`.

## Public API

### Type Parameters
```python
Input = TypeVar('Input')
Output = TypeVar('Output')
```

### Constructor
```python
def __init__(self,
             input: Input,
             name: str = 'ProcessIO') -> None
```
Delegates to `ProcessInput.__init__` and `ProcessOutput.__init__`.

### Methods

```python
def run(self) -> Output
```
Delegates to `ProcessOutput.run(self)` which executes the
lifecycle (`_run_pre` -> `_run` -> `_run_post`), captures the
return value of `_run()` into `_output`, and returns it.

### Subclass Contract
Subclasses **must** override `_run()`, read `self.input`, and
**return** the output. `run()` captures the return value.

### Inherited (from ProcessInput)
```python
@property
def input(self) -> Input
```

### Inherited (from ProcessBase)
```python
def _run(self) -> Output        # override this — return output
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
           └── ProcessBase ─── run() -> None, elapsed, timing
                │
                ├── ProcessInput[Input] ─── input property
                │
                ├── ProcessOutput[Output] ─── run() -> Output
                │
                └── ProcessIO[Input, Output] ─── combines both
                     │
                     └── ValidatableMutable ── __bool__()
```

| Base | Responsibility |
|------|----------------|
| `ProcessInput` | `input` property, generic `Input` type |
| `ProcessOutput` | `run()` returns `Output`, `_output` attribute |
| `ProcessBase` | Template Method lifecycle, timing |
| `HasName` | `name` as `key`, `str`, comparison, hash |
| `ValidatableMutable` | `__bool__`, mutable `_is_valid` |

## Dependencies

| Import | Purpose |
|--------|---------|
| `f_core.processes.i_1_input.ProcessInput` | Input parent class |
| `f_core.processes.i_1_output.ProcessOutput` | Output parent class |
| `typing.Generic` | Generic class support |
| `typing.TypeVar` | `Input` and `Output` type variables |

## Usage Examples

### Basic Subclass
```python
from f_core.processes.i_2_io import ProcessIO

class Doubler(ProcessIO[int, int]):
    def _run(self) -> int:
        return self.input * 2

result = Doubler(input=5, name='Doubler').run()
print(result)  # 10
```

### String Transformation
```python
class UpperCase(ProcessIO[str, str]):
    def _run(self) -> str:
        return self.input.upper()

result = UpperCase(input='hello', name='Upper').run()
print(result)  # 'HELLO'
```

### Different Input/Output Types
```python
class Parser(ProcessIO[str, list[int]]):
    def _run(self) -> list[int]:
        return [int(x) for x in self.input.split(',')]

result = Parser(input='1,2,3', name='Parser').run()
print(result)  # [1, 2, 3]
```

### Factory
```python
from f_core.processes.i_2_io import ProcessIO

Square = ProcessIO.Factory.square()
result = Square(input=4).run()
print(result)  # 16
```
