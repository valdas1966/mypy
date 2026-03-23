# FileTxt

## Purpose
Text file class with read/write content operations.
Extends `FileBase` with text-specific functionality.

## Public API

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `text` | `str` (read/write) | File content as string |

### Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `lines()` | `list[str]` | Content as list of lines |

### Inherited from FileBase

| Member | Type | Description |
|--------|------|-------------|
| `path` | `Path` | Full file path |
| `name` | `str` | File name with extension |
| `stem` | `str` | File name without extension |
| `suffix` | `str` | File extension |
| `size` | `int` | File size in bytes |
| `exists()` | `bool` | True if file exists |
| `delete()` | `None` | Delete file |

## Inheritance (Hierarchy)
```
HasRepr
 └── FileBase
      └── FileTxt (this class)
           └── FileTex — LaTeX file
```

## Factory

| Method | Returns |
|--------|---------|
| `empty()` | FileTxt with empty content |
| `hello()` | FileTxt with 'hello' content |
| `lines()` | FileTxt with 'aaa\nbbb\nccc' content |

## Dependencies

| Import | Purpose |
|--------|---------|
| `f_psl.file.i_0_base.FileBase` | Base file operations |
