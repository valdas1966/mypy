# WidgetQuestion

## Purpose
Tkinter Frame widget that displays a question counter
and question text.

## Public API

```python
class WidgetQuestion(tk.Frame):
    def __init__(self, master: tk.Widget) -> None
    def set_question(self, number: int, total: int,
                     text: str) -> None
```

## Dependencies

| Import | Purpose |
|--------|---------|
| `tkinter` | GUI framework |
