# ProcessOutput Module

> **Location:** `f_core/processes/i_1_output`
> **Purpose:** Generic process that produces typed output

---

## Quick Reference

| Component | Description |
|-----------|-------------|
| `ProcessOutput[Output]` | Generic process with typed output |
| `Factory` | Static factory for test instances |
| Inherits | [ProcessABC](../i_0_abc/claude.md) |
| Pattern | Generic TypeVar for output typing |

---

## Architecture

```
Equable ──────────────────── ../../mixins/equable/
 └── Comparable ───────────── ../../mixins/comparable/
      └── HasName ──────────── ../../mixins/has/name/
           │
           └── ProcessABC ──── ../i_0_abc/
                │   ├── run() → None
                │   ├── elapsed (property)
                │   └── seconds_since_last_call()
                │
                └── ProcessOutput[Output] ──── (this module)
                     ├── run() → Output  ← OVERRIDES
                     └── _output (attribute)
```

### What You Get

| From [ProcessABC](../i_0_abc/claude.md) | From ProcessOutput |
|-----------------------------------------|-------------------|
| `_run()` lifecycle | `run()` returns `Output` |
| `elapsed` timing | `_output` attribute |
| `name` property | Generic `Output` type |
| `==`, `!=`, `<`, `>` | |

---

## Files

| File | Purpose |
|------|---------|
| `main.py` | Core `ProcessOutput[Output]` class |
| `_factory.py` | Factory for test instances |
| `_study.py` | Usage examples |
| `__init__.py` | Exports + Factory binding |

---

## ProcessOutput Class

### Type Parameter

```python
Output = TypeVar('Output')  # Generic output type
```

### Constructor

```python
def __init__(self, name: str = 'ProcessOutput') -> None
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `name` | `str` | `'ProcessOutput'` | Process name |

### Key Override: `run()`

```python
def run(self) -> Output:
    self._run_pre()
    self._run()
    self._run_post()
    return self._output  # ← Returns output!
```

**Important:** Unlike `ProcessABC.run()` which returns `None`, `ProcessOutput.run()` returns the computed output.

### Private Attributes

| Attribute | Type | Set By | Description |
|-----------|------|--------|-------------|
| `_output` | `Output \| None` | `_run()` | The computed output (set in subclass) |

---

## Usage Examples

### Basic Subclass

```python
from f_core.processes.i_1_output import ProcessOutput

class DataGenerator(ProcessOutput[list[int]]):
    def _run(self) -> None:
        # Set _output in your implementation
        self._output = [1, 2, 3, 4, 5]

generator = DataGenerator(name='Number Generator')
result = generator.run()  # Returns [1, 2, 3, 4, 5]
print(f"Generated: {result}")
print(f"Elapsed: {generator.elapsed} seconds")
```

### With String Output

```python
class Greeter(ProcessOutput[str]):
    def __init__(self, greeting: str, name: str = 'Greeter'):
        self._greeting = greeting
        super().__init__(name=name)

    def _run(self) -> None:
        self._output = f"Hello, {self._greeting}!"

greeter = Greeter(greeting='World')
message = greeter.run()  # Returns "Hello, World!"
```

### With Complex Output

```python
from dataclasses import dataclass

@dataclass
class Report:
    title: str
    data: list[float]
    success: bool

class ReportGenerator(ProcessOutput[Report]):
    def _run(self) -> None:
        self._output = Report(
            title='Analysis',
            data=[1.0, 2.5, 3.7],
            success=True
        )

gen = ReportGenerator(name='Report Gen')
report = gen.run()
print(report.title)  # 'Analysis'
```

---

## Factory

```python
# Get a pre-configured instance
proc = ProcessOutput.Factory.a()
result = proc.run()
print(result)  # 1
```

### Factory.a()

Returns a `ProcessOutput[int]` instance that outputs `1`:

```python
@staticmethod
def a() -> ProcessOutput[int]:
    class A(ProcessOutput[int]):
        RECORD_SPEC = {'output': lambda o: o._output}
        def __init__(self):
            ProcessOutput.__init__(self, verbose=True, name='A')
        def _run(self) -> int:
            self._output = 1
    return A()  # Note: returns instance, not class
```

---

## Process Hierarchy

```
ProcessABC (i_0_abc)
    │
    ├── ProcessInput[Input] (i_1_input)
    │       └── Adds: input property
    │
    ├── ProcessOutput[Output] (i_1_output) ← YOU ARE HERE
    │       └── Adds: _output, run() returns Output
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

1. **Generic Programming** - `ProcessOutput[Output]` uses TypeVar for type safety
2. **Template Method** - Inherits lifecycle, overrides `run()` return
3. **Factory Pattern** - `ProcessOutput.Factory` for test instances
4. **Output Capture** - `_output` set in `_run()`, returned by `run()`

---

## Comparison with ProcessInput

| Aspect | ProcessInput | ProcessOutput |
|--------|--------------|---------------|
| Type Parameter | `Input` | `Output` |
| Direction | Data flows **in** | Data flows **out** |
| Access | `input` property (read-only) | `_output` attribute (set in `_run`) |
| Constructor | Takes `input` parameter | No input parameter |
| `run()` return | `None` | `Output` |
