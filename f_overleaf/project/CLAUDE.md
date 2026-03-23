# ProjectOverLeaf

## Purpose
Represents an OverLeaf project with a unique ID (key) and a name.
Provides access to top-level files and folders.

## Public API

### Constructor
```python
def __init__(self, key: str, name: str, api: pyoverleaf.Api) -> None
```
Create a project with an OverLeaf ID, name, and API reference.

### Properties

| Property | Type | Source |
|----------|------|--------|
| `key` | `str` | `HasKey[str]` — OverLeaf project ID |
| `name` | `str` | `HasName` — project name |

### Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `list_files()` | `list[str]` | Top-level file names |
| `list_folders()` | `list[str]` | Top-level folder names |
| `create_folder(path)` | `None` | Create folder; override if exists |
| `delete_folder(path)` | `None` | Delete folder; ignore if not found |
| `create_file(path, text)` | `None` | Create text file; override if exists |
| `upload_file(path_src, path_dest)` | `None` | Upload local file; override if exists |
| `delete_file(path)` | `None` | Delete file; ignore if not found |

### Dunder Methods
- `__str__` — returns `name` (from `HasName`, first in MRO)
- `__eq__` — equality by key (from `HasKey`)
- `__lt__` — comparison by key (from `HasKey`)
- `__hash__` — hash by key (from `HasKey`)

## Inheritance (Hierarchy)
```
HasName
HasKey[str] (Comparable, Hashable)
 └── ProjectOverLeaf
```

## Dependencies

| Import | Purpose |
|--------|---------|
| `pyoverleaf` | API access, ProjectFile, ProjectFolder |
| `f_core.mixins.has.key.HasKey` | Key identity mixin |
| `f_core.mixins.has.name.HasName` | Name property mixin |
