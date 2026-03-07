# creds

## Purpose

Sub-package grouping all Google authentication credential providers.
Re-exports `Auth` and `OAuth` for convenient access via `f_google.creds`.

## Structure

| Module | Class | Purpose |
|--------|-------|---------|
| `auth/` | `Auth` | Service-Account authentication (JSON key file) |
| `oauth/` | `OAuth` | OAuth browser-based authentication (token caching) |

## Public API (re-exports)

```python
from f_google.creds import Auth, OAuth
```

### Auth

```python
Auth.get_creds(path: str, scopes: list[str]) -> SACredentials
Auth.Factory.rami() -> SACredentials
```
Service-Account credentials from a JSON key file.

### OAuth

```python
OAuth.get_creds(path_client: str, path_token: str, scopes: list[str]) -> OAuthCredentials
OAuth.Factory.valdas() -> OAuthCredentials
```
OAuth credentials with token caching and browser login flow.

## Inheritance (Hierarchy)

```
creds/                  (re-export package)
├── auth/Auth           (standalone static utility)
└── oauth/OAuth         (standalone static utility)
```

No inheritance between `Auth` and `OAuth` — they are independent utilities.

## Dependencies

| Import | Purpose |
|--------|---------|
| `f_google.creds.auth.Auth` | Re-exported |
| `f_google.creds.oauth.OAuth` | Re-exported |

## Security — Credential File Storage

| Concern | Status |
|---------|--------|
| Credentials in git | Not tracked — key files live outside repo |
| Auth key path | `~/prof/rami.json` (macOS) or `RAMI_JSON_PATH` env var |
| OAuth client path | `~/prof/valdas/oauth_client.json` or `OAUTH_CLIENT_JSON_PATH` env var |
| OAuth token path | `~/prof/valdas/token.json` or `VALDAS_TOKEN_PATH` env var |
| Token file permissions | Default `open()` — world-readable on shared systems |

## Usage Example

```python
from f_google.creds import Auth, OAuth

# Service Account
sa_creds = Auth.Factory.rami()

# OAuth (browser login on first use)
oauth_creds = OAuth.Factory.valdas()
```
