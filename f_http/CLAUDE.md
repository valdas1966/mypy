# f_http

## Purpose
HTTP client infrastructure package. Provides a static GET client that returns
structured response objects with status validation, parsed JSON data, timing,
and error capture. Includes a standalone URL utility for extracting file
suffixes from CDN-style URLs.

## Public API

### Client
| Signature | Behavior |
|-----------|----------|
| `Client.get_json(url: str, params: dict[str, Any] = None, headers: dict[str, str] = None) -> Response` | Sends HTTP GET request. Returns `Response` with status, data, elapsed, and exception. Handles connection and JSON parse errors separately. |

### Status
| Signature | Behavior |
|-----------|----------|
| `Status(code: int) -> None` | Wraps HTTP status code. Valid (truthy) for 2xx codes only. Resolves name via `HTTPStatus`; unknown codes get `'UNKNOWN'`. |
| `code -> int` | Raw HTTP status code. |
| `name -> str` | Human-readable name (`'OK'`, `'NOT_FOUND'`, `'UNKNOWN'`). |
| `__bool__() -> bool` | `True` if 2xx. |
| `__str__() -> str` | `'Code=200, Name=OK'`. |

### Response
| Signature | Behavior |
|-----------|----------|
| `Response(status: Status, data: dict[str, Any], elapsed: float, exception: str = None) -> None` | Result of an HTTP request. Valid when `bool(status)` and `data is not None`. |
| `status -> Status` | HTTP status wrapper. |
| `data -> dict` | Parsed JSON body (or `None`). |
| `elapsed -> float` | Round-trip time in seconds. |
| `exception -> str` | Error message if request failed (or `None`). |
| `__bool__() -> bool` | `True` if status is 2xx and data exists. |

### URL
| Signature | Behavior |
|-----------|----------|
| `URL(url: str) -> None` | Wraps a URL string. |
| `suffix() -> str \| None` | Extracts file extension without dot. Tries path first, then `mime_type`/`mimeType` query param. |

## Inheritance

```
Client          (standalone static class)
Status    -> HasName, Validatable
Response  -> Validatable
URL             (standalone class)
```

Client produces Response objects. Response wraps a Status object.
URL is independent of the other three classes.

## Dependencies

| Import | Purpose |
|--------|---------|
| `requests` | Third-party HTTP library for GET requests |
| `http.HTTPStatus` | Stdlib enum for resolving status codes to names |
| `urllib.parse` | Stdlib URL parsing (`urlparse`, `parse_qs`) |
| `f_core.mixins.validatable` | Mixin providing `is_valid` and `__bool__()` |
| `f_core.mixins.has.name` | Mixin providing `name` property and `__repr__()` |

## Usage

### Typical workflow: fetch JSON and check result
```python
from f_http import Client

response = Client.get_json(url='https://api.example.com/posts/1')
if response:
    print(response.data)           # parsed JSON dict
    print(response.elapsed)        # e.g. 0.15
else:
    print(response.status.code)    # e.g. 404
    print(response.exception)      # error message or None
```

### Check status details
```python
from f_http import Status

status = Status(code=200)
assert status                      # True (2xx)
assert status.name == 'OK'
assert str(status) == 'Code=200, Name=OK'
```

### Extract file suffix from URL
```python
from f_http import URL

url = URL(url='https://cdn.example.com/video.mp4')
assert url.suffix() == 'mp4'

# Works with mime_type query param too
url = URL(url='https://cdn.example.com/stream?mime_type=video_mp4')
assert url.suffix() == 'mp4'
```
