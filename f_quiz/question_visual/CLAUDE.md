# QuestionVisual

## Purpose
Quiz question backed by a diagram (SVG) with one masked label.
Extends `QuestionOptions` — the user picks the correct label from
two options. The SVG lives on Google Drive under `Quiz/Visuals/`.

## Public API

```python
class QuestionVisual(QuestionOptions):
    def __init__(self,
                 topic: str,
                 svg_path: str,
                 masked_label: str,
                 answer: str,
                 wrong: str) -> None
    @property
    def topic(self) -> str
    @property
    def svg_path(self) -> str
    @property
    def masked_label(self) -> str
```

## Inheritance

```
Question (text, answer)
  └── QuestionOptions (+ wrong, options)
        └── QuestionVisual (+ topic, svg_path, masked_label)
```

## Factory

```python
Factory.argument_anatomy() -> QuestionVisual
Factory.modus_ponens()     -> QuestionVisual
```

## Storage

- SVGs on Google Drive at `Quiz/Visuals/NN_name.svg`.
- Metadata on the `Visual` tab of the quiz spreadsheet:
  `Id | Topic | SvgPath | MaskedLabel | Correct | Wrong`.

## Dependencies

| Import | Purpose |
|--------|---------|
| `f_quiz.question_options.QuestionOptions` | Base class |
