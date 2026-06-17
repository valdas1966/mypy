# Instruction to AI Agent (Claude Code): Write a Skill

A skill lives at `.claude/skills/<name>/`. Read this before creating or
editing any `SKILL.md`. Goal: the **most minimal `SKILL.md` that still
passes the correct message** — minimal, never gutted.

## Two files, two audiences

- `SKILL.md` — **Claude-facing instructions.** Loaded and executed when
  the skill runs. Keep it minimal: only lines that change what Claude
  does. Required.
- `ABOUT.html` — **human-facing** visual explainer. Where "why",
  philosophy, motivation, and examples live. Optional, on demand.

Rule of thumb: a line that tells a *human why* → `ABOUT.html`. A line
that tells *Claude what to do* → `SKILL.md`.

## Frontmatter (the only always-loaded part)

`description` is injected into every session's skill list — it is the
trigger and costs tokens permanently. Make it tight but complete:

- `name`: kebab-case, matches the folder.
- `description`: one sentence of *what it does* + the trigger phrases
  ("Trigger when the user says …"). No body detail — that loads lazily
  only when the skill runs.

## Body — minimal and imperative

Include only what changes behavior at run time:

- Imperative steps ("Lead with the answer", "Upload to …"), not prose.
- Keep all concrete commands, paths, schemas, and tables.
- Guardrails as single lines ("If already concise, say so").

Cut: philosophy, motivation, restating the description, narration,
"this is useful because …". A step should never need a paragraph of
justification to be followed.

## The litmus test

Delete any line where removing it would not change what Claude does.
If that line is still worth saying to a *human*, move it to `ABOUT.html`.

## Minimal ≠ gutted

Necessary procedure is not padding. A workflow skill (e.g. a Drive
lifecycle) legitimately needs every step, command, and template — keep
them all. Trim only non-behavioral content, never required instruction.
