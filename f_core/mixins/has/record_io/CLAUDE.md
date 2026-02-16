# HasRecordIO

## Purpose

Mixin for objects with separate input and output records. Creates two `HasRecord` instances on construction — one for tracking input data and one for output data.

## Public API

### Constructor

```python
def __init__(self, name: str = 'HasRecordIO') -> None
```
Calls `HasName.__init__` with `name`, creates `_record_input` and `_record_output` as empty `HasRecord` instances.

### Properties

```python
@property
def record_input(self) -> HasRecord
```
Returns the input record.

```python
@property
def record_output(self) -> HasRecord
```
Returns the output record.

## Inheritance (Hierarchy)

```
Equatable (abstract key, __eq__)
  ├── Comparable (@total_ordering, __lt__)
  └── Hashable (__hash__ via key)
       └── HasName(Comparable, Hashable)
            └── HasRecordIO(HasName)
```

| Base | Responsibility |
|------|----------------|
| `HasName` | `name` property, `key`, comparison, hashing, str/repr |

## Dependencies

| Import | Purpose |
|--------|---------|
| `f_core.mixins.has.HasRecord` | Input/output record instances |
| `f_core.mixins.has.HasName` | Base — name, comparison, hashing |

## Notes

- No `__init__.py` exists for this module (no Factory wiring).
- The `_factory.py` exists but is incomplete (`Factory.proc()` never returns a value and passes an invalid `verbose` kwarg to `HasRecordIO.__init__`).

## Usage Example

```python
from f_core.mixins.has.record_io.main import HasRecordIO

proc = HasRecordIO(name='MyProcess')
print(proc.name)                  # 'MyProcess'
print(proc.record_input.record)   # {}
print(proc.record_output.record)  # {}
```
