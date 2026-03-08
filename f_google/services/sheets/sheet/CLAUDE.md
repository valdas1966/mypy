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

### Methods

```python
def last_row(self) -> int
```
Return the 1-based index of the last row with a non-empty cell. Returns 0 if all rows are empty.

```python
def last_col(self) -> int
```
Return the 1-based index of the last column with a non-empty cell. Returns 0 if all cells are empty.

```python
def to_range(self) -> Range
```
Return all data as a `Range`.

### Dunder Methods

```python
def __getitem__(self, key: int | slice) -> list[str] | Range
```
Return row at the given index (0-based), or a `Range` from a slice. Triggers lazy load on first call.

## Inheritance (Hierarchy)

```
Sheet (standalone class, no base class)
```

No bases. No Factory or Tester — requires a live `gspread.Worksheet` (tested via `Spread`'s tester).

## Dependencies

| Import | Purpose |
|--------|---------|
| `gspread` | `Worksheet` type for the wrapped object |
| `f_ds.range.Range` | `Range` data structure for `to_range()` and slice access |

## Usage Examples

### Via Spread

```python
from f_google.services.sheets.spread import Spread

spread = Spread.Factory.valdas(id_spread='...')
sheet = spread['Sheet1']
print(sheet.name)     # 'Sheet1'
print(sheet.last_row())  # 1-based last row with data
print(sheet.last_col())  # 1-based last col with data
print(sheet[0])       # first row as list[str]
```
