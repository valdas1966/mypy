# Sizable

## Purpose
Mixin for objects that have a measurable length (size).
Extends `collections.abc.Sized` and requires subclasses to implement
`__len__`. Provides a default `__bool__` that returns `True` when the
object is non-empty.

## Public API

### Abstract Method
```python
@abstractmethod
def __len__(self) -> int:
```
Return the object's length. Must be implemented by every subclass.

### Dunder Methods
```python
def __bool__(self) -> bool:
```
Returns `True` if `len(self) != 0`. Delegates to `__len__`.

## Inheritance (Hierarchy)

```
Sized (collections.abc)
 └── Sizable
```

| Base    | Responsibility                                     |
|---------|----------------------------------------------------|
| `Sized` | ABC that requires `__len__`; enables `len()` calls |

## Dependencies

| Import                        | Purpose                             |
|-------------------------------|-------------------------------------|
| `collections.abc.Sized`       | Base ABC providing the `__len__` contract |
| `abc.abstractmethod`          | Marks `__len__` as abstract         |

## Usage Example

```python
from f_core.mixins.sizable import Sizable


class Items(Sizable):
    def __init__(self, data: list) -> None:
        self._data = data

    def __len__(self) -> int:
        return len(self._data)


items = Items([1, 2, 3])
len(items)    # 3
bool(items)   # True

empty = Items([])
len(empty)    # 0
bool(empty)   # False
```
