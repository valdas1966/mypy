# WidgetStatus

## Purpose
Tkinter Frame widget that displays answer feedback
(correct/wrong) and the current score.

## Public API

```python
class WidgetStatus(tk.Frame):
    def __init__(self, master: tk.Widget) -> None
    def set_correct(self) -> None
    def set_wrong(self, answer: str) -> None
    def set_score(self, score: int, total: int) -> None
    def set_finished(self, score: int, total: int) -> None
```

## Dependencies

| Import | Purpose |
|--------|---------|
| `tkinter` | GUI framework |
