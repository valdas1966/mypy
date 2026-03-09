# Exam

## Purpose
Interactive quiz exam. Prompts the user with questions in the terminal,
checks answers, and displays results.

## Public API

```python
class Exam:
    def __init__(self, questions: list[Question]) -> None
    @property
    def questions(self) -> list[Question]
    def run(self) -> None
```

## Factory

```python
Factory.two_capitals() -> Exam  # 2 capital city questions
```

## Dependencies

| Import | Purpose |
|--------|---------|
| `f_quiz.question.Question` | Question class |
