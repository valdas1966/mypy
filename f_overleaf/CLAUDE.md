# OverLeaf

## Purpose
Client wrapper for OverLeaf (online LaTeX editor).
Inherits from `Dictable[str, ProjectOverLeaf]` — projects are
accessed by name via `overleaf['Project Name']`.

## Public API

### `__init__(api: pyoverleaf.Api) -> None`
Create an OverLeaf client with an authenticated pyoverleaf Api.
Eagerly loads all projects into the internal dict.

### `create_project(name: str) -> ProjectOverLeaf`
Create a blank Overleaf project, add it to the internal dict, and
return it. Raises `ValueError` if a project with the same name
already exists. Internally `POST`s `/project/new` with a CSRF
token pulled from the project-dashboard page; `pyoverleaf` does
not wrap this endpoint, so we use its session/host directly.

### `delete_project(name: str) -> None`
Delete an existing Overleaf project and remove it from the
internal dict. Raises `KeyError` if no such project. Internally
`DELETE`s `/project/<id>` with a fresh CSRF token. The project
is moved to Overleaf's Trash (server-side soft-delete); not
recoverable through this API.

### `rename_project(name: str, name_new: str) -> None`
Rename an existing project in place, preserving its id / URL /
history. Raises `KeyError` if `name` is missing, `ValueError` if
`name_new` already exists. Internally `POST`s
`/project/<id>/rename` with `{newProjectName}` and a fresh CSRF
token (same session/host pattern as `create_project`); updates the
internal dict key.

### `tag_project(project_name: str, tag_name: str) -> None`
Apply a tag (visible as a "folder" in the Overleaf sidebar) to
a project. The tag is created if it does not yet exist. Issues
one dashboard `GET` (CSRF + existing tags), optionally one
`POST /tag` (create), then `POST /tag/<tid>/project/<pid>`
(apply). Idempotent re-application is harmless.

### Inherited from Dictable
- `overleaf['Name']` — get project by name
- `overleaf.keys()` — all project names
- `overleaf.values()` — all ProjectOverLeaf objects
- `len(overleaf)` — number of projects
- `'Name' in overleaf` — check if project exists

### `close() -> None` + context manager (`__enter__`/`__exit__`)
Explicit teardown hook. pyoverleaf keeps **no** long-lived
connection (each HTTP call builds a throwaway `requests.Session`),
and the realtime socket.io connections are closed at the source in
`ProjectOverLeaf._root` — so there is no persistent handle to
release; `close()` forces a GC sweep to reap any stray socket
objects. Use `with OverLeaf.Factory.valdas() as ol:` to guarantee
close on block exit.

## Online-Presence Note — realtime sockets must be closed
Overleaf shows a client as an online "me" collaborator for every
open **socket.io** realtime connection. Upstream
`pyoverleaf.Api.project_get_files` opens such a socket per call and
**never closes it**, so each file op leaked a phantom online
viewer (a single push spawned dozens). `ProjectOverLeaf._root`
reimplements that read and closes the socket in `finally` — keeping
at most one transient connection open at a time and none behind.

## Inheritance (Hierarchy)
```
Sizable
 └── Dictable[str, ProjectOverLeaf]
      └── OverLeaf
```

## Factory

### `Factory.valdas() -> OverLeaf`
Create client using Valdas session cookies cached as a local
JSON file. First existing path wins:
- `F:/jsons/valdas/overleaf.json` (Windows)
- `/mnt/f/jsons/valdas/overleaf.json` (WSL)
- `~/prof/valdas/overleaf.json` (macOS / Linux)

JSON format is `{cookie_name: cookie_value, ...}` — at minimum
`overleaf_session2`. To refresh after expiry (~30 days), re-export
the cookies from Firefox DevTools (Storage → Cookies →
`https://www.overleaf.com`) and overwrite the JSON.

### `Factory.firefox() -> OverLeaf`
Create client using Firefox's cookie jar via
`browsercookie.firefox()`. Cross-platform, zero-config —
requires you to be logged in to Overleaf in Firefox.
Preferred on macOS because it reads Firefox's plaintext
`cookies.sqlite` directly and does **not** trigger a
Keychain prompt (unlike Chrome).

## Dependencies

| Import | Purpose |
|--------|---------|
| `pyoverleaf` | Python OverLeaf API |
| `bs4.BeautifulSoup` | Parse CSRF token from dashboard HTML |
| `f_core.mixins.dictable.Dictable` | Dict-like base class |
| `f_overleaf.project.ProjectOverLeaf` | Project data class |
| `json` | Read cookie JSON file |
| `pathlib.Path` | Cookie file path |

## Usage Example
```python
from f_overleaf import OverLeaf

overleaf = OverLeaf.Factory.valdas()
project = overleaf['Test']  # ProjectOverLeaf
```
