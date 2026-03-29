# f_quiz

## Purpose
Quiz framework. Loads quiz questions from external sources,
models them as Question objects, and runs interactive exams.

## Structure

| Path | Purpose |
|------|---------|
| `question/` | Question class (text + answer) |
| `question_options/` | QuestionOptions(Question) — two-option answer |
| `question_yes_no/` | QuestionYesNo(QuestionOptions) — fixed Yes/No |
| `exam/` | Exam class (terminal quiz runner) |
| `exam_gui/` | ExamGui class (tkinter GUI quiz runner) |
| `exam_gui_options/` | ExamGuiOptions (two-option GUI quiz) |
| `exam_gui_combined/` | ExamGuiCombined (mixed text + options GUI) |
| `loaders/` | Load questions from external sources |
| `sheets/` | Instructions for Claude Code (sheet tasks) |

## Dependencies

| Import | Purpose |
|--------|---------|
| `pandas` | DataFrame creation (loaders) |
| `f_google.services.sheets.Spread` | Google Sheets access (loaders) |
