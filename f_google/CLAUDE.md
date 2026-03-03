# f_google

## Purpose
Framework package for Google Cloud and Google Workspace services.
Provides unified authentication and client wrappers.

## Public API

### Modules
| Module | Class | Purpose |
|--------|-------|---------|
| `auth/` | `Auth` | Authentication (Service Account + OAuth) |
| `bigquery/` | `BigQuery` | BigQuery client wrapper |

### Re-exports from `__init__.py`
```python
from f_google import Auth, Account, TypeAuth, BigQuery
```

## Dependencies

| Import | Purpose |
|--------|---------|
| `google-auth` | Google authentication core |
| `google-auth-oauthlib` | OAuth browser flow |
| `google-cloud-bigquery` | BigQuery client |
| `gspread` | Google Sheets (planned) |
| `pandas` | DataFrame results |

## Usage Example
```python
from f_google import Auth, Account, BigQuery

# Service Account (RAMI)
creds = Auth.Factory.rami()

# OAuth (VALDAS)
creds = Auth.Factory.valdas()

# BigQuery
bq = BigQuery.Factory.rami()
df = bq.select(query='SELECT * FROM dataset.table')
```
