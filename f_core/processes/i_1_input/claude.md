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
             name: str = 'Process Input',
             is_recording: bool = False) -> None
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
           └── ProcessBase ─── run(), elapsed, recorder, timing
                │
                └── ProcessInput[Input] ─── input property
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
