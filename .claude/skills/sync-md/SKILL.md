---
name: sync-md
description: >-
  Reconcile CLAUDE.md docs with manual code changes under a given local
  path — read the current code (source of truth) against each folder's
  existing CLAUDE.md, then update/create the stale ones per
  for_claude_md.md. Trigger when the user says "sync md", "update
  CLAUDE.md for <path>", "refresh CLAUDE docs after my changes", or hands
  a path of manual edits to document. Runs in ultrathink mode.
---

# Sync CLAUDE.md to manual code changes

**Run in ultrathink mode** — reason at maximum depth throughout; change
analysis and doc edits must be deliberate, not mechanical.

Input: a local `<path>` (file or folder) where manual code changes were
made. If `<path>` is a file, treat its containing folder as the scope
root. If no path was given, ask for one before proceeding.

**Detection model — no git.** The current code on disk is the source of
truth; each folder's existing `CLAUDE.md` is the baseline. "Recognize the
changes" = find where the code and its `CLAUDE.md` diverge.

## Steps

1. **Enumerate in-scope folders** under `<path>`: the scope root and, if
   it is a directory, every subfolder. Keep only folders that hold a
   class or utility module (`main.py`, `__init__.py`, `_factory.py`,
   `_tester.py`, `u_*.py`, `c_*.py`). **Skip script-only** folders
   (`_study.py`, `s_*.py`, `experiments/`, `benchmark/`, `scripts/`,
   `study/`) — they need no `CLAUDE.md`.

2. **Detect divergences** per in-scope folder. Read the current code in
   full and the existing `CLAUDE.md` (if any), then identify what no
   longer matches: new/renamed/removed public API or classes, changed
   signatures, new/removed dependencies, new/deleted modules, moved
   files. A renamed/removed symbol shows up as a doc entry absent from
   the code.

3. **Update each divergent folder's `CLAUDE.md`** to match the current
   code, following `.claude/instructions/docs/for_claude_md.md` (5 mandatory
   sections: Purpose, Public API, Inheritance, Dependencies, Usage
   example). Create it if missing. Fix only what diverged; stay accurate
   to the code — never invent. Remove or repoint stale (renamed/deleted)
   entries.

4. **Propagate upward.** If the change altered public surface or
   structure that a parent/aggregator `CLAUDE.md` (or the root hub
   `CLAUDE.md`) documents — e.g. a new/removed public class in an
   aggregated package — update those too.

5. **Never touch** `CLAUDE.html`, `CLAUDE_REVIEW.html`, or `ABOUT.html`
   — those are generated on explicit request only.

6. **Report**: list the **full absolute path** of every `CLAUDE.md`
   created/updated, each with a one-line summary of what changed; note
   any folders skipped as script-only.
