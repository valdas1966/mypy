# FetchBase

## Purpose
Shared configuration and helper methods for TikTok RapidAPI access.
Holds HOST, KEY, HEADERS and provides `_get_response`, `_on_error`,
`_on_broken`, and `_stamp` used by both `FetchSingle` and `FetchMulti`.

## Public API

| Method | Signature | Description |
|--------|-----------|-------------|
| `_get_response` | `(url: str, params: dict) -> Response` | HTTP GET with API headers |
| `_on_error` | `(status: Status, anchor: tuple) -> dict` | Error dict on bad response |
| `_on_broken` | `(msg: str, anchor: tuple) -> dict` | Error dict on exception |
| `_stamp` | `(row: dict) -> dict` | Add `is_ok`/`is_broken` defaults |

## Inheritance
No base class (root of the fetch hierarchy).

## Dependencies
- `f_http` (Client, Response, Status)
- `f_utils.u_file`, `f_psl.sys.utils`, `f_os.u_environ`

## Usage Example
```python
from f_proj.rapid_api.tiktok.fetch.i_0_base import FetchBase

row = FetchBase._stamp({'id_user': '123'})
# {'id_user': '123', 'is_ok': True, 'is_broken': False}

error = FetchBase._on_error(status=Status(404),
                            anchor=('id_user', '123'))
# {'status_code': 404, 'is_ok': False, 'id_user': '123'}
```
