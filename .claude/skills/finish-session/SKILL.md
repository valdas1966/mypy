---
name: finish-session
description: >-
  Save, close, summarize, or end the current named work session by writing
  its summary to Google Drive (MyPy project). Trigger when the user says
  "save the session", "close session", "summarize the session", "finish
  session", or "end session", or when a meaningful chunk of work is done.
  Writes the full summary per Drive's For_Session_Summary.md format and
  uploads it. To start or continue a session instead, use start-session.
---

# Finish a session

Write and upload the end-of-session summary. Summaries live on Google Drive
at `YYYY/MM/DD/<name>_session.md` (flat names).

**Helper script** (run from anywhere inside the repo — it self-locates the
repo root for the `f_google` import):

```bash
python .claude/skills/_session_lib/session.py read   <drive_path>
python .claude/skills/_session_lib/session.py create <name> <YYYY-MM-DD> <local_md>
```

Today's date is in your context (`currentDate`) — pass it to `create`.

## Steps

1. **Re-read** the summary format (never cache — it may have changed):
   ```bash
   python .claude/skills/_session_lib/session.py read Instructions/For_Session_Summary.md
   ```
   Follow its section structure exactly.

2. **Write** the full summary to `/tmp/<name>_session.md` — fill in
   Purpose, What We Built, Architecture, Style & Methodology, Next Steps
   (`- [ ]` checkboxes), How to Resume. Replace every
   `_(to be filled in ...)_` placeholder with real content.

3. **Upload** to today's date folder:
   ```bash
   python .claude/skills/_session_lib/session.py create <name> <currentDate> /tmp/<name>_session.md
   ```

4. **TeX / PDF only on explicit request** — follow the "On-Demand: TeX and
   PDF Exports" section of `For_Session_Summary.md` (write `.tex`,
   `tectonic` compile, upload both). Do not generate proactively.

5. **No local saves** — `/tmp/` only; do not auto-open the PDF.

## Notes

- All Drive ops use `Drive.Factory.valdas()` (VALDAS OAuth) via the helper.
- If a Drive instruction conflicts with project `CLAUDE.md`, Drive wins.
- The summary's primary audience is the *next* session (human or AI) — make
  it resumable: someone with zero prior context should be able to pick up.
