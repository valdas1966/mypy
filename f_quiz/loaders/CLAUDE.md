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
```
Reads the questions spreadsheet via `Spread.Factory.questions()`,
treats the first row as headers, returns a list of Question objects.

## Dependencies

| Import | Purpose |
|--------|---------|
| `f_google.services.sheets.Spread` | Google Sheets access |
| `f_quiz.question.Question` | Question class |
