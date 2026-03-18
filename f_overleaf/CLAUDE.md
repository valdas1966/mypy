# Overleaf

## Purpose
Client wrapper for Overleaf (online LaTeX editor).
Provides project listing via pyoverleaf.

## Public API

### `__init__(api: pyoverleaf.Api) -> None`
Create an Overleaf client with an authenticated pyoverleaf Api.

### `projects() -> list[str]`
Return names of all projects for the authenticated user.

## Inheritance (Hierarchy)
```
Overleaf (no base class)
```
No inheritance. Standalone client wrapper.

## Factory

### `Factory.gmail() -> Overleaf`
Create client using browser cookies (user logged into Overleaf
via Gmail in their browser).

### `Factory.token(cookies: dict[str, str]) -> Overleaf`
Create client using provided session cookies directly.

## Dependencies

| Import | Purpose |
|--------|---------|
| `pyoverleaf` | Python Overleaf API |

## Usage Example
```python
from f_overleaf import Overleaf

overleaf = Overleaf.Factory.gmail()
names = overleaf.projects()
```
