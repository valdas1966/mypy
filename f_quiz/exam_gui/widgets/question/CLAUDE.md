# WidgetQuestion

## Purpose
Tkinter Frame widget that displays a question counter
and question text. Uses large bold font (Arial 52) with
1200px wraplength for fullscreen readability.

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
