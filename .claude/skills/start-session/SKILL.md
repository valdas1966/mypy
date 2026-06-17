---
name: start-session
description: >-
  Start or continue a named work session whose summary lives on Google Drive
  (MyPy project). Trigger when the user says "start session '<name>'", "new
  session", "open session '<name>'", or otherwise begins a named session.
  Reads Drive Instructions, finds & continues a prior same-named session,
  creates today's skeleton on Drive, and reports back the prior context.
  To save / close / summarize a session instead, use the finish-session skill.
---

# Start a session

Begin (or continue) a named work session. Summaries live on Google Drive at:

```
YYYY/MM/DD/<name>_session.md
```

Names are **flat** (e.g. `skills`, `drive_refactor`) — keep the current
folder/file convention; do not introduce nested paths.

**Helper script** (run from anywhere in the repo):

```bash
python .claude/skills/_session_lib/session.py find   <name>
python .claude/skills/_session_lib/session.py read   <drive_path>
python .claude/skills/_session_lib/session.py create <name> <YYYY-MM-DD> <local_md>
```

Today's date is in your context (`currentDate`) — pass it to `create`;
do not rely on the machine clock.

## Steps

1. **Acknowledge** the session name.

2. **Read Drive instructions** (never cache — always re-read). At minimum:
   ```bash
   python .claude/skills/_session_lib/session.py read Instructions/For_Session_Summary.md
   ```
   Also read `For_Summary.md` / `For_Tex.md` if the session will touch
   paper summaries or LaTeX.

3. **Find prior same-named sessions**:
   ```bash
   python .claude/skills/_session_lib/session.py find <name>
   ```
   Branch on the output:
   - **EXACT match(es)** → continue automatically. `read` the
     `MOST_RECENT` file to restore context; announce the date you are
     continuing from. If it is a skeleton (`SKELETON: True`), also read
     the most recent *substantive* file in the EXACT list.
   - **No exact, but a SIMILAR name** (typo / substring) → **ask** the
     user whether to continue it. Do not assume.
   - **No match** → fresh session.

4. **Create today's skeleton**:
   - Write the skeleton (template below) to `/tmp/<name>_session.md`.
     If continuing, seed Purpose / What We Built / Next Steps from the
     prior summary. Today's date folder is used even when continuing —
     the prior file stays intact.
   - Upload:
     ```bash
     python .claude/skills/_session_lib/session.py create <name> <currentDate> /tmp/<name>_session.md
     ```
   - `.md` only — no `.tex` / `.pdf` at session start.

5. **Report back**, leading with the outcome:
   - **S1 (mandatory):** which session started, today's date, and the
     prior date being continued (or "fresh session").
   - **S2–S5 (optional, drop if no value):** recap of prior session,
     where it ended, recommended starting point for today.
   - If the immediately-prior file is a skeleton, recap the most recent
     *substantive* session instead and flag the skeleton in S1.

6. **Track** throughout the session — key decisions & reasoning, what was
   built, design choices, open issues — so finish-session is accurate.

## Skeleton template

```markdown
# <name>

**Date:** <currentDate>
**Project path:** /Users/eyalberkovich/mypy

---

## Purpose

<one paragraph — seed from prior summary if continuing>

---

## What We Built

_(to be filled in as work proceeds)_

---

## Architecture

_(to be filled in as work proceeds)_

---

## Style & Methodology

_(to be filled in as work proceeds)_

---

## Next Steps

<carry over unchecked items from the prior summary, or TBD>

---

## How to Resume

1. Read this file from Drive at `YYYY/MM/DD/<name>_session.md`.
2. Prior sessions: <list with one-line each>.
3. Key paths / Drive assets for this session.
```

## Notes

- All Drive ops use `Drive.Factory.valdas()` (VALDAS OAuth) via the helper.
- If a needed Drive instruction file is missing, list `Instructions/` and
  confirm — new files may have been added.
- If a Drive instruction conflicts with project `CLAUDE.md`, Drive wins.
