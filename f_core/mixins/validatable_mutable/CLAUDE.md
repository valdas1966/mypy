# ValidatableMutable

## Purpose

Mixin that extends `Validatable` with public methods to change the validation state at runtime. Use when an object's validity is determined or toggled after construction.

## Public API

### Class Attributes

```python
Factory: type | None = None
```
Factory class for creating instances. Attached via `__init__.py`.

### Constructor

```python
def __init__(self, is_valid: bool | None = None) -> None
```
Calls `super().__init__(is_valid=is_valid)`. Defaults to `None` (unset) if not provided.

### Methods

```python
def set_valid(self) -> None
```
Sets `_is_valid = True`.

```python
def set_invalid(self) -> None
```
Sets `_is_valid = False`.

### Dunder Methods

```python
def __bool__(self) -> bool
```
Inherited from `Validatable`. Returns `_is_valid`.

## Inheritance (Hierarchy)

```
Validatable
 └── ValidatableMutable
```

| Base | Responsibility |
|------|----------------|
| [`Validatable`](../validatable/CLAUDE.html) | Read-only validation state (`__bool__`) |

## Dependencies

| Import | Purpose |
|--------|---------|
| `f_core.mixins.validatable.main.Validatable` | Base class providing `__bool__` |

## Usage Example

```python
from f_core.mixins.validatable_mutable import ValidatableMutable


class Cell(ValidatableMutable):
    def __init__(self, row: int, col: int):
        ValidatableMutable.__init__(self, is_valid=True)
        self.row = row
        self.col = col


cell = Cell(0, 0)
if cell:             # True
    visit(cell)

cell.set_invalid()   # Mark as obstacle
if not cell:         # Now False
    skip(cell)

cell.set_valid()     # Reopen
```

### Using the Factory

```python
from f_core.mixins.validatable_mutable import ValidatableMutable

obj = ValidatableMutable.Factory.valid()
assert obj
obj.set_invalid()
assert not obj
```
