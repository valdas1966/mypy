# ProcessOutput

## Purpose
Generic process that produces typed output. Extends `ProcessBase`
and overrides `run()` to return the computed output. Subclass,
override `_run()` to **return** the result, and call `run()` to
get it.

## Public API

### Type Parameter
```python
Output = TypeVar('Output')
```

### Constructor
```python
def __init__(self, name: str = 'ProcessOutput') -> None
```
Initializes `_output` to `None`, then delegates to
`ProcessBase.__init__`.

### Methods

```python
def run(self) -> Output
```
Overrides `ProcessBase.run()`. Executes the lifecycle
(`_run_pre` -> `_run` -> `_run_post`), captures the return
value of `_run()` into `_output`, and **returns** it.

```python
def _run_post(self) -> None
```
Overrides to call `ProcessBase._run_post(self)` explicitly.

### Private Attributes
```python
_output: Output | None = None
```
Set by `run()` from `_run()`'s return value. Returned by `run()`.

### Subclass Contract
Subclasses **must** override `_run()` and **return** the output.
`run()` captures the return value into `_output` and returns it.

### Inherited (from ProcessBase)
```python
def _run(self) -> Output        # override this — return output
def _run_pre(self) -> None
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
                └── ProcessOutput[Output] ─── run() -> Output
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
| `typing.TypeVar` | `Output` type variable |

## Usage Examples

### Basic Subclass
```python
from f_core.processes.i_1_output import ProcessOutput

class Generator(ProcessOutput[list[int]]):
    def _run(self) -> list[int]:
        return [1, 2, 3, 4, 5]

result = Generator(name='Gen').run()
print(result)  # [1, 2, 3, 4, 5]
```

### With String Output
```python
class Greeter(ProcessOutput[str]):
    def __init__(self, greeting: str):
        self._greeting = greeting
        super().__init__(name='Greeter')

    def _run(self) -> str:
        return f'Hello, {self._greeting}!'

message = Greeter(greeting='World').run()
print(message)  # "Hello, World!"
```

### Factory
```python
from f_core.processes.i_1_output import ProcessOutput

proc = ProcessOutput.Factory.a()
result = proc.run()
print(result)  # 1
```
