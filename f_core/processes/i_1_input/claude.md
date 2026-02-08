# ProcessInput Module

> **Location:** `f_core/processes/i_1_input`
> **Purpose:** Generic process with input parameter

---

## Quick Reference

| Component | Description |
|-----------|-------------|
| `ProcessInput[Input]` | Generic process with typed input |
| `Factory` | Static factory for test instances |
| Inherits | [ProcessABC](../i_0_abc/claude.md) |
| Pattern | Generic TypeVar for input typing |

---

## Architecture

```
Equable ──────────────────── ../../mixins/equable/
 └── Comparable ───────────── ../../mixins/comparable/
      └── HasName ──────────── ../../mixins/has/name/
           │
           └── ProcessABC ──── ../i_0_abc/
                │   ├── run()
                │   ├── elapsed (property)
                │   └── seconds_since_last_call()
                │
                └── ProcessInput[Input] ──── (this module)
                     └── input (property)
```

### What You Get

| From [ProcessABC](../i_0_abc/claude.md) | From ProcessInput |
|-----------------------------------------|-------------------|
| `run()` lifecycle | `input` property |
| `elapsed` timing | Generic `Input` type |
| `name` property | Type-safe input access |
| `==`, `!=`, `<`, `>` | |

---

## Files

| File | Purpose |
|------|---------|
| `main.py` | Core `ProcessInput[Input]` class |
| `_factory.py` | Factory for test instances |
| `_study.py` | Usage examples |
| `__init__.py` | Exports + Factory binding |

---

## ProcessInput Class

### Type Parameter

```python
Input = TypeVar('Input')  # Generic input type
```

### Constructor

```python
def __init__(self, input: Input, name: str = 'Process Input') -> None
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `input` | `Input` | *required* | The input data for the process |
| `name` | `str` | `'Process Input'` | Process name |

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `input` | `Input` | Read-only access to the input data |
| `name` | `str` | Process name (from [ProcessABC](../i_0_abc/claude.md)) |
| `elapsed` | `int \| None` | Execution time (from [ProcessABC](../i_0_abc/claude.md)) |

### Private Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `_input` | `Input` | Stored input data |

---

## Usage Examples

### Basic Subclass

```python
from f_core.processes.i_1_input import ProcessInput

class DataLoader(ProcessInput[str]):
    def _run(self) -> None:
        # Access typed input
        filepath = self.input
        self.load_file(filepath)

loader = DataLoader(input='/path/to/data.csv', name='CSV Loader')
loader.run()
print(f"Loaded from: {loader.input}")
print(f"Elapsed: {loader.elapsed} seconds")
```

### With Integer Input

```python
class Calculator(ProcessInput[int]):
    def _run(self) -> None:
        result = self.input * 2
        print(f"Input {self.input} doubled = {result}")

calc = Calculator(input=5, name='Doubler')
calc.run()  # Output: Input 5 doubled = 10
```

### With Complex Input

```python
from dataclasses import dataclass

@dataclass
class Config:
    path: str
    batch_size: int

class ConfiguredProcess(ProcessInput[Config]):
    def _run(self) -> None:
        print(f"Path: {self.input.path}")
        print(f"Batch: {self.input.batch_size}")

config = Config(path='/data', batch_size=32)
process = ConfiguredProcess(input=config, name='Configured')
process.run()
```

---

## Factory

```python
# Get the factory-created class
A = ProcessInput.Factory.a()

# Instantiate with input
proc = A(input=1)
proc.run()
print(proc.input)  # 1
```

### Factory.a()

Returns a concrete `ProcessInput[int]` subclass with:
- `RECORD_SPEC` for logging
- Verbose mode enabled
- Name preset to `'A'`

```python
@staticmethod
def a() -> type[ProcessInput]:
    class A(ProcessInput[int]):
        RECORD_SPEC = {'input': lambda o: o.input}
        def __init__(self, input: int):
            ProcessInput.__init__(self, input=input, verbose=True, name='A')
    return A
```

---

## Process Hierarchy

```
ProcessABC (i_0_abc)
    │
    ├── ProcessInput[Input] (i_1_input) ← YOU ARE HERE
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

## Dependencies

**Inherits:**
- [f_core.processes.i_0_abc.ProcessABC](../i_0_abc/claude.md)

**Through ProcessABC:**
- [f_core.mixins.has.name.HasName](../../mixins/has/name/claude.md)
- [f_core.mixins.validatable.Validatable](../../mixins/validatable/claude.md)
- [f_core.mixins.comparable.Comparable](../../mixins/comparable/claude.md)
- [f_core.mixins.equable.Equable](../../mixins/equatable/claude.md)

**Standard Library:**
- `typing.Generic` for generic typing
- `typing.TypeVar` for type variable

---

## Design Patterns

1. **Generic Programming** - `ProcessInput[Input]` uses TypeVar for type safety
2. **Template Method** - Inherits `run()` lifecycle from ProcessABC
3. **Factory Pattern** - `ProcessInput.Factory` for test instances
4. **Property Pattern** - `input` wraps `_input`

---

## Comparison with ProcessOutput

| Aspect | ProcessInput | ProcessOutput |
|--------|--------------|---------------|
| Type Parameter | `Input` | `Output` |
| Direction | Data flows **in** | Data flows **out** |
| Property | `input` (read-only) | `output` (set in `_run`) |
| `run()` return | `None` | `Output` |
