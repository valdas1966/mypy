# Exam

## Purpose
Interactive quiz exam. Prompts the user with questions in the terminal,
checks answers, and displays results. Supports shuffling and limiting
the number of questions.

## Public API

```python
class Exam:
    def __init__(self,
                 questions: list[Question],
                 is_random: bool = False,
                 n_questions: int | None = None) -> None
    @property
    def questions(self) -> list[Question]
    def run(self) -> None
```

| Param | Type | Default | Behavior |
|-------|------|---------|----------|
| `questions` | `list[Question]` | required | Full question pool |
| `is_random` | `bool` | `False` | Shuffle questions before running |
| `n_questions` | `int \| None` | `None` | Limit to first N questions (after shuffle) |

## Factory

```python
Factory.two_capitals() -> Exam          # 2 capital city questions
Factory.two_capitals_random() -> Exam   # 2 capitals, shuffled
Factory.two_capitals_n(n_questions) -> Exam  # limited to n questions
Factory.hebrew() -> Exam                # from Google Sheet
```

## Dependencies

| Import | Purpose |
|--------|---------|
| `f_quiz.question.Question` | Question class |
| `random` | Shuffling questions |
