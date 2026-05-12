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
| `set_root_doc(name)` | `None` | Set project's compile root document |

### Dunder Methods
- `__str__` — returns `name` (from `HasName`, first in MRO)
- `__eq__` — equality by key (from `HasKey`)
- `__lt__` — comparison by key (from `HasKey`)
- `__hash__` — hash by key (from `HasKey`)

## RootDoc Note — `create_file` Breaks the Root Document Pointer

A new Overleaf project ships with a stub `main.tex` and the
project's `rootDoc_id` set to that doc's `_id`. `create_file()`
(and `upload_file()`) implement "override if exists" by deleting
the old file first, then uploading new bytes. If the deleted
file was the project's root document, `rootDoc_id` becomes
`None` and Overleaf shows the project as having **no main
document** — compilation fails silently from the UI.

After overwriting the root doc, call `set_root_doc(name)` to
re-bind the project to the new doc:

```python
proj.create_file(path='main.tex', text=tex)
proj.set_root_doc('main.tex')
```

The endpoint is `POST /project/<id>/settings` with body
`{rootDocId: <doc_id>}`. The doc must be at the project root
and of type `'doc'` (i.e., the same multipart `/upload` we use
classified it as text — see *Encoding Note* below).

## Encoding Note — Overleaf Upload is ASCII-Only

The Overleaf `/project/<id>/upload` endpoint (used by
`pyoverleaf.Api.project_upload_file`) silently corrupts any byte
in a text upload that is `>= 0x80`. Each high-bit byte is decoded
as Latin-1 and re-encoded as UTF-8 server-side, byte-by-byte (not
as multi-byte UTF-8 sequences). So a UTF-8 file containing `─`
(`E2 94 80`) becomes `Ã  ⃞ ⃞` on storage. The transform is
purely lossy — there is no client-side encoding that survives it
for chars outside U+0000–U+007F. Binary uploads (e.g. PDF, PNG)
pass through unchanged because Overleaf detects them as binary
(NULL bytes / non-text signal) and skips the conversion.

**Rule:** `create_file(path, text)` requires `text` to be pure
ASCII. It raises `ValueError` listing any offending chars. To
include math symbols, accented letters, or decorative dividers,
use LaTeX commands instead (`\S` for `§`, `\alpha` for `α`,
`---` or `=` for `═`, `\ldots` for `…`, etc.).

**Workaround for arbitrary text** (not yet implemented): set
the document content via the Overleaf WebSocket / ShareJS
protocol (`joinDoc` + insert operations). `pyoverleaf` only
exposes the read side (`_pull_doc_project_file_content`).

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
