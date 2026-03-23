# OverLeaf

## Purpose
Client wrapper for OverLeaf (online LaTeX editor).
Inherits from `Dictable[str, ProjectOverLeaf]` — projects are
accessed by name via `overleaf['Project Name']`.

## Public API

### `__init__(api: pyoverleaf.Api) -> None`
Create an OverLeaf client with an authenticated pyoverleaf Api.
Eagerly loads all projects into the internal dict.

### Inherited from Dictable
- `overleaf['Name']` — get project by name
- `overleaf.keys()` — all project names
- `overleaf.values()` — all ProjectOverLeaf objects
- `len(overleaf)` — number of projects
- `'Name' in overleaf` — check if project exists

## Inheritance (Hierarchy)
```
Sizable
 └── Dictable[str, ProjectOverLeaf]
      └── OverLeaf
```

## Factory

### `Factory.valdas() -> OverLeaf`
Create client using Valdas session cookies stored in
`F:/jsons/valdas/overleaf.json`.

## Dependencies

| Import | Purpose |
|--------|---------|
| `pyoverleaf` | Python OverLeaf API |
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
