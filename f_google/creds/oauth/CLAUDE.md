# OAuth

## Purpose
Static utility class for Google OAuth (browser-based) authentication.
Takes paths to client secrets and token cache, returns `OAuthCredentials`.

## Public API

### `OAuth.get_creds(path_client: str, path_token: str, scopes: list[str]) -> OAuthCredentials`
Return OAuth credentials. Opens browser on first use, caches token after.

### `OAuth.Factory.valdas() -> OAuthCredentials`
Return OAuth credentials for VALDAS.
Resolves paths via `~/prof/` (Mac) or env vars (Windows).

## Inheritance (Hierarchy)
```
OAuth (static utility, no base class)
```

## Dependencies

| Import | Purpose |
|--------|---------|
| `google.oauth2.credentials.Credentials` | OAuth token credentials |
| `google.auth.transport.requests.Request` | Token refresh |
| `google_auth_oauthlib.flow.InstalledAppFlow` | OAuth browser login |

## Credential Files

| Platform | Client Secrets | Token Cache |
|----------|---------------|-------------|
| Mac | `~/prof/oauth_client.json` | `~/prof/valdas_token.json` |
| Windows | `OAUTH_CLIENT_JSON_PATH` | `VALDAS_TOKEN_PATH` |

## Usage Example
```python
from f_google.oauth import OAuth

# Via Factory
creds = OAuth.Factory.valdas()

# Generic
creds = OAuth.get_creds(path_client='/path/to/client.json',
                        path_token='/path/to/token.json',
                        scopes=['https://...'])
```
