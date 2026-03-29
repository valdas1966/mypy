# Fill Wrong Column — Instructions for Claude Code

## Goal

Fill empty cells in column D ("Wrong") of the **Options** sheet
in the Questions Google Spreadsheet.
Each "Wrong" value should be a semantically confusing alternative
to the corresponding "Correct" value in column C — designed to
challenge an exam participant choosing between two options.

## Quick Steps

1. **Read the sheet** via gspread (bypass `f_google` imports).
2. **Find rows** where column C (Correct) is non-empty
   but column D (Wrong) is empty.
3. **Generate wrong answers** using the strategy below.
4. **Batch-write** all wrong answers to column D.
5. **Verify** by re-reading a sample of updated rows.

## Access — Google Sheets via gspread

Do NOT import from `f_google` — the import chain pulls in
optional dependencies (vertexai, pymupdf4llm) that may be missing.
Use gspread directly:

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
spread = gc.open_by_key('1_aKGiiAdxVqZwXiTjiX4FAqCl0g3sCL7gSJg9ro06tU')
ws = spread.worksheet('Options')
rows = ws.get_all_values()
```

## Sheet Layout

| Column | Index | Header   | Content                        |
|--------|-------|----------|--------------------------------|
| A      | 0     | Full     | Original full sentence         |
| B      | 1     | Question | Sentence with one word masked  |
| C      | 2     | Correct  | The masked word (right answer) |
| D      | 3     | Wrong    | Confusing alternative (to fill)|

- Row 0 is the header row.
- Data starts at row 1.

## Wrong-Answer Generation Strategy

The wrong answer must **confuse** a participant who hasn't studied,
but be clearly wrong to someone who has. Use these patterns:

### By Word Type

| Type | Strategy | Examples |
|------|----------|---------|
| Content nouns | Domain-related but wrong | proposition/assumption, Logic/Intuition, origins/endings |
| Adjectives | Antonym or opposite prefix | formal/informal, valid/invalid, independent/dependent, same/different |
| Verbs | Antonym or plausible alternative | express/conceal, has/lacks, shows/hides, depends/reflects |
| Determiners | Swap with similar | The/A, a/no, Every/No, the/a |
| Auxiliary verbs | Tense or polarity swap | is/was, can/cannot, must/might |
| Prepositions | Wrong but plausible | of/about, on/beyond, from/into, to/for, with/without |
| Conjunctions | Swap | and/or, or/and |
| Quantifiers | Opposite | both/neither, either/neither, only/also, multiple/single |
| Possessives | Number swap | its/their |
| Proper nouns | Same category, different | Greece/Egypt, India/Japan, Latin/Greek, Boolean/Integer |
| Numbers | Close but wrong | 2/3, 4/5, II/III, IV/VI |
| Hyphenated terms | Flip the concept | truth-value/truth-label, non-contingent/contingent, three-valued/two-valued |

### Rules

- **Never use a synonym** — the wrong answer must be wrong.
- **Match capitalization** of the correct answer.
- **Match punctuation** (e.g., if correct has apostrophe, wrong should too).
- **Skip rows** where column C (Correct) is empty — these are
  broken rows from token-splitting issues in `generate_options.py`.
- **Be consistent** — if "proposition" always maps to "assumption",
  keep that mapping across all sentences.

## Writing Back — Batch Update

```python
cells = []
for row_1based, value in wrong_answers.items():
    cells.append(gspread.Cell(row=row_1based, col=4, value=value))
ws.update_cells(cells)
```

Use `update_cells` for batch efficiency (single API call).
Row numbers are 1-based (row 1 = header, row 2 = first data row).
Column 4 = column D (Wrong).

## Verification

After writing, re-read and print a sample:

```python
rows = ws.get_all_values()
for i in [sample_indices]:
    print(f'Row {i}: Correct={rows[i][2]!r}, Wrong={rows[i][3]!r}')
```

## Related Files

| File | Purpose |
|------|---------|
| `f_quiz/scripts/generate_options.py` | Generates rows A-C (do NOT modify) |
| `f_quiz/loaders/u_gsheet.py` | Loads QuestionOptions: text=B, answer=C, wrong=D |
| `f_quiz/question_options/main.py` | QuestionOptions(text, answer, wrong) |
| `f_google/services/sheets/spread/_factory.py` | Spread.Factory.questions() — spreadsheet ID |
