# Response

## Purpose
Immutable result object returned by `Client.get_json()`. Wraps the HTTP status, parsed JSON data, elapsed time, and any exception message. Considered valid (truthy) when the status is 2xx and data is not `None`.

## Public API

| Signature | Behavior |
|-----------|----------|
| `Response(status: Status \| None, data: dict[str, Any] \| None, elapsed: float \| None, exception: str \| None = None) -> None` | Create a response. Valid when `bool(status)` is `True` and `data` is not `None`. |
| `status -> Status \| None` | The HTTP status wrapper (or `None` on connection failure). |
| `data -> dict[str, Any] \| None` | Parsed JSON body (or `None` on failure). |
| `elapsed -> float \| None` | Request round-trip time in seconds (or `None` on failure). |
| `exception -> str \| None` | Error message if the request failed (or `None`). |
| `__bool__() -> bool` | `True` if status is 2xx and data is not `None`. Inherited from `Validatable`. |
| `__str__() -> str` | `'Code=200, Data=True, Elapsed=0.1'` |

## Inheritance

```
Response -> Validatable (provides is_valid, __bool__)
```

| Base | Responsibility |
|------|----------------|
| `Validatable` | Stores `is_valid` flag, exposes `__bool__()` for truthiness checks |

## Dependencies

| Import | Purpose |
|--------|---------|
| `f_http.status.Status` | HTTP status wrapper with code, name, and 2xx validation |
| `f_core.mixins.validatable.Validatable` | Mixin providing immutable boolean validity |
| `typing.Any` | Type hint for response data values |

## Usage

### OK response (valid)
```python
from f_http.response import Response
from f_http.status import Status

status = Status(code=200)
response = Response(status=status,
                    data={'key': 'value'},
                    elapsed=0.1)
assert response                         # True (2xx + data)
assert response.status.code == 200
assert response.data == {'key': 'value'}
assert response.elapsed == 0.1
assert response.exception is None
```

### Not-found response (invalid)
```python
response = Response.Factory.not_found()
assert not response                     # False (404)
assert response.status.code == 404
assert response.data is None
```

### Unknown error response (invalid)
```python
response = Response.Factory.unknown()
assert not response                     # False (no status)
assert response.exception == 'Unknown error'
```
