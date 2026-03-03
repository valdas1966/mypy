# Auth

## Purpose
Static utility class for Google Service-Account authentication.
Takes a path to a JSON key file and scopes, returns `SACredentials`.

## Public API

### `Auth.get_creds(path: str, scopes: list[str]) -> SACredentials`
Return Service-Account credentials from a JSON key file.

### `Auth.Factory.rami() -> SACredentials`
Return credentials for RAMI (project `noteret`).
Resolves path via `~/prof/rami.json` (Mac) or `RAMI_JSON_PATH` env var.

## Inheritance (Hierarchy)
```
Auth (static utility, no base class)
```

## Dependencies

| Import | Purpose |
|--------|---------|
| `google.oauth2.service_account.Credentials` | SA credentials |

## Credential Files

| Platform | Path |
|----------|------|
| Mac | `~/prof/rami.json` |
| Windows | `RAMI_JSON_PATH` env var |

## Usage Example
```python
from f_google.auth import Auth

# Via Factory
creds = Auth.Factory.rami()
print(creds.project_id)  # 'noteret'

# Generic
creds = Auth.get_creds(path='/path/to/key.json',
                       scopes=['https://...'])
```
