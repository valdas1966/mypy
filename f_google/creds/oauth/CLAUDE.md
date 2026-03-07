# OAuth

## Purpose

Static utility class for Google OAuth (browser-based) authentication.
Takes paths to client secrets and token cache files, returns `OAuthCredentials`.
Opens browser for login on first use, caches and refreshes token automatically.

## Public API

### Class Attribute

```python
Factory: type | None = None
```
Factory for creating credential instances. Wired via `__init__.py`.

### Static Methods

```python
@staticmethod
def get_creds(path_client: str, path_token: str, scopes: list[str]) -> OAuthCredentials
```
Return OAuth credentials. Loads cached token if available, refreshes if expired, or opens browser login flow if no valid token exists. Saves token to `path_token` after authentication.

### Factory Methods

```python
@staticmethod
def valdas() -> OAuthCredentials
```
Return OAuth credentials for VALDAS. Resolves paths via `~/prof/valdas/` (macOS) or env vars `OAUTH_CLIENT_JSON_PATH` / `VALDAS_TOKEN_PATH`.

## Inheritance (Hierarchy)

```
OAuth (standalone static utility, no base class)
```

No bases. All methods are `@staticmethod`.

## Dependencies

| Import | Purpose |
|--------|---------|
| `google.oauth2.credentials.Credentials` | OAuth token credentials |
| `google.auth.transport.requests.Request` | Token refresh transport |
| `google_auth_oauthlib.flow.InstalledAppFlow` | OAuth browser login flow |
| `pathlib.Path` | File existence check and path resolution (Factory) |
| `os.environ` | Read env vars for credential paths (Factory) |
| `sys.platform` | Platform detection for path resolution (Factory) |

## Usage Examples

### Via Factory

```python
from f_google.creds.oauth import OAuth

creds = OAuth.Factory.valdas()
```

### Generic

```python
from f_google.creds.oauth import OAuth

creds = OAuth.get_creds(path_client='/path/to/client.json',
                        path_token='/path/to/token.json',
                        scopes=['https://www.googleapis.com/auth/drive'])
```
