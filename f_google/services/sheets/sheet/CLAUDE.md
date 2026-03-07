# Sheet

## Purpose

Wrapper around a `gspread.Worksheet` providing lazy-loaded row access.
Loads all cell values on first access and caches them for subsequent reads.

## Public API

### Constructor

```python
def __init__(self, ws: gspread.Worksheet) -> None
```
Wrap a live `gspread.Worksheet`. Rows are not fetched until first access.

### Properties

```python
@property
def name(self) -> str
```
Return the worksheet title.

### Dunder Methods

```python
def __getitem__(self, row: int) -> list[str]
```
Return row at the given index (0-based). Triggers lazy load on first call.

```python
def __len__(self) -> int
```
Return the number of rows. Triggers lazy load on first call.

## Inheritance (Hierarchy)

```
Sheet (standalone class, no base class)
```

No bases. No Factory or Tester — requires a live `gspread.Worksheet` (tested via `Spread`'s tester).

## Dependencies

| Import | Purpose |
|--------|---------|
| `gspread` | `Worksheet` type for the wrapped object |

## Usage Examples

### Via Spread

```python
from f_google.services.sheets.spread import Spread

spread = Spread.Factory.valdas(id_spread='...')
sheet = spread['Sheet1']
print(sheet.name)     # 'Sheet1'
print(len(sheet))     # number of rows
print(sheet[0])       # first row as list[str]
```
