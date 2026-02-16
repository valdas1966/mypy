# Dictable

## Purpose

Generic mixin that wraps a `dict[K, V]` and exposes a dictionary-like public API. Provides key/value access, iteration, containment checks, update, and equality. Inherits size semantics (`__len__`, `__bool__`) from `Sizable`. Implements `__str__` directly (not via `Printable`).

## Public API

### Class Attributes

```python
Factory: type = None
```
Factory class for creating instances. Attached via `__init__.py`.

### Constructor

```python
def __init__(self, data: dict[K, V] = None) -> None
```
Stores `data` (or a new empty `dict`) as `_data`.

### Methods

```python
def keys(self) -> list[K]
```
Returns list of keys.

```python
def values(self) -> list[V]
```
Returns list of values.

```python
def items(self) -> list[tuple[K, V]]
```
Returns list of `(key, value)` tuples.

```python
def get(self, key: K, default: V = None) -> V
```
Returns value for `key`, or `default` if missing.

```python
def update(self, data: Union[dict[K, V], 'Dictable[K, V]']) -> None
```
Merges `data` into `_data`. Accepts a `dict` or another `Dictable`.

### Dunder Methods

```python
def __getitem__(self, key: K) -> V
```
`obj[key]` — raises `KeyError` if missing.

```python
def __setitem__(self, key: K, value: V) -> None
```
`obj[key] = value`.

```python
def __contains__(self, key: K) -> bool
```
`key in obj`.

```python
def __len__(self) -> int
```
`len(obj)` — satisfies `Sizable` contract.

```python
def __iter__(self) -> Iterator[K]
```
Iterates over keys.

```python
def __str__(self) -> str
```
Returns `str(self._data)`.

```python
def __eq__(self, other: 'Dictable[K, V]') -> bool
```
Compares `_data` dicts for equality. Returns `NotImplemented` for non-Dictable.

## Inheritance (Hierarchy)

```
Sized (collections.abc)
 └── Sizable (abstract __len__, provides __bool__)
      └── Dictable(Sizable, Generic[K, V])
```

| Base | Responsibility |
|------|----------------|
| `Sizable` | Abstract `__len__`, concrete `__bool__` |
| `Generic[K, V]` | Type parameterization for key/value types |

## Dependencies

| Import | Purpose |
|--------|---------|
| `typing.Generic`, `TypeVar`, `Iterator`, `Union` | Generics and type hints |
| `f_core.mixins.sizable.Sizable` | Base — size/bool semantics |

## Usage Example

```python
from f_core.mixins.dictable import Dictable

d = Dictable(data={'a': 1, 'b': 2, 'c': 3})
d['d'] = 4
print(d.keys())       # ['a', 'b', 'c', 'd']
print('a' in d)       # True
print(d.get('z', 0))  # 0
print(len(d))         # 4
```

### Using the Factory

```python
from f_core.mixins.dictable import Dictable

abc = Dictable.Factory.abc()  # {'a': 1, 'b': 2, 'c': 3}
print(abc.keys())             # ['a', 'b', 'c']
print(abc['b'])               # 2
```
