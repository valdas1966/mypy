# loaders

## Purpose
Load quiz questions from external sources into DataFrames.

## Structure

| File | Purpose |
|------|---------|
| `u_gsheet.py` | Load questions from Google Sheet |
| `_tester.py` | pytest tests for u_gsheet |

## Public API

### u_gsheet

```python
def load(sheet_name: str = 'Hebrew') -> list[Question]
def load_options(sheet_name: str = 'Options') -> list[QuestionOptions]
def load_yes_no(sheet_name: str = 'YesNo') -> list[QuestionYesNo]
def load_visual(sheet_name: str = 'Visual') -> list[QuestionVisual]
```
Reads the questions spreadsheet via `Spread.Factory.questions()`,
treats the first row as headers.

## Dependencies

| Import | Purpose |
|--------|---------|
| `f_google.services.sheets.Spread` | Google Sheets access |
| `f_quiz.question.Question` | Question class |
| `f_quiz.question_options.QuestionOptions` | Two-option question |
| `f_quiz.question_yes_no.QuestionYesNo` | Yes/No question |
| `f_quiz.question_visual.QuestionVisual` | Diagram-based question |
