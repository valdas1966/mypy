# QuestionOptions

## Purpose
Quiz question with two answer options (correct and wrong).
Extends Question — fully compatible with ExamRunner and ExamGui.

## Public API

```python
class QuestionOptions(Question):
    def __init__(self, text: str, answer: str, wrong: str) -> None
    @property
    def wrong(self) -> str
    @property
    def options(self) -> list[str]  # [answer, wrong] shuffled
```

## Inheritance

```
Question (text, answer)
  └── QuestionOptions (+ wrong, options)
```

## Factory

```python
Factory.logic() -> QuestionOptions
Factory.formal() -> QuestionOptions
```

## Dependencies

| Import | Purpose |
|--------|---------|
| `f_quiz.question.Question` | Base class |
| `random` | Shuffle options order |
