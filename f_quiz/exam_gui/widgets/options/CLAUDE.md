# WidgetOptions

## Purpose
Tkinter Frame widget that displays two answer options as large
side-by-side labels. Supports highlighting correct/wrong choices.

## Public API

```python
class WidgetOptions(tk.Frame):
    def __init__(self, master: tk.Widget) -> None
    def set_options(self, options: list[str]) -> None
    def get(self, key: int) -> str      # key is 1 or 2
    def highlight_correct(self, key: int) -> None
    def highlight_wrong(self, key: int) -> None
    def clear(self) -> None
```

## Dependencies

| Import | Purpose |
|--------|---------|
| `tkinter` | GUI framework |
