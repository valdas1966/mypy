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

---

## Task: Fill Wrong Column (Options Sheet)

### When to Run
- **Automatically** — when working on the Options sheet and
  empty cells are found in column D (Wrong).
- **On demand** — when the user asks to fill wrong answers.

### Goal
Fill empty cells in column D ("Wrong") of the **Options** sheet
with wrong answers based on **polarity** — the opposite meaning
of the correct answer in column C.

### Sheet Access

Use gspread directly (do NOT import from `f_google` — the import
chain pulls in optional dependencies that may be missing):

```python
import gspread
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import os

path_token = os.environ['VALDAS_TOKEN_PATH']
creds = Credentials.from_authorized_user_file(
    filename=path_token,
    scopes=['https://www.googleapis.com/auth/spreadsheets']
)
if creds.expired and creds.refresh_token:
    creds.refresh(Request())
    with open(path_token, 'w') as f:
        f.write(creds.to_json())

gc = gspread.authorize(creds)
spread = gc.open_by_key(
    '1_aKGiiAdxVqZwXiTjiX4FAqCl0g3sCL7gSJg9ro06tU'
)
ws = spread.worksheet('Options')
rows = ws.get_all_values()
```

### Sheet Layout

| Col | Idx | Header   | Content                        |
|-----|-----|----------|--------------------------------|
| A   | 0   | Full     | Original full sentence         |
| B   | 1   | Question | Sentence with one word masked  |
| C   | 2   | Correct  | The masked word (right answer) |
| D   | 3   | Wrong    | Opposite/polarity word (fill)  |

Row 0 = header. Data starts at row 1.

### Polarity Strategy

The wrong answer is the **opposite** of the correct answer:

| Correct | Wrong | Pattern |
|---------|-------|---------|
| valid | invalid | antonym |
| formal | informal | opposite prefix |
| has | lacks | verb antonym |
| both | neither | quantifier flip |
| dependent | independent | opposite prefix |
| express | conceal | verb antonym |
| and | or | conjunction swap |
| is | was | tense swap |
| can | cannot | polarity swap |
| The | A | determiner swap |
| with | without | preposition flip |

**Rules:**
- Wrong answer = opposite/antonym of correct answer.
- Match capitalization and punctuation of the correct answer.
- Skip rows where column C (Correct) is empty.

### Batch Write

```python
cells = []
for row_1based, value in wrong_answers.items():
    cells.append(
        gspread.Cell(row=row_1based, col=4, value=value)
    )
ws.update_cells(cells)
```

Row numbers are 1-based (row 1 = header, row 2 = first data).
Column 4 = column D (Wrong).
