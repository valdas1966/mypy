# ProcessABC Module

> **Location:** `f_core/processes/i_0_abc`
> **Purpose:** Abstract base class for processes with timing and lifecycle management

---

## Quick Reference

| Component | Description |
|-----------|-------------|
| `ProcessABC` | Base class for all processes |
| `Factory` | Static factory for test instances |
| Inherits | [HasName](../../mixins/has/name/claude.md), [Validatable](../../mixins/validatable/claude.md) |
| Pattern | Template Method (`run` → `_run_pre` → `_run` → `_run_post`) |

---

## Architecture

```
Equable ──────────────────── ../../mixins/equable/
 └── Comparable ───────────── ../../mixins/comparable/
      └── HasName ──────────── ../../mixins/has/name/
           │
           └── ProcessABC ──── (this module)
                │   ├── run()
                │   ├── _run_pre()
                │   ├── _run()
                │   ├── _run_post()
                │   ├── elapsed (property)
                │   └── seconds_since_last_call()
                │
                └── Validatable ── ../../mixins/validatable/
                     └── __bool__()
```

### What You Get

| From [HasName](../../mixins/has/name/claude.md) | From [Validatable](../../mixins/validatable/claude.md) | From ProcessABC |
|-------------------------------------------------|--------------------------------------------------------|-----------------|
| `name` property | `__bool__()` truthiness | `run()` lifecycle |
| `==`, `!=`, `<`, `>` | `_is_valid` state | `elapsed` timing |
| `hash()`, `str()`, `repr()` | | `seconds_since_last_call()` |

---

## Files

| File | Purpose |
|------|---------|
| `main.py` | Core `ProcessABC` class |
| `_factory.py` | Factory for test instances |
| `_study.py` | Usage examples |
| `__init__.py` | Exports + Factory binding |

---

## ProcessABC Class

### Constructor

```python
def __init__(self, name: str = 'ProcessABC') -> None
```

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `name` | `str` | Process name (from [HasName](../../mixins/has/name/claude.md)) |
| `elapsed` | `int \| None` | Total execution time in seconds |

### Timing Attributes (Private)

| Attribute | Type | Description |
|-----------|------|-------------|
| `_elapsed` | `int \| None` | Stored elapsed time |
| `_time_start` | `float \| None` | Start timestamp |
| `_time_finish` | `float \| None` | Finish timestamp |
| `_time_lap_prev` | `int \| None` | Previous lap checkpoint |

---

## Template Method Pattern

### Lifecycle Methods

```python
run()           # Main entry point - orchestrates lifecycle
  ├── _run_pre()    # Setup: reset timing, record start
  ├── _run()        # Main logic (override in subclass)
  └── _run_post()   # Cleanup: record finish, calculate elapsed
```

| Method | Purpose | Override? |
|--------|---------|-----------|
| `run()` | Entry point, orchestrates lifecycle | Rarely |
| `_run_pre()` | Setup, starts timer | Rarely |
| `_run()` | **Main process logic** | **Yes** |
| `_run_post()` | Cleanup, calculates elapsed | Rarely |

### Execution Flow

```
process.run()
    │
    ▼
_run_pre()
    ├── _elapsed = None
    └── _time_start = time.time()
    │
    ▼
_run()  ← Override this in subclass
    │
    ▼
_run_post()
    ├── _time_finish = time.time()
    └── _elapsed = int(_time_finish - _time_start)
    │
    ▼
process.elapsed  # Access total time
```

---

## Lap Timer

### `seconds_since_last_call() -> int`

Measures time between consecutive calls.

```python
process.seconds_since_last_call()  # Returns 0 (first call)
time.sleep(2)
process.seconds_since_last_call()  # Returns 2
time.sleep(3)
process.seconds_since_last_call()  # Returns 3
```

| Call | Returns | Action |
|------|---------|--------|
| First | `0` | Stores checkpoint |
| Subsequent | Seconds since last call | Updates checkpoint |

---

## Usage Examples

### Basic Subclass

```python
from f_core.processes.i_0_abc import ProcessABC

class MyProcess(ProcessABC):
    def _run(self) -> None:
        # Your process logic here
        self.do_work()

process = MyProcess(name='DataProcessor')
process.run()
print(f"Completed in {process.elapsed} seconds")
```

### With Lap Timer

```python
class TimedProcess(ProcessABC):
    def _run(self) -> None:
        print(self.seconds_since_last_call())  # 0

        self.step_one()
        print(self.seconds_since_last_call())  # Time for step 1

        self.step_two()
        print(self.seconds_since_last_call())  # Time for step 2
```

### Sorting Processes

```python
# From HasName - processes are sortable by name
processes = [
    MyProcess(name='Zebra'),
    MyProcess(name='Alpha'),
    MyProcess(name='Beta')
]
sorted(processes)  # [Alpha, Beta, Zebra]
```

### Validity Check

```python
# From Validatable
process = MyProcess(name='Test')
if process:  # Calls __bool__()
    process.run()
```

---

## Process Hierarchy

```
ProcessABC (i_0_abc) ← YOU ARE HERE
    │
    ├── ProcessInput[Input] (i_1_input)
    │       └── Adds: input property
    │
    ├── ProcessOutput[Output] (i_1_output)
    │       └── Adds: output, run() returns Output
    │
    └── ProcessIO[Input, Output] (i_2_io)
            └── Combines: input + output
```

### Naming Convention

| Prefix | Level | Description |
|--------|-------|-------------|
| `i_0_` | Base | Abstract base class |
| `i_1_` | Level 1 | Single capability (input OR output) |
| `i_2_` | Level 2 | Combined capabilities |

---

## Factory

```python
ProcessABC.Factory.nested()  # Creates example nested process
```

---

## Dependencies

**Inherits:**
- [f_core.mixins.has.name.HasName](../../mixins/has/name/claude.md)
- [f_core.mixins.validatable.Validatable](../../mixins/validatable/claude.md)

**Through HasName:**
- [f_core.mixins.comparable.Comparable](../../mixins/comparable/claude.md)
- [f_core.mixins.equable.Equable](../../mixins/equable/claude.md)

**Standard Library:**
- `time.time()` for timing

---

## Design Patterns

1. **Template Method** - `run()` orchestrates `_run_pre()`, `_run()`, `_run_post()`
2. **Mixin Composition** - Combines HasName + Validatable
3. **Factory Pattern** - `ProcessABC.Factory` for test instances
4. **Property Pattern** - `elapsed` wraps `_elapsed`

---

## Comparison with `process/` Module

| Aspect | ProcessABC (i_0_abc) | Process (process/) |
|--------|---------------------|-------------------|
| Timing | `time.time()` (seconds) | `perf_counter()` (ms) |
| Generic | Via subclasses | Built-in `[Input, Output]` |
| Architecture | Hierarchical | Flat/unified |
| Use Case | Teaching, explicit lifecycle | Production |
