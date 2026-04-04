# ProcessParallel

## Purpose
Parallel process that splits a list of items into chunks, distributes
them across workers (threads or processes), and collects results.
Extends `ProcessIO[list[Item], list[Output | None]]`. Failed chunks
produce `None` in the output; errors are collected separately.

## Public API

### Type Parameters
```python
Item = TypeVar('Item')
Output = TypeVar('Output')
```

### Constructor
```python
def __init__(self,
             input: list[Item],
             func: Callable[[list[Item]], Output | None],
             workers: int,
             use_processes: bool = False,
             name: str = 'ProcessParallel') -> None
```
Stores `func`, clamps `workers` to `len(input)`, and delegates to
`ProcessIO.__init__`. Workers are set to `0` if input is empty.

### Properties
```python
@property
def errors(self) -> list[tuple[int, list[Item], Exception]]
```
Returns collected errors from failed chunks as
`(chunk_index, chunk_data, exception)` tuples.

### Inherited (from ProcessIO / ProcessBase)
```python
def run(self) -> list[Output | None]
@property
def input(self) -> list[Item]
@property
def elapsed(self) -> int
@property
def name(self) -> str
def seconds_since_last_call(self) -> int
def __str__(self) -> str
def __eq__(self, other: object) -> bool
def __lt__(self, other: object) -> bool
def __hash__(self) -> int
```

### Subclass Contract
Not intended for subclassing. Pass a `func` callable instead.

## Inheritance (Hierarchy)

```
Equatable
 └── Comparable
      └── HasName
           └── ProcessBase ─── run(), elapsed, recorder, timing
                ├── ProcessInput[list[Item]] ─── input property
                ├── ProcessOutput[list[Output | None]] ─── run() -> Output
                └── ProcessIO[list[Item], list[Output | None]]
                     └── ProcessParallel[Item, Output] ← this module
```

| Base | Responsibility |
|------|----------------|
| `ProcessIO` | Combines input + output, lifecycle |
| `ProcessInput` | `input` property |
| `ProcessOutput` | `run()` returns output |
| `ProcessBase` | Template Method lifecycle, timing, recording |
| `HasName` | `name` as `key`, comparison, hash |

## Dependencies

| Import | Purpose |
|--------|---------|
| `f_core.processes.i_2_io.ProcessIO` | Parent class |
| `f_ds.groups.Group` | `to_groups()` splits input into chunks |
| `concurrent.futures.ThreadPoolExecutor` | Thread-based parallelism |
| `concurrent.futures.ProcessPoolExecutor` | Process-based parallelism |
| `multiprocessing` | `get_context('forkserver')` on non-Windows |
| `sys` | Platform detection (`sys.platform`) |

## Usage Examples

### Thread-Based (I/O-Bound)
```python
from f_core.processes.i_3_parallel import ProcessParallel

def square_chunk(chunk: list[int]) -> int:
    return sum(x * x for x in chunk)

proc = ProcessParallel(input=list(range(1, 13)),
                       func=square_chunk,
                       workers=3)
output = proc.run()
print(output)          # [14, 77, 194]
print(proc.elapsed)    # seconds
print(proc.errors)     # []
```

### Process-Based (CPU-Bound)
```python
proc = ProcessParallel(input=list(range(1, 13)),
                       func=square_chunk,
                       workers=3,
                       use_processes=True)
output = proc.run()
```

### Error Tolerance
```python
def failing(chunk: list[int]) -> int:
    if 3 in chunk:
        raise ValueError('fail')
    return sum(chunk)

proc = ProcessParallel(input=list(range(1, 7)),
                       func=failing,
                       workers=3)
output = proc.run()
# Failed chunks → None, others succeed
for idx, chunk_data, exc in proc.errors:
    print(f'Chunk {idx}: {chunk_data} → {exc}')
```

### Factory
```python
from f_core.processes.i_3_parallel import ProcessParallel

proc = ProcessParallel.Factory.io_bound()
output = proc.run()
```
