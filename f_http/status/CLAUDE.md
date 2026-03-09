# Status

## Purpose
Thin wrapper around Python's `http.HTTPStatus` with validation and a readable name. A Status is considered valid (truthy) only for 2xx success codes.

## Public API

| Signature | Behavior |
|-----------|----------|
| `Status(code: int \| None) -> None` | Wraps an HTTP status code. Sets `is_valid=True` for 200-299. Resolves name via `HTTPStatus`; falls back to `'UNKNOWN'`. |
| `code -> int \| None` | The raw HTTP status code (or `None`). |
| `name -> str` | Human-readable name from `HTTPStatus` (`'OK'`, `'NOT_FOUND'`, `'UNKNOWN'`). |
| `is_valid -> bool` | `True` if code is in range 200-299. Inherited from `Validatable`. |
| `__bool__() -> bool` | `True` if code is 2xx. Inherited from `Validatable`. |
| `__str__() -> str` | `'Code=200, Name=OK'` |
| `__repr__() -> str` | `'<Status: Name=OK>'`. Inherited from `HasName`. |

## Inheritance
```
Status -> HasName      (provides name property, __repr__)
       -> Validatable  (provides is_valid property, __bool__)
```

## Dependencies
- `f_core.mixins.validatable` — boolean validity via `is_valid` and `__bool__`
- `f_core.mixins.has.name` — `name` property and `__repr__`
- `http.HTTPStatus` — standard library enum for resolving code to name

## Usage
```python
from f_http.status import Status

# 200 OK — valid
status = Status(code=200)
assert status                    # True (2xx)
assert status.code == 200
assert status.name == 'OK'
assert str(status) == 'Code=200, Name=OK'

# 404 Not Found — invalid
status = Status(code=404)
assert not status                # False (not 2xx)
assert status.name == 'NOT_FOUND'

# Unknown code — invalid
status = Status(code=None)
assert not status
assert status.name == 'UNKNOWN'
```
