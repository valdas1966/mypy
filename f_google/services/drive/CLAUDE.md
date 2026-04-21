# Drive

## Purpose
Facade wrapper for Google Drive API v3.
Delegates to single-purpose internal helpers for navigation,
folder management, download, upload, and in-memory reading.

## Public API

### `__init__(creds: OAuthCredentials | SACredentials) -> None`
Create a Drive client with OAuth or Service-Account credentials.

### `folders(path: str = None) -> list[str]`
Return names of sub-folders at the given path.
`path=None` means Drive root.

### `files(path: str = None) -> list[str]`
Return names of files (non-folders) at the given path.
`path=None` means Drive root.

### `is_exists(path: str) -> bool`
Return True if a file or folder exists at the given path.

### `delete(path: str) -> None`
Permanently delete a file or folder (recursive for folders).

### `create_folder(path: str) -> None`
Create a folder at the given path (mkdir -p).
If the target folder already exists, deletes and re-creates it.

### `download(path_src: str, path_dest: str) -> None`
Download a file or folder from Drive to a local path.
Google-native docs exported to suitable formats.
Folders are downloaded recursively.

### `upload(path_src: str, path_dest: str) -> None`
Upload a local file or folder to Drive.
Creates parent folders if needed. Overwrites silently.
Folders are uploaded recursively.

### `read(path: str, encoding: str = 'utf-8') -> _ReadResponse`
Read a file from Drive into memory (no disk writes).
- `.txt`, `.csv`: decoded text using the specified encoding
- `.pdf`: markdown text + rendered page images (delegates to `f_pdf`)
- Returns `_ReadResponse` with `.text` and `.pages` properties

### `get_path_by_id(file_id: str) -> str`
Resolve a Drive file/folder ID to its `/`-joined path relative to
"My Drive" root. Walks parents via `files().get(fields='name,parents')`.
Raises `FileNotFoundError` for unknown IDs.

Used by consumers that receive fileIds from external triggers
(e.g. `f_tex_editor`'s `/drive-ui/open` entry point, driven by a
browser extension / bookmarklet from `drive.google.com`).

## Inheritance (Hierarchy)
```
Drive (no base class)
```
Standalone facade. Composes internal helpers.

## Internal Architecture
```
Drive (facade)
├── _Nav       — path resolution, listing, existence checks
├── _Folders   — create, delete, ensure parents
├── _Download  — download files/folders to disk
├── _Upload    — upload files/folders from disk
└── _Read      — read files into memory (uses f_pdf for PDFs)
```

All helpers live in `_internal/`:

| File | Class | Purpose |
|------|-------|---------|
| `_internal/_nav.py` | `_Nav` | resolve, find_child, list_children |
| `_internal/_folders.py` | `_Folders` | create, delete, ensure_parents |
| `_internal/_download.py` | `_Download` | download file/folder to disk |
| `_internal/_upload.py` | `_Upload` | upload file/folder from disk |
| `_internal/_read.py` | `_Read` | read to memory, delegate to f_pdf |
| `_internal/_read_response.py` | `_ReadResponse` | return type for read() |

## Path Semantics
- Separator: `/`
- `path=None` -> Drive root ("My Drive")
- Duplicate names in same parent -> `ValueError`
- Non-existent path -> `FileNotFoundError`

## Dependencies

| Import | Purpose |
|--------|---------|
| `google.oauth2.credentials.Credentials` | OAuth credentials |
| `google.oauth2.service_account.Credentials` | SA credentials |
| `googleapiclient.discovery` | Drive API v3 client |
| `f_pdf.UPdf` | PDF parsing (used by _Read) |

## Usage Example
```python
from f_google.services.drive import Drive

drive = Drive.Factory.valdas()
folders = drive.folders(path='projects/2024')
drive.create_folder(path='projects/2025/data')
drive.delete(path='projects/old')

# Download a file
drive.download(path_src='projects/report.pdf',
               path_dest='/local/report.pdf')

# Upload a folder
drive.upload(path_src='/local/data',
             path_dest='projects/2025/data')

# Read a text file into memory (no disk writes)
response = drive.read(path='projects/notes.txt')
print(response.text)

# Read a PDF — get text + page images
response = drive.read(path='papers/attention.pdf')
print(response.text)        # markdown with tables
for i, page in enumerate(response.pages):
    with open(f'/tmp/page_{i}.png', 'wb') as f:
        f.write(page)       # save for visual inspection
```
