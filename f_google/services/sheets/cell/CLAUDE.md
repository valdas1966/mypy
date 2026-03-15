# Cell

## Purpose

Proxy for a Google Sheet cell. Extends `str` for backwards-compatible
read access. The `.value` setter writes `str(val)` to the remote
Google Sheet and updates the local cache.

## Public API

```python
class Cell(str):
    @property
    def value(self) -> str
    @value.setter
    def value(self, val: object) -> None
```

## Dependencies

| Import | Purpose |
|--------|---------|
| `gspread` | `Worksheet.update_cell()` for writes |

## Usage Examples

```python
cell = sheet[1][2]        # Cell is a str
print(cell)               # prints cell value
cell.value = 'hello'      # writes 'hello' to Google Sheet
cell.value = 42           # writes '42'
```
