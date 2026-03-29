# QuestionYesNo

## Purpose
Quiz question with fixed Yes/No answer options.
Options are always displayed in fixed order: Yes (left), No (right).
The participant guesses whether the statement is true or false.

## Public API

```python
class QuestionYesNo(QuestionOptions):
    def __init__(self, text: str, answer: str) -> None
    @property
    def options(self) -> list[str]  # always ['Yes', 'No']
```

Inherited from `QuestionOptions`:
```python
@property
def wrong(self) -> str       # auto-derived: opposite of answer
def __str__(self) -> str     # 'text -> answer | wrong'
```

Inherited from `Question`:
```python
@property
def text(self) -> str
@property
def answer(self) -> str
```

## Inheritance (Hierarchy)

```
Question (text, answer)
  └── QuestionOptions (+ wrong, options — shuffled)
        └── QuestionYesNo (options fixed: ['Yes', 'No'])
```

- `Question`: provides `text` and `answer`
- `QuestionOptions`: provides `wrong` and `options` (shuffled)
- `QuestionYesNo`: overrides `options` to fixed order, derives `wrong` automatically

## Factory

```python
Factory.yes() -> QuestionYesNo   # answer='Yes'
Factory.no()  -> QuestionYesNo   # answer='No'
```

## Dependencies

| Import | Purpose |
|--------|---------|
| `f_quiz.question_options.QuestionOptions` | Base class |

## Usage Examples

```python
from f_quiz.question_yes_no import QuestionYesNo

q = QuestionYesNo(text='Logic is formal study', answer='Yes')
q.options   # ['Yes', 'No'] — always fixed order
q.answer    # 'Yes'
q.wrong     # 'No'
```
