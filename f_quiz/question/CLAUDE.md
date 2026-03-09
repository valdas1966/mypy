# Question

## Purpose
Quiz question with text and answer.

## Public API

```python
class Question:
    def __init__(self, text: str, answer: str) -> None
    @property
    def text(self) -> str
    @property
    def answer(self) -> str
    def __str__(self) -> str  # 'text -> answer'
```

## Factory

```python
Factory.a() -> Question  # 'Capital of France' / 'Paris'
Factory.b() -> Question  # 'Capital of Germany' / 'Berlin'
```

## Dependencies
None.
