# ExamGuiOptions

## Purpose
GUI exam for two-option questions. User presses 1 or 2 to choose
the correct answer. Highlights correct/wrong with color feedback.
Wrong answers loop on the same question but count as mistakes.

## Public API

```python
class ExamGuiOptions:
    def __init__(self,
                 questions: list[QuestionOptions],
                 is_random: bool = False,
                 n_questions: int | None = None) -> None
    def run(self) -> None
```

## Factory

```python
Factory.logic() -> ExamGuiOptions
```

## Reused Components

| Component | From |
|-----------|------|
| `ExamRunner` | `f_quiz.exam_gui.runner` |
| `WidgetQuestion` | `f_quiz.exam_gui.widgets.question` |
| `WidgetStatus` | `f_quiz.exam_gui.widgets.status` |
| `WidgetOptions` | `f_quiz.exam_gui.widgets.options` |

## Dependencies

| Import | Purpose |
|--------|---------|
| `tkinter` | GUI framework |
| `f_quiz.question_options.QuestionOptions` | Question type |
| `f_quiz.exam_gui.runner.ExamRunner` | Exam logic |
| `f_quiz.exam_gui.widgets.*` | Shared widgets |
