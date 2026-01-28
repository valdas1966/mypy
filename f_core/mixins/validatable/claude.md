# Validatable Mixin Module

> **Location:** `f_core/mixins/validatable.py` + `validatable_public.py`
> **Purpose:** Mixin for objects with validation state (valid/invalid)

---

## Quick Reference

| Component | Description |
|-----------|-------------|
| `Validatable` | Read-only validation state |
| `ValidatablePublic` | Mutable validation state |
| Key Method | `__bool__()` for truthiness |
| State | `True`, `False`, or `None` |

---

## Architecture

```
Validatable
    │
    ├── __init__(is_valid)
    ├── __bool__() ────────── if obj: ...
    └── _is_valid (private)
         │
         └── ValidatablePublic
              ├── set_valid()
              └── set_invalid()
```

### Two Classes, Two Use Cases

| Class | Mutability | Use Case |
|-------|------------|----------|
| `Validatable` | Read-only | Validation fixed at creation |
| `ValidatablePublic` | Mutable | Validation changes at runtime |

---

## Files

| File | Purpose |
|------|---------|
| `validatable.py` | Base class (read-only) |
| `validatable_public.py` | Extended class (mutable) |

---

## Validatable Class

### Constructor

```python
def __init__(self, is_valid: bool = None) -> None
```

### Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `__bool__()` | `bool` | Returns `_is_valid` for truthiness |

### Truth Table

| `is_valid` | `bool(obj)` | Meaning |
|------------|-------------|---------|
| `True` | `True` | Valid/success |
| `False` | `False` | Invalid/failure |
| `None` | `False` | Uninitialized |

---

## ValidatablePublic Class

### Constructor

```python
def __init__(self, is_valid: bool = None) -> None
```

### Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `__bool__()` | `bool` | Inherited from Validatable |
| `set_valid()` | `None` | Set `_is_valid = True` |
| `set_invalid()` | `None` | Set `_is_valid = False` |

---

## Usage Examples

### Basic Truthiness

```python
from f_core.mixins.validatable import Validatable

class Response(Validatable):
    def __init__(self, status_code: int, data: dict):
        is_valid = status_code == 200 and data is not None
        Validatable.__init__(self, is_valid=is_valid)
        self.data = data

response = Response(200, {"result": "ok"})
if response:  # Calls __bool__()
    process(response.data)
```

### Mutable State

```python
from f_core.mixins.validatable_public import ValidatablePublic

class Cell(ValidatablePublic):
    def __init__(self, row: int, col: int):
        ValidatablePublic.__init__(self, is_valid=True)
        self.row = row
        self.col = col

cell = Cell(0, 0)
if cell:  # True - walkable
    visit(cell)

cell.set_invalid()  # Mark as obstacle
if not cell:  # Now False
    skip(cell)

cell.set_valid()  # Reopen
```

### Filtering

```python
# Filter valid items using truthiness
valid_cells = [cell for cell in grid.cells() if cell]
invalid_cells = [cell for cell in grid.cells() if not cell]
```

### Multi-Mixin Composition

```python
class Status(HasName, Printable, Validatable):
    def __init__(self, code: int):
        HasName.__init__(self, name=str(code))
        is_valid = code == 200
        Validatable.__init__(self, is_valid=is_valid)
```

---

## Classes Using Validatable

### With Validatable (Read-Only)

| Class | Module | Validation Logic |
|-------|--------|------------------|
| `Response` | `f_http/response` | status OK + data exists |
| `Status` | `f_http/status` | code == 200 |
| `ProcessABC` | `f_core/processes` | set during execution |
| `SolutionsPath` | `f_graph/old_path` | solutions found |

### With ValidatablePublic (Mutable)

| Class | Module | Use Case |
|-------|--------|----------|
| `CellMap` | `f_ds/grids/cell` | Grid obstacles |
| `SolutionAlgo` | `f_cs/solution` | Deferred validation |
| `Cell` | `f_ds/old_grids` | Legacy grid cells |

---

## Validation Flow

```
Object Created
      │
      ▼
is_valid set (True/False/None)
      │
      ▼
__bool__() called
      │
      ├── if obj: ...
      ├── filter(bool, items)
      └── any([obj1, obj2])
      │
      ▼
Control flow continues
```

---

## Design Patterns

1. **Single Responsibility** - Only manages validation state
2. **Separation of Concerns** - Read-only vs mutable variants
3. **Truthiness via `__bool__`** - Pythonic `if obj:` syntax
4. **None as Uninitialized** - Distinguishes "not set" from "invalid"
5. **Mixin Composition** - Works with any class hierarchy

---

## Dependencies

**Internal:** None

**External:** None (pure Python)

---

## Common Patterns

### Validation at Construction

```python
class Result(Validatable):
    def __init__(self, success: bool, error: str = None):
        Validatable.__init__(self, is_valid=success)
        self.error = error
```

### Validation from External State

```python
class Cell(ValidatablePublic):
    def __init__(self):
        ValidatablePublic.__init__(self, is_valid=True)

    def block(self):
        self.set_invalid()

    def unblock(self):
        self.set_valid()
```

### Combining with Other Mixins

```python
class Process(HasName, Validatable):
    def __init__(self, name: str):
        HasName.__init__(self, name=name)
        Validatable.__init__(self)  # None = not yet run

    def run(self):
        # After execution, validation determined
        self._is_valid = self._execute()
```
