# Sheet

## Purpose

Wrapper around a `gspread.Worksheet` providing lazy-loaded row access.
Loads all cell values on first access and caches them. Returns
`list[Cell]` rows where each Cell supports `.value` setter for writes.

## Public API

```python
class Sheet:
    def __init__(self, ws: gspread.Worksheet) -> None
    @property
    def name(self) -> str
    def last_row(self) -> int
    def last_col(self) -> int
    def insert_row(self, row: int) -> None   # 1-based, pushes down
    def delete_row(self, row: int) -> None  # 1-based, removes row
    def to_range(self) -> Range
    def __getitem__(self, key: int | slice) -> list[Cell] | Range
```

## Dependencies

| Import | Purpose |
|--------|---------|
| `gspread` | `Worksheet` type for the wrapped object |
| `f_ds.range.Range` | `Range` data structure for `to_range()` and slice |
| `f_google.services.sheets.cell.Cell` | Cell proxy with write support |

## Usage Examples

```python
sheet = spread['Sheet1']
print(sheet[0][0])              # read cell as str
sheet[1][2].value = 'hello'     # write to Google Sheet
```
