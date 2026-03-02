# ProcessParallel Module

> **Location:** `f_core/processes/i_3_parallel`
> **Purpose:** Parallel process that distributes items across workers

---

## Quick Reference

| Component | Description |
|-----------|-------------|
| `ProcessParallel[Item, Output]` | Splits input into chunks, executes in parallel |
| `Factory` | Static factory for test instances |
| Inherits | [ProcessIO](../i_2_io/CLAUDE.md) |
| Pattern | Generic, tolerant (failed chunks produce `None`) |

---

## Architecture

```
ProcessABC ──── ../i_0_abc/
    ├── ProcessInput[Input] ── ../i_1_input/
    ├── ProcessOutput[Output] ── ../i_1_output/
    └── ProcessIO[Input, Output] ── ../i_2_io/
            └── ProcessParallel[Item, Output] ── (this module)
```

---

## Files

| File | Purpose |
|------|---------|
| `main.py` | Core `ProcessParallel` class |
| `_factory.py` | Factory with test instances |
| `_tester.py` | pytest unit tests |
| `_study.py` | Usage examples |
| `__init__.py` | Exports + Factory binding |

---

## Constructor

```python
ProcessParallel(input, func, workers, use_processes=False, name='ProcessParallel')
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `input` | `list[Item]` | required | Items to distribute |
| `func` | `Callable[[list[Item]], Output \| None]` | required | Worker function per chunk |
| `workers` | `int` | required | Number of parallel workers |
| `use_processes` | `bool` | `False` | `False`=threads, `True`=processes |
| `name` | `str` | `'ProcessParallel'` | Process name |

---

## Properties

| Property | Type | Description |
|----------|------|-------------|
| `input` | `list[Item]` | Read-only input data |
| `errors` | `list[tuple[int, list[Item], Exception]]` | (chunk_idx, chunk_data, exception) |
| `elapsed` | `int` | Execution time in seconds |

---

## Cross-Platform Behavior

| Platform | Threads (`use_processes=False`) | Processes (`use_processes=True`) |
|----------|--------------------------------|----------------------------------|
| **Linux** | Works | Works (forkserver context) |
| **macOS** | Works | Works (forkserver context) |
| **Windows** | Works | Works (spawn context) |

### Windows requirement for processes

On Windows, Python's `multiprocessing` uses `spawn` which re-imports the
main module. When using `use_processes=True`, the caller script **must**
wrap the entry point with `if __name__ == '__main__':`.

This is a Python-wide requirement on Windows, not specific to this class.
On macOS and Linux, no guard is needed — `forkserver` handles it.

```python
# Windows-safe script
from f_core.processes.i_3_parallel import ProcessParallel

def square_chunk(chunk: list[int]) -> int:
    return sum(x * x for x in chunk)

if __name__ == '__main__':
    proc = ProcessParallel(input=list(range(1, 13)),
                           func=square_chunk,
                           workers=3,
                           use_processes=True)
    output = proc.run()
    print(output)
```

---

## Error Tolerance

Failed chunks produce `None` in the output. Other chunks continue.
Errors are collected in `proc.errors` as `(chunk_idx, chunk_data, exception)`.

---

## Factory

| Method | Workers | Executor | Input | Purpose |
|--------|---------|----------|-------|---------|
| `io_bound()` | 3 | threads | `[1..12]` | Happy path, threads |
| `cpu_bound()` | 3 | processes | `[1..12]` | Happy path, processes |
| `with_error()` | 3 | threads | `[1..6]` | Error tolerance path |

---

## Dependencies

- [f_core.processes.i_2_io.ProcessIO](../i_2_io/CLAUDE.md)
- [f_ds.groups.Group](../../../f_ds/groups/) — chunking via `distribute()`
- `concurrent.futures.ThreadPoolExecutor`
- `concurrent.futures.ProcessPoolExecutor`
