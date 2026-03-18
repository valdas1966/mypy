# Drive

## Purpose
Client wrapper for Google Drive API v3.
Provides path-based navigation, folder management, and file/folder
listing with permanent delete support.

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
Create a folder at the given path. Creates intermediate folders
if needed (mkdir -p). If the target folder already exists, deletes
and re-creates it (override behavior).

## Inheritance (Hierarchy)
```
Drive (no base class)
```
No inheritance. Standalone client wrapper.

## Internal Methods

### `_resolve(path: str = None) -> str`
Resolve a path string to a Drive folder/file ID.
Walks the folder tree segment by segment.
`None` resolves to `'root'`.

### `_find_child(parent_id: str, name: str) -> str | None`
Find a child ID by name within a parent folder.
Returns None if not found. Raises ValueError on duplicates.

### `_list_children(parent_id, mime_type, mime_type_exclude) -> list[str]`
List child names with optional MIME type filtering.

### `_create_single_folder(parent_id: str, name: str) -> str`
Create one folder and return its ID.

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

## Usage Example
```python
from f_google.services.drive import Drive

drive = Drive.Factory.valdas()
folders = drive.folders(path='projects/2024')
drive.create_folder(path='projects/2025/data')
drive.delete(path='projects/old')
exists = drive.is_exists(path='projects/2025')
```
