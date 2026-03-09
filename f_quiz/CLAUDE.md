# f_quiz

## Purpose
Quiz framework. Loads quiz questions from external sources,
models them as Question objects, and runs interactive exams.

## Structure

| Path | Purpose |
|------|---------|
| `question/` | Question class (text + answer) |
| `exam/` | Exam class (interactive quiz runner) |
| `loaders/` | Load questions from external sources |

## Dependencies

| Import | Purpose |
|--------|---------|
| `pandas` | DataFrame creation (loaders) |
| `f_google.services.sheets.Spread` | Google Sheets access (loaders) |
