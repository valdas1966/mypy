# Auth

## Purpose
Static utility class for Google authentication.
Supports two auth flows: Service Account (JSON key) and OAuth (browser login).
Each `Account` enum member declares its auth type; `get_creds()` dispatches
accordingly.

## Public API

### `Auth.get_creds(account: Account) -> Credentials`
Return credentials for the given account.
Dispatches to Service Account or OAuth based on `account.type_auth`.

### `Auth.Factory.rami() -> Credentials`
Return Service Account credentials for RAMI (`project_id='noteret'`).

### `Auth.Factory.valdas() -> Credentials`
Return OAuth credentials for VALDAS (opens browser on first use).

### Enums

#### `TypeAuth`
| Value | Description |
|-------|-------------|
| `SERVICE_ACCOUNT` | JSON key file auth |
| `OAUTH` | Browser-based OAuth flow |

#### `Account`
| Value | Auth Type | Description |
|-------|-----------|-------------|
| `RAMI` | `SERVICE_ACCOUNT` | GCP project `noteret` |
| `VALDAS` | `OAUTH` | Personal Google account |

**Properties:** `account -> str`, `type_auth -> TypeAuth`

## Inheritance (Hierarchy)
```
Auth (static utility, no base class)
```
No inheritance. All methods are `@staticmethod`.

## Dependencies

| Import | Purpose |
|--------|---------|
| `google.oauth2.service_account.Credentials` | Service Account auth |
| `google.oauth2.credentials.Credentials` | OAuth token credentials |
| `google.auth.transport.requests.Request` | Token refresh |
| `google_auth_oauthlib.flow.InstalledAppFlow` | OAuth browser login |

## Credential Files (`~/prof/`)

| File | Purpose |
|------|---------|
| `rami.json` | RAMI Service Account key |
| `oauth_client.json` | OAuth client ID (from RAMI's GCP) |
| `valdas_token.json` | Cached VALDAS OAuth token (auto-generated) |

## Usage Example
```python
from f_google.auth import Auth, Account

# Service Account
creds = Auth.get_creds(account=Account.RAMI)
print(creds.project_id)  # 'noteret'

# OAuth (opens browser on first login, caches token after)
creds = Auth.get_creds(account=Account.VALDAS)
```
