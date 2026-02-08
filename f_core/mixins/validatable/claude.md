# Validatable

## Purpose

Mixin that adds a read-only boolean validation state to objects. The state is set at construction and exposed via `__bool__()`, enabling Pythonic truthiness checks (`if obj:`).

## Public API

### Class Attributes

```python
Factory: type | None = None
```
Factory class for creating instances. Attached via `__init__.py`.

### Constructor

```python
def __init__(self, is_valid: bool) -> None
```
Stores `is_valid` as the private attribute `_is_valid`.

### Dunder Methods

```python
def __bool__(self) -> bool
```
Returns `_is_valid`. Enables `if obj:`, `filter(bool, items)`, `any()`, `all()`.

## Inheritance (Hierarchy)

```
Validatable  (standalone mixin, no base class)
 └── ValidatableMutable  (direct subclass)
```

| Base | Responsibility |
|------|----------------|
| *(none)* | Validatable is a root mixin |

**Direct subclass:** [`ValidatableMutable`](../validatable_mutable/CLAUDE.html) (`f_core.mixins.validatable_mutable`)

## Dependencies

**Internal:** None

**External:** None (pure Python)

## Usage Example

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

### Using the Factory

```python
from f_core.mixins.validatable import Validatable

valid = Validatable.Factory.valid()    # Validatable(is_valid=True)
invalid = Validatable.Factory.invalid()  # Validatable(is_valid=False)

assert valid
assert not invalid
```
