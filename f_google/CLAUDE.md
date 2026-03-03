# f_google

## Purpose
Framework package for Google Cloud and Google Workspace services.
Provides authentication and client wrappers.

## Public API

### Modules
| Module | Class | Purpose |
|--------|-------|---------|
| `auth/` | `Auth` | Service-Account authentication |
| `oauth/` | `OAuth` | OAuth (browser-based) authentication |
| `bigquery/` | `BigQuery` | BigQuery client wrapper |

### Re-exports from `__init__.py`
```python
from f_google import Auth, OAuth, BigQuery
```

## Dependencies

| Import | Purpose |
|--------|---------|
| `google-auth` | Google authentication core |
| `google-auth-oauthlib` | OAuth browser flow |
| `google-cloud-bigquery` | BigQuery client |
| `pandas` | DataFrame results |

## Usage Example
```python
from f_google import Auth, OAuth, BigQuery

# Service Account (RAMI)
creds = Auth.Factory.rami()

# OAuth (VALDAS)
creds = OAuth.Factory.valdas()

# BigQuery
bq = BigQuery.Factory.rami()
df = bq.select(query='SELECT * FROM dataset.table')
```
