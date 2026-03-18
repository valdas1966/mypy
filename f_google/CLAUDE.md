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
| `services/drive/` | `Drive` | Google Drive client wrapper |
| `services/sheets/` | `Spread` | Google Sheets client wrapper |

### Re-exports from `__init__.py`
```python
from f_google import Auth, OAuth, BigQuery, Drive, Spread
from f_google.creds import Auth, OAuth
from f_google.services import BigQuery, Drive, Spread
```

## Dependencies

| Import | Purpose |
|--------|---------|
| `google-auth` | Google authentication core |
| `google-auth-oauthlib` | OAuth browser flow |
| `google-cloud-bigquery` | BigQuery client |
| `google-api-python-client` | Drive API v3 client |
| `gspread` | Google Sheets client |
| `pandas` | DataFrame results |

## Usage Example
```python
from f_google import Auth, OAuth, BigQuery, Drive, Spread

# Service Account (RAMI)
creds = Auth.Factory.rami()

# OAuth (VALDAS)
creds = OAuth.Factory.valdas()

# BigQuery
bq = BigQuery.Factory.rami()
df = bq.select(query='SELECT * FROM dataset.table')

# Drive
drive = Drive.Factory.valdas()
folders = drive.folders(path='projects/2024')
drive.create_folder(path='projects/2025/data')

# Sheets
spread = Spread.Factory.valdas(id_spread='...')
sheet = spread['Sheet1']
```
