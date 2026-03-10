# ExamGui

## Purpose
GUI exam application using tkinter. Displays questions one at a time,
accepts answers via text entry, and shows feedback with score.

## Structure

| Path | Purpose |
|------|---------|
| `runner/` | ExamRunner — pure exam logic (no GUI) |
| `widgets/question/` | WidgetQuestion — question display |
| `widgets/answer/` | WidgetAnswer — answer text entry |
| `widgets/status/` | WidgetStatus — feedback and score |

## Public API

```python
class ExamGui:
    def __init__(self,
                 questions: list[Question],
                 is_random: bool = False,
                 n_questions: int | None = None) -> None
    def run(self) -> None
```

## Factory

```python
Factory.two_capitals() -> ExamGui
Factory.hebrew() -> ExamGui
Factory.hebrew_random(n_questions=None) -> ExamGui
```

## Dependencies

| Import | Purpose |
|--------|---------|
| `tkinter` | GUI framework |
| `f_quiz.question.Question` | Question class |
| `f_quiz.exam_gui.runner.ExamRunner` | Exam logic |
| `f_quiz.exam_gui.widgets.*` | GUI widgets |
