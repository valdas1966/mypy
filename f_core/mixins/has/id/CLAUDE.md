# HasId

## Purpose

Mixin that assigns a unique nano-precision birth timestamp (`id_birth`) to every instance upon creation. Optionally carries `id_group` and `id_counter` metadata for grouping and ordering.

## Public API

### Constructor

```python
def __init__(self, id_group: str = None, id_counter: int = None) -> None
```
Generates `_id_birth` via `UDateTime.str_now(UDateTime.Format.NANO)`. Stores `id_group` and `id_counter`.

### Properties

```python
@property
def id_birth(self) -> str
```
Returns the nano-precision birth timestamp string.

```python
@property
def id_group(self) -> str
```
Returns the group identifier (can be `None`).

```python
@property
def id_counter(self) -> int
```
Returns the counter value (can be `None`).

## Inheritance (Hierarchy)

```
HasId (plain class, no mixin bases)
```

## Dependencies

| Import | Purpose |
|--------|---------|
| `f_psl.datetime.UDateTime` | Generates nano-precision timestamp for `id_birth` |

## Usage Example

```python
from f_core.mixins.has.id import HasId

a = HasId()
b = HasId()
print(a.id_birth)  # e.g. '2026-02-16 12:00:00.123456789'
print(b.id_birth)  # different timestamp

c = HasId(id_group='batch_1', id_counter=42)
print(c.id_group)    # 'batch_1'
print(c.id_counter)  # 42
```
