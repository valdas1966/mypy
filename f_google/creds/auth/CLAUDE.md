# Auth

## Purpose

Static utility class for Google Service-Account authentication.
Takes a path to a JSON key file and scopes, returns `SACredentials`.

## Public API

### Class Attribute

```python
Factory: type | None = None
```
Factory for creating credential instances. Wired via `__init__.py`.

### Static Methods

```python
@staticmethod
def get_creds(path: str, scopes: list[str]) -> SACredentials
```
Return Service-Account credentials from a JSON key file using `SACredentials.from_service_account_file()`.

### Factory Methods

```python
@staticmethod
def rami() -> SACredentials
```
Return credentials for RAMI (project: `noteret`). Resolves path via `~/prof/rami.json` (macOS) or `RAMI_JSON_PATH` env var.

## Inheritance (Hierarchy)

```
Auth (standalone static utility, no base class)
```

No bases. All methods are `@staticmethod`.

## Dependencies

| Import | Purpose |
|--------|---------|
| `google.oauth2.service_account.Credentials` | SA credentials class |
| `pathlib.Path` | Resolve home directory path (Factory) |
| `os.environ` | Read env var for key file path (Factory) |
| `sys.platform` | Platform detection for path resolution (Factory) |

## Usage Examples

### Via Factory

```python
from f_google.creds.auth import Auth

creds = Auth.Factory.rami()
print(creds.project_id)  # 'noteret'
```

### Generic

```python
from f_google.creds.auth import Auth

creds = Auth.get_creds(path='/path/to/key.json',
                       scopes=['https://www.googleapis.com/auth/cloud-platform'])
```
