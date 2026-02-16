# HasRecord

## Purpose

Mixin for objects that can be converted to a flat record (dict). Uses a class-variable `RECORD_SPEC` to define field names and getter functions. Supports MRO-based spec merging so subclasses automatically inherit and extend parent fields. Also provides verbose colored console output.

## Public API

### Class Attributes

```python
Factory = None
```
Factory class for creating instances. Attached via `__init__.py`.

```python
RECORD_SPEC: ClassVar[dict[str, RecordGetter]] = {'name': lambda o: o.name}
```
Maps field names to getter callables. Subclasses override to add fields.

### Constructor

```python
def __init__(self, name: str = None, verbose: bool = False) -> None
```
Calls `HasName.__init__` with `name`, stores `_verbose`.

### Properties

```python
@property
def verbose(self) -> bool
```
Returns the verbose flag.

```python
@property
def record(self) -> dict[str, Any]
```
Returns `{field: value}` dict, excluding fields where the getter returns `None`. Uses `_record_spec()` for MRO-merged fields.

### Methods

```python
def str_record(self) -> str
```
Returns `'[Key=value] [Key=value] ...'` string representation of the record, excluding the `'name'` field. Returns empty string if no fields.

```python
def print(self, msg: str = str()) -> None
```
Prints a timestamped, colored message if `verbose` is `True`. Format: `[HH:MM:SS] [name] msg`.

```python
@staticmethod
def spec(**fields: RecordGetter) -> dict[str, RecordGetter]
```
Helper for nicer `RECORD_SPEC` syntax in subclasses. Returns `fields` as a dict.

```python
@classmethod
def header_record(cls) -> list[str]
```
Returns ordered list of field names (for CSV headers, tables, etc.).

```python
@classmethod
def _record_spec(cls) -> dict[str, RecordGetter]
```
Internal: merges `RECORD_SPEC` from all classes in MRO (reversed order so subclass wins).

## Inheritance (Hierarchy)

```
Equatable (abstract key, __eq__)
  ├── Comparable (@total_ordering, __lt__)
  └── Hashable (__hash__ via key)
       └── HasName(Comparable, Hashable)
            └── HasRecord(HasName)
```

| Base | Responsibility |
|------|----------------|
| `HasName` | `name` property, `key`, comparison, hashing, str/repr |

## Dependencies

| Import | Purpose |
|--------|---------|
| `__future__.annotations` | Postponed evaluation of annotations |
| `f_core.mixins.has.name.HasName` | Base — name, comparison, hashing |
| `typing.Any`, `Callable`, `ClassVar` | Type hints |
| `f_utils.u_datetime` | Timestamp for verbose print |
| `enum.Enum` | `Color` enum for ANSI codes |

## Usage Example

```python
from f_core.mixins.has.record import HasRecord

a = HasRecord.Factory.a()   # A(HasRecord) with a=1
b = HasRecord.Factory.b()   # B(A) with a=1, b=2

print(a.record)             # {'name': 'A', 'a': 1}
print(b.record)             # {'name': 'B', 'a': 1, 'b': 2}
print(b.str_record())       # '[A=1] [B=2]'
print(b.header_record())    # ['name', 'a', 'b']
```
