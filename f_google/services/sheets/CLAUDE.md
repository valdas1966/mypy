# sheets

## Purpose

Sub-package grouping Google Sheets service wrappers.
Re-exports `Spread` and `Sheet` for convenient access via `f_google.services.sheets`.

## Public API (re-exports)

```python
from f_google.services.sheets import Spread, Sheet
```

### Spread

```python
class Spread(HasName):
    def __init__(self,
                 creds: OAuthCredentials | SACredentials,
                 id_spread: str) -> None

    @property
    def sheets(self) -> list[Sheet]

    def __getitem__(self, name: str) -> Sheet
```
Google Spreadsheet wrapper. Authorizes via OAuth or Service-Account credentials
and opens a spreadsheet by ID.

**Factory:**
```python
Factory.valdas(id_spread: str) -> Spread
Factory.valdas_test() -> Spread
Factory.rami(id_spread: str) -> Spread
```

### Sheet

```python
class Sheet:
    def __init__(self, ws: gspread.Worksheet) -> None

    @property
    def name(self) -> str

    def __getitem__(self, row: int) -> list[str]
    def __len__(self) -> int
```
Worksheet wrapper with lazy-loaded row access.
No Factory or Tester — requires a live API connection, tested via `Spread`.

## Inheritance (Hierarchy)

```
HasName
  └── Spread

Sheet (standalone class, no base class)
```

## Dependencies

| Import | Purpose |
|--------|---------|
| `f_google.services.sheets.spread.Spread` | Re-exported |
| `f_google.services.sheets.sheet.Sheet` | Re-exported |
| `gspread` | Google Sheets client (transitive) |
| `f_core.mixins.has.HasName` | Name mixin for Spread (transitive) |
| `f_google.creds.oauth.OAuth` | Factory: OAuth credentials (transitive) |
| `f_google.creds.auth.Auth` | Factory: SA credentials (transitive) |

## Usage Examples

```python
from f_google.services.sheets import Spread

# Open a spreadsheet via OAuth
spread = Spread.Factory.valdas(id_spread='<SPREADSHEET_ID>')

# Spreadsheet name
print(spread.name)

# List all sheets
sheets = spread.sheets

# Access a sheet by name
sheet = spread['Sheet1']

# Read rows
print(len(sheet))     # number of rows
print(sheet[0])       # first row as list[str]
```
