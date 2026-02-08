# ProcessIO Module

> **Location:** `f_core/processes/i_2_io`
> **Purpose:** Generic process combining input and output capabilities

---

## Quick Reference

| Component | Description |
|-----------|-------------|
| `ProcessIO[Input, Output]` | Generic process with both input and output |
| `Factory` | Static factory for test instances |
| Inherits | [ProcessInput](../i_1_input/claude.md), [ProcessOutput](../i_1_output/claude.md) |
| Pattern | Multiple inheritance combining both capabilities |

---

## Architecture

```
ProcessABC ────────────────── ../i_0_abc/
    │
    ├── ProcessInput[Input] ── ../i_1_input/
    │       └── input property
    │
    ├── ProcessOutput[Output] ── ../i_1_output/
    │       └── run() → Output
    │
    └── ProcessIO[Input, Output] ──── (this module)
            ├── input property (from ProcessInput)
            └── run() → Output (from ProcessOutput)
```

### What You Get

| From [ProcessInput](../i_1_input/claude.md) | From [ProcessOutput](../i_1_output/claude.md) | Combined |
|---------------------------------------------|----------------------------------------------|----------|
| `input` property | `run()` returns `Output` | Both capabilities |
| Generic `Input` type | `_output` attribute | Two type parameters |
| | Generic `Output` type | Full I/O process |

---

## Files

| File | Purpose |
|------|---------|
| `main.py` | Core `ProcessIO[Input, Output]` class |
| `_factory.py` | Factory for test instances |
| `_study.py` | Usage examples |
| `__init__.py` | Exports + Factory binding |

---

## ProcessIO Class

### Type Parameters

```python
Input = TypeVar('Input')    # Generic input type
Output = TypeVar('Output')  # Generic output type
```

### Constructor

```python
def __init__(self, input: Input, name: str = 'ProcessIO') -> None
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `input` | `Input` | *required* | The input data for the process |
| `name` | `str` | `'ProcessIO'` | Process name |

### Properties

| Property | Type | Source | Description |
|----------|------|--------|-------------|
| `input` | `Input` | ProcessInput | Read-only access to input data |
| `name` | `str` | ProcessABC | Process name |
| `elapsed` | `int \| None` | ProcessABC | Execution time in seconds |

### Private Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `_input` | `Input` | Stored input data |
| `_output` | `Output \| None` | Computed output (set in `_run`) |

### run() Method

```python
def run(self) -> Output:
    return ProcessOutput.run(self)
```

Delegates to `ProcessOutput.run()` which returns the output.

---

## Usage Examples

### Basic Subclass

```python
from f_core.processes.i_2_io import ProcessIO

class Doubler(ProcessIO[int, int]):
    def _run(self) -> None:
        self._output = self.input * 2

doubler = Doubler(input=5, name='Doubler')
result = doubler.run()  # Returns 10
print(f"Input: {doubler.input}, Output: {result}")
```

### String Transformation

```python
class UpperCase(ProcessIO[str, str]):
    def _run(self) -> None:
        self._output = self.input.upper()

proc = UpperCase(input='hello', name='UpperCase')
result = proc.run()  # Returns 'HELLO'
```

### Different Input/Output Types

```python
class Parser(ProcessIO[str, list[int]]):
    def _run(self) -> None:
        self._output = [int(x) for x in self.input.split(',')]

parser = Parser(input='1,2,3,4,5', name='Parser')
result = parser.run()  # Returns [1, 2, 3, 4, 5]
```

### With Complex Types

```python
from dataclasses import dataclass

@dataclass
class Config:
    path: str
    batch_size: int

@dataclass
class Result:
    success: bool
    count: int

class DataProcessor(ProcessIO[Config, Result]):
    def _run(self) -> None:
        # Access typed input
        config = self.input

        # Produce typed output
        self._output = Result(
            success=True,
            count=config.batch_size * 10
        )

config = Config(path='/data', batch_size=32)
processor = DataProcessor(input=config, name='Processor')
result = processor.run()
print(result.count)  # 320
```

---

## Factory

```python
# Get the factory-created class
Square = ProcessIO.Factory.square()

# Instantiate with input
proc = Square(input=4)
result = proc.run()  # Returns 16 (4 * 4)
```

### Factory.square()

Returns a `ProcessIO[int, int]` class that squares its input:

```python
@staticmethod
def square() -> type[ProcessIO[int, int]]:
    class Square(ProcessIO[int, int]):
        RECORD_SPEC = {
            'input': lambda o: o.input,
            'output': lambda o: o._output
        }
        def __init__(self, name='Square', verbose=True, input=input) -> None:
            ProcessIO.__init__(self, name=name, verbose=verbose, input=input)
        def _run(self) -> None:
            self._output = self.input * self.input
    return Square
```

---

## Process Hierarchy

```
ProcessABC (i_0_abc)
    │
    ├── ProcessInput[Input] (i_1_input)
    │       └── Adds: input property
    │
    ├── ProcessOutput[Output] (i_1_output)
    │       └── Adds: _output, run() returns Output
    │
    └── ProcessIO[Input, Output] (i_2_io) ← YOU ARE HERE
            └── Combines: input + output
```

### Multiple Inheritance

```python
class ProcessIO(Generic[Input, Output],
                ProcessInput[Input],
                ProcessOutput[Output]):
```

ProcessIO uses **multiple inheritance** to combine both capabilities.

### Naming Convention

| Prefix | Level | Description |
|--------|-------|-------------|
| `i_0_` | Base | Abstract base class |
| `i_1_` | Level 1 | Single capability (input OR output) |
| `i_2_` | Level 2 | Combined capabilities |

---

## Dependencies

**Inherits:**
- [f_core.processes.i_1_input.ProcessInput](../i_1_input/claude.md)
- [f_core.processes.i_1_output.ProcessOutput](../i_1_output/claude.md)

**Through parents:**
- [f_core.processes.i_0_abc.ProcessABC](../i_0_abc/claude.md)
- [f_core.mixins.has.name.HasName](../../mixins/has/name/claude.md)
- [f_core.mixins.validatable.Validatable](../../mixins/validatable/claude.md)
- [f_core.mixins.comparable.Comparable](../../mixins/comparable/claude.md)
- [f_core.mixins.equable.Equable](../../mixins/equatable/claude.md)

**Standard Library:**
- `typing.Generic` for generic typing
- `typing.TypeVar` for type variables

---

## Design Patterns

1. **Multiple Inheritance** - Combines ProcessInput and ProcessOutput
2. **Generic Programming** - `ProcessIO[Input, Output]` with two type variables
3. **Template Method** - Inherits lifecycle from ProcessABC
4. **Factory Pattern** - `ProcessIO.Factory` for test instances

---

## Comparison Summary

| Class | Type Params | Has `input` | `run()` returns |
|-------|-------------|-------------|-----------------|
| ProcessABC | None | No | `None` |
| ProcessInput | `[Input]` | Yes | `None` |
| ProcessOutput | `[Output]` | No | `Output` |
| **ProcessIO** | `[Input, Output]` | **Yes** | **`Output`** |
