# FileTex

## Purpose
LaTeX file class with document structure operations.
Extends `FileTxt` with LaTeX-specific functionality.

## Public API

### Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `add_document_class(name)` | `None` | Add `\documentclass{name}` as first line |
| `add_environment(name)` | `None` | Add `\begin{name}...\end{name}` |

### Inherited from FileTxt

| Member | Type | Description |
|--------|------|-------------|
| `text` | `str` (read/write) | File content as string |
| `lines()` | `list[str]` | Content as list of lines |
| `write_line(line, index)` | `None` | Insert line at index |
| `delete_line(index)` | `None` | Delete line at index |

### Inherited from FileBase

| Member | Type | Description |
|--------|------|-------------|
| `path` | `Path` | Full file path |
| `name` | `str` | File name with extension |
| `size` | `int` | File size in bytes |
| `exists()` | `bool` | True if file exists |
| `delete()` | `None` | Delete file |

## Inheritance (Hierarchy)
```
HasRepr
 └── FileBase
      └── FileTxt
           └── FileTex (this class)
```

## Factory

| Method | Returns |
|--------|---------|
| `empty()` | Empty FileTex |
| `article()` | Minimal article with document environment |

## Dependencies

| Import | Purpose |
|--------|---------|
| `f_psl.file.i_1_txt.FileTxt` | Base text file operations |

## Behavior Notes
- `add_environment()` inserts before `\end{document}` if found,
  otherwise appends at end.
