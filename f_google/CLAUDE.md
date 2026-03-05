# f_google

## Purpose
Framework package for Google Cloud and Google Workspace services.
Provides authentication and client wrappers.

## Structure

### `creds/` — Credential Providers
| Module | Class | Purpose |
|--------|-------|---------|
| `creds/auth/` | `Auth` | Service-Account authentication |
| `creds/oauth/` | `OAuth` | OAuth (browser-based) authentication |

### `services/` — Service Wrappers
| Module | Class | Purpose |
|--------|-------|---------|
| `services/bigquery/` | `BigQuery` | BigQuery client wrapper |
| `services/sheets/` | `Spread` | Google Sheets client wrapper |

### Re-exports from `__init__.py`
```python
from f_google import Auth, OAuth, BigQuery, Spread
from f_google.creds import Auth, OAuth
from f_google.services import BigQuery, Spread
```

## Dependencies

| Import | Purpose |
|--------|---------|
| `google-auth` | Google authentication core |
| `google-auth-oauthlib` | OAuth browser flow |
| `google-cloud-bigquery` | BigQuery client |
| `gspread` | Google Sheets client |
| `pandas` | DataFrame results |

## Usage Example
```python
from f_google import Auth, OAuth, BigQuery, Spread

# Service Account (RAMI)
creds = Auth.Factory.rami()

# OAuth (VALDAS)
creds = OAuth.Factory.valdas()

# BigQuery
bq = BigQuery.Factory.rami()
df = bq.select(query='SELECT * FROM dataset.table')

# Sheets
spread = Spread.Factory.valdas(id_spread='...')
sheet = spread['Sheet1']
```
