# Processes Package

## Purpose
Process framework providing a hierarchy of reusable process classes
with Template Method lifecycle (`_run_pre` -> `_run` -> `_run_post`),
automatic timing, and optional input/output typing. Designed to be
subclassed: override `_run()` with your logic, call `run()`.

## Public API (Package Exports)

```python
from f_core.processes import ProcessIO, ProcessParallel
```

| Export | Type Params | Description |
|--------|-------------|-------------|
| `ProcessIO` | `[Input, Output]` | Process with typed input and output |
| `ProcessParallel` | `[Item, Output]` | Parallel chunked execution |

## Module Hierarchy

```
f_core/processes/
├── i_0_base/        ProcessBase         — ABC, lifecycle, timing
├── i_1_input/       ProcessInput[Input] — adds input property
├── i_1_output/      ProcessOutput[Output] — run() returns Output
├── i_2_io/          ProcessIO[Input, Output] — input + output
└── i_3_parallel/    ProcessParallel[Item, Output] — parallel chunks
```

## Inheritance Chain

```
Equatable
 └── Comparable
      └── HasName ─── name, str(), comparison, hash
           └── ProcessBase ─── run(), elapsed, recorder, timing
                │
                ├── ProcessInput[Input] ─── input property
                │
                ├── ProcessOutput[Output] ─── run() -> Output
                │
                └── ProcessIO[Input, Output] ─── combines both
                     │
                     └── ProcessParallel[Item, Output] ─── parallel
```

## Class Comparison

| Class | Input | Output | Parallel | Use Case |
|-------|-------|--------|----------|----------|
| `ProcessBase` | No | No | No | Side-effect-only processes |
| `ProcessInput` | Yes | No | No | Consume input, no return |
| `ProcessOutput` | No | Yes | No | Generate output |
| `ProcessIO` | Yes | Yes | No | Transform input to output |
| `ProcessParallel` | Yes | Yes | Yes | Distribute work across workers |

## Lifecycle

All processes share the same Template Method lifecycle:
1. `run()` — entry point (returns `Output` for IO/Parallel)
2. `_run_pre()` — resets timing, records start time
3. `_run()` — **override this** with your logic
4. `_run_post()` — records finish time, calculates `elapsed`

## Dependencies

| Import | Purpose |
|--------|---------|
| `f_core.mixins.has.HasName` | Name-based identity and comparison |
| `f_core.recorder.Recorder` | Structured event recording |
| `f_ds.groups.Group` | Chunking for ProcessParallel |
| `concurrent.futures` | Thread/process pools for ProcessParallel |

## Usage Examples

### Simple Transform
```python
from f_core.processes import ProcessIO

class Doubler(ProcessIO[int, int]):
    def _run(self) -> int:
        return self.input * 2

result = Doubler(input=5, name='Doubler').run()  # 10
```

### Parallel Execution
```python
from f_core.processes import ProcessParallel

def square_chunk(chunk: list[int]) -> int:
    return sum(x * x for x in chunk)

proc = ProcessParallel(input=list(range(1, 13)),
                       func=square_chunk,
                       workers=3)
output = proc.run()  # [14, 77, 194]
```

### Side-Effect Process
```python
from f_core.processes.i_0_base import ProcessBase

class Logger(ProcessBase):
    def _run(self) -> None:
        print(f'{self.name} executed')

Logger(name='MyLogger').run()
```
