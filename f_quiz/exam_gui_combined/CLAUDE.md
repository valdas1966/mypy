# ExamGuiCombined

## Purpose
Combined GUI exam that mixes text-input and two-option Questions.
Text Questions use Enter key (WidgetAnswer).
Option Questions use 1/2 keys (WidgetOptions).
Dynamically shows/hides the appropriate widget per question type.

## Public API

```python
class ExamGuiCombined:
    def __init__(self,
                 questions: list[Question],
                 is_random: bool = False,
                 n_questions: int | None = None) -> None
    def run(self) -> None
```

## Factory

```python
Factory.test() -> ExamGuiCombined        # 2 text + 2 options
Factory.combined(is_random, n_questions)  # Hebrew + Options sheets
```

## Reused Components

| Component | From |
|-----------|------|
| `ExamRunner` | `f_quiz.exam_gui.runner` |
| `WidgetQuestion` | `f_quiz.exam_gui.widgets.question` |
| `WidgetAnswer` | `f_quiz.exam_gui.widgets.answer` |
| `WidgetOptions` | `f_quiz.exam_gui.widgets.options` |
| `WidgetStatus` | `f_quiz.exam_gui.widgets.status` |

## Dependencies

| Import | Purpose |
|--------|---------|
| `tkinter` | GUI framework |
| `f_quiz.question.Question` | Base question type |
| `f_quiz.question_options.QuestionOptions` | Options question type |
| `f_quiz.exam_gui.runner.ExamRunner` | Exam logic |
| `f_quiz.exam_gui.widgets.*` | Shared widgets |
| `f_quiz.loaders.u_gsheet` | Google Sheets loaders |
