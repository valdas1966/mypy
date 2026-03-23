# HasRepr

## Purpose
Mixin that provides a standardized `__repr__` based on `__str__`.
One place to change the repr format for all classes in the codebase.

## Public API

### Dunder Methods
```python
def __repr__(self) -> str
```
Returns `<ClassName: str(self)>`.

## Inheritance (Hierarchy)
```
HasRepr (this class)
 └── HasName (inherits repr)
```

## Dependencies
None.

## Usage Example
```python
from f_core.mixins.has.repr import HasRepr

class MyClass(HasRepr):
    def __str__(self) -> str:
        return 'hello'

obj = MyClass()
repr(obj)  # '<MyClass: hello>'
```
