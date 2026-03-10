# ExamRunner

## Purpose
Pure exam logic with no GUI dependency. Manages question sequence,
answer checking, and score tracking.

## Public API

```python
class ExamRunner:
    def __init__(self,
                 questions: list[Question],
                 is_random: bool = False,
                 n_questions: int | None = None) -> None
    @property
    def current(self) -> Question | None
    @property
    def number(self) -> int
    @property
    def total(self) -> int
    @property
    def score(self) -> int
    @property
    def is_finished(self) -> bool
    def check(self, answer: str) -> bool
```

## Factory

```python
Factory.two_capitals() -> ExamRunner
Factory.two_capitals_random() -> ExamRunner
Factory.two_capitals_n(n_questions) -> ExamRunner
```

## Dependencies

| Import | Purpose |
|--------|---------|
| `f_quiz.question.Question` | Question class |
| `random` | Shuffling questions |
