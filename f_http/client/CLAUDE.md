# Client

## Purpose
Static HTTP client for sending GET requests and returning parsed `Response` objects. Handles connection errors and JSON parse errors separately, preserving status and elapsed time even when JSON parsing fails.

## Public API

| Signature | Behavior |
|-----------|----------|
| `Client.get_json(url: str, params: dict[str, Any] = None, headers: dict[str, str] = None) -> Response` | Sends HTTP GET request. Returns `Response` with status, data, elapsed, and exception. Connection errors populate `exception` with all other fields as `None`. JSON parse errors preserve `status` and `elapsed` but set `data` to `None`. |
| `Factory: type` | Class attribute. Wired to `Factory` in `__init__.py`. |

## Inheritance
```
Client  (standalone static class, no base class)
```

| Base | Responsibility |
|------|----------------|
| *(none)* | Client is a standalone utility class with only static methods |

## Logging

Every `get_json()` call logs an INFO line with colored metadata:
- **Success**: `GET <url> <status_code> <elapsed>`
- **Error**: `GET <url> <exception>`

Colors: GET in cyan, URL in violet, status in green (2xx) or
red (error), elapsed in amber.

## Dependencies

| Import | Category | Used For |
|--------|----------|----------|
| `requests` | Third-party | HTTP GET request execution |
| `f_http.response.Response` | Internal | Return type wrapping status, data, elapsed, exception |
| `f_http.status.Status` | Internal | Wraps HTTP status code with validation (2xx = valid) |
| `f_log.get_log` | Internal | Module logger |
| `f_log.color_log.ColorLog` | Internal | ANSI coloring for log output |
| `typing.Any` | Stdlib | Type hints for params and data dicts |

## Usage

### Valid Request (200 OK)
```python
from f_http.client import Client

response = Client.get_json(url="https://jsonplaceholder.typicode.com/posts/1")
assert response                    # True (status 200, data present)
assert response.status.code == 200
assert response.status.name == 'OK'
assert response.data               # parsed JSON dict
```

### Invalid Request (404 Not Found)
```python
from f_http.client import Client

response = Client.get_json(url="https://jsonplaceholder.typicode.com/posts/999")
assert not response                 # False (status 404)
assert response.status.code == 404
assert response.status.name == 'NOT_FOUND'
assert not response.data            # no data for 404
```

### Using Factory
```python
from f_http.client import Client

valid = Client.Factory.valid()      # 200 response
invalid = Client.Factory.invalid()  # 404 response
```
