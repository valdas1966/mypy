# ProcessBase

## Purpose
Abstract base class for all process classes. Provides a Template Method
lifecycle (`_run_pre` -> `_run` -> `_run_post`), execution timing via
`elapsed`, event recording via `recorder`, and a lap timer via
`seconds_since_last_call()`. Inherits name-based identity/comparison
from `HasName`.

## Public API

### Constructor
```python
def __init__(self, name: str = 'ProcessBase',
             is_recording: bool = False) -> None
```
Initializes timing attributes (`_elapsed`, `_time_start`,
`_time_finish`) to `None`, sets up the lap timer checkpoint,
and creates a `Recorder` (active when `is_recording=True`).

### Properties
```python
@property
def elapsed(self) -> float
```
Total execution time in seconds. `None` before `run()` completes.

```python
@property
def recorder(self) -> Recorder
```
The process's `Recorder` for structured event recording.

### Methods

```python
def run(self) -> None
```
Entry point. Orchestrates `_run_pre()` -> `_run()` -> `_run_post()`.

```python
def seconds_since_last_call(self) -> float
```
Returns seconds elapsed since the previous call to this method.
First call returns `0` and stores a checkpoint.

```python
def _run_pre(self) -> None
```
Resets `_elapsed` to `None` and records `_time_start`. Override rarely.

```python
def _run(self) -> None
```
Override in subclass with process logic. Default is no-op.

```python
def _run_post(self) -> None
```
Records `_time_finish` and calculates `_elapsed`. Override rarely.

### Inherited (from HasName)
```python
@property
def name(self) -> str
def __str__(self) -> str
def __repr__(self) -> str
def __eq__(self, other: object) -> bool
def __lt__(self, other: object) -> bool
def __le__(self, other: object) -> bool
def __gt__(self, other: object) -> bool
def __ge__(self, other: object) -> bool
def __hash__(self) -> int
```
All comparisons delegate to `name`.

## Inheritance (Hierarchy)

```
Equatable
 └── Comparable
      └── HasName ─────────── name, str(), comparison, hash
           │
           └── ProcessBase ─── run(), elapsed, recorder, timing
```

| Base | Responsibility |
|------|----------------|
| `Equatable` | `__eq__`, `__hash__` via `key` |
| `Comparable` | `__lt__`, `__le__`, `__gt__`, `__ge__` via `key` |
| `HasName` | `name` property as `key`, `__str__`, `__repr__` |

## Dependencies

| Import | Purpose |
|--------|---------|
| `f_core.mixins.has.HasName` | Name-based identity and comparison |
| `f_core.recorder.Recorder` | Structured event recording |
| `time.time` | Wall-clock timing for elapsed and lap |

## Usage Examples

### Basic Subclass

```python
from f_core.processes.i_0_base import ProcessBase


class MyProcess(ProcessBase):
    def _run(self) -> None:
        # process logic here
        pass


process = MyProcess(name='DataProcessor')
process.run()
print(process.elapsed)  # seconds taken
```

### Lap Timer

```python
import time
from f_core.processes.i_0_base import ProcessBase


class TimedSteps(ProcessBase):
    def _run(self) -> None:
        self.seconds_since_last_call()  # 0 (first call)
        time.sleep(2)
        print(self.seconds_since_last_call())  # 2
        time.sleep(3)
        print(self.seconds_since_last_call())  # 3


TimedSteps(name='Steps').run()
```
