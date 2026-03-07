# Spread

## Purpose

Google Spreadsheet wrapper built on `gspread`.
Provides access to sheets within a spreadsheet by name or index,
using either OAuth or Service-Account credentials.

## Public API

```python
class Spread(HasName):
    def __init__(self,
                 creds: OAuthCredentials | SACredentials,
                 id_spread: str) -> None

    @property
    def sheets(self) -> list[Sheet]

    def __getitem__(self, name: str) -> Sheet
```

### Factory

```python
Factory.valdas(id_spread: str) -> Spread
Factory.valdas_test() -> Spread
Factory.rami(id_spread: str) -> Spread
```

## Inheritance (Hierarchy)

```
HasName
  └── Spread
```

## Dependencies

| Import | Purpose |
|--------|---------|
| `gspread` | Google Sheets client (authorize, open_by_key) |
| `google.oauth2.credentials.Credentials` | OAuth credentials type |
| `google.oauth2.service_account.Credentials` | SA credentials type |
| `f_google.services.sheets.sheet.Sheet` | Sheet wrapper |
| `f_core.mixins.has.HasName` | Name mixin (spreadsheet title) |
| `f_google.creds.oauth.OAuth` | Factory: OAuth credentials |
| `f_google.creds.auth.Auth` | Factory: SA credentials |

## Usage Examples

```python
from f_google.services.sheets.spread import Spread

# Open a spreadsheet via OAuth
spread = Spread.Factory.valdas(id_spread='<SPREADSHEET_ID>')

# Get spreadsheet name
print(spread.name)

# List all sheets
sheets = spread.sheets

# Access a sheet by name
sheet = spread['Sheet1']

# Read a cell value
value = sheet[1][0]
```
