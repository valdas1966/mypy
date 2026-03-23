# FileBase

## Purpose
Base class for file operations. Wraps a file path and provides
common file-system operations: existence check, deletion, size,
and path properties. Auto-creates the file if it does not exist.

## Public API

### Constructor
```python
def __init__(self, path: str) -> None
```
Store the path. Create parent dirs and empty file if not exists.

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `path` | `Path` | Full file path (pathlib) |
| `name` | `str` | File name with extension |
| `stem` | `str` | File name without extension |
| `suffix` | `str` | File extension (e.g., `.txt`) |
| `size` | `int` | File size in bytes |

### Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `exists()` | `bool` | True if file exists |
| `delete()` | `None` | Delete file; ignore if not exists |

### Dunder Methods
- `__str__` — file path as string
- `__repr__` — `<FileBase: path>`

## Inheritance (Hierarchy)
```
FileBase (this class)
 ├── FileTxt  — text file (read/write text, lines)
 │    └── FileTex  — LaTeX file (sections, packages)
 ├── FileCsv  — CSV file (rows, columns)
 ├── FileJson — JSON file (load, dump)
 └── FileImage — image file (dimensions, format)
```

## Factory

| Method | Returns |
|--------|---------|
| `empty()` | FileBase with new empty temp file |
| `with_content()` | FileBase with temp file containing 'hello' |
| `non_existing()` | FileBase with auto-created file at temp path |

## Dependencies

| Import | Purpose |
|--------|---------|
| `pathlib.Path` | File path operations |
