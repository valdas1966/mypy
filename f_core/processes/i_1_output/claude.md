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
def __init__(self, name: str = 'ProcessOutput',
             is_recording: bool = False) -> None
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

### Subclass Contract
Subclasses **must** override `_run()` and **return** the output.
`run()` captures the return value into `_output` and returns it.

### Inherited (from ProcessBase)
```python
def _run(self) -> Output        # override this — return output
def _run_pre(self) -> None
def seconds_since_last_call(self) -> float
@property
def elapsed(self) -> float
@property
def recorder(self) -> Recorder
@property
def name(self) -> str
def __str__(self) -> str
def __eq__(self, other: object) -> bool
def __lt__(self, other: object) -> bool
def __hash__(self) -> int
```

## Inheritance (Hierarchy)

```
Equatable
 └── Comparable
      └── HasName
           └── ProcessBase ─── run() -> None, elapsed, recorder, timing
                │
                └── ProcessOutput[Output] ─── run() -> Output
```

| Base | Responsibility |
|------|----------------|
| `ProcessBase` | Template Method lifecycle, timing, recording |
| `HasName` | `name` as `key`, `str`, comparison, hash |

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
