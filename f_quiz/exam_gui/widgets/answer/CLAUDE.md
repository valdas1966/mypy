# WidgetAnswer

## Purpose
Tkinter Frame widget with an Entry for user answer input.
Supports Enter key binding and text retrieval. Uses large
bold font (Arial 44) with extra height (ipady=15).

## Public API

```python
class WidgetAnswer(tk.Frame):
    def __init__(self, master: tk.Widget) -> None
    @property
    def text(self) -> str
    def clear(self) -> None
    def focus(self) -> None
    def bind_enter(self, callback: Callable) -> None
```

## Dependencies

| Import | Purpose |
|--------|---------|
| `tkinter` | GUI framework |
