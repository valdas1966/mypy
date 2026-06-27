# MyPy Framework — Coding Conventions

This file is the **hub**: the always-loaded introduction and conventions
index. Detailed, task-specific procedures live in `.claude/instructions/`
— read the relevant guide **before** starting that task.

## Task-Specific Guides

When you are about to do one of these tasks, read its guide under
`.claude/instructions/` first (this index is the map; each section below
also links its guide inline). The top level splits into three folders —
`code/` (how to write MyPy code), `docs/` (generating CLAUDE/ABOUT docs),
and `meta/` (external tools, formats, reference); `code/` itself
sub-folders by topic into `layout/` (module skeleton), `style/`
(line-level), and `design/` (class design & quality):

**`code/layout/` — module skeleton: folders, names, import wiring**

| About to… | Read |
|---|---|
| Lay out a module (folders, file roles) | `code/layout/for_structure.md` |
| Name a folder / file / class / var (prefixes, case) | `code/layout/for_naming.md` |
| Write imports / an `__init__.py` | `code/layout/for_imports.md` |

**`code/style/` — line-level: formatting, docstrings, logging**

| About to… | Read |
|---|---|
| Write a docstring / inline comment (`=`-separator) | `code/style/for_docstrings.md` |
| Format code / annotate types / clean-code statements | `code/style/for_code_style.md` |
| Add logging to a module | `code/style/for_logging.md` |

**`code/design/` — class design, reuse & validation**

| About to… | Read |
|---|---|
| Write new code (reuse-first check) / build a class | `code/design/for_new_class.md` |
| Apply a design pattern | `code/design/for_patterns.md` |
| Write tests (`_tester.py`) | `code/design/for_testing.md` |

**`docs/` — CLAUDE & ABOUT documentation**

| About to… | Read |
|---|---|
| Add or update a `CLAUDE.md` | `docs/for_claude_md.md` |
| Generate `CLAUDE.html` | `docs/for_claude_html.md` |
| Generate `CLAUDE_REVIEW.html` | `docs/for_claude_review.md` |
| Generate `ABOUT.html` | `docs/for_about_html.md` |

**`meta/` — tools, formats, reference**

| About to… | Read |
|---|---|
| Write or edit a skill | `meta/for_skill.md` |
| Do any Google Drive operation | `meta/for_drive.md` |
| Write or edit LaTeX (`.tex`) | `meta/for_tex.md` |
| Look up a domain abbreviation | `meta/for_glossary.md` |

---

## Clarify Before Acting
Before starting a task that involves code changes or design decisions, if
the prompt is ambiguous, underspecified, or open to multiple
interpretations, ask clarifying questions first. Do not assume intent —
confirm it. For straightforward operational tasks (run tests, commit,
format, etc.) proceed directly without asking.

## Project Structure

Framework modules use the `f_` prefix (`f_core`, `f_ds`, `f_search`,
`f_google`, …); inside a module, `i_X_name/` folders encode inheritance
depth (`i_0_` = abstract base). Each class module holds a subset of a
standard file set (`main.py`, `__init__.py`, `_factory.py`, `_tester.py`,
`_from.py`, `_to.py`, `CLAUDE.md`, …; `_`-prefixed = private). Full
hierarchy diagram + file-role table:
`.claude/instructions/code/layout/for_structure.md`.

---

## Naming Conventions

Full prefix tables + finer rules:
`.claude/instructions/code/layout/for_naming.md`. Essentials:

- **Folders**: `f_` framework module, `i_X_` inheritance level
  (`i_0_` = abstract base), `_internal/` private helpers, (none) =
  domain grouping (`algos/`, `problems/`).
- **Files**: `u_` utility (functions), `c_` component/service wrapper,
  `_` private (`_factory.py`, `_tester.py`), (none) = public
  (`main.py`).
- **Classes**: PascalCase; bases `*Base` or in `i_0_base/`; mixins are
  adjectives (`Comparable`, `HasRowCol`); enums `TypeComparison`.
- **Functions/vars**: snake_case; single `_` prefix = private;
  `UPPER_CASE` public / `_UPPER_CASE` private constants; a plural
  producer is suffixed `_many` and takes a `many: int` count.
- **Type vars**: PascalCase with bound —
  `State = TypeVar('State', bound=StateBase)`.

---

## Docstring Conventions

Width table + worked examples:
`.claude/instructions/code/style/for_docstrings.md`. Essentials:

- `=`-separator docstrings; the `=` count keeps total width at 80, so it
  shrinks with indentation: module 80 / class 76 / method 72.
- Short inline comments sit **above** the line they describe.

---

## Code Style

Worked examples, class-definition order, full clean-code rule:
`.claude/instructions/code/style/for_code_style.md`. Essentials:

### Type Annotations
- Annotate all params and returns; `-> None` when returning nothing.
- Modern union syntax `type | None` (not `Optional`); lowercase generics
  `dict[str, Any]`, `list[str]`.
- Prefer `typing.Self` (PEP 673) for the enclosing class's own instances
  (`-> Self`, `child: Self`, `other: Self` in domain methods);
  comparison/`__eq__` dunders keep `other: object`.

### Formatting
- 4-space indent, no tabs; 80-char lines; multi-line params align with
  the opening paren.
- f-strings preferred; pass named arguments —
  `data.set_best_to_be_parent_of(state=state)`.

### Clean Code
- Decompose nested/complex statements into simple named steps —
  `cell = Cell(row=0, col=0)`; `state = State(cell=cell)` — not a
  constructor nested in another call's argument. Trigger is nesting, not
  single-use; keep simple calls (`len(items)`) inline.

---

## Design Patterns

Full examples: `.claude/instructions/code/design/for_patterns.md` — read it before
applying one. The canonical patterns:

- **Factory** — class declares `Factory: type = None`; the real Factory
  lives in `_factory.py` and is wired in `__init__.py`.
- **Mixin Composition** — prefer mixins (adjectives) over deep
  inheritance: `class CellBase(HasRowCol, HasName)`.
- **Template Method** — base defines lifecycle hooks (`_pre_run`,
  `_post_run`, `_init_add_atts`); subclasses override.
- **Generics** — parameterize with `Generic[...]`.
- **Comparison Operators** — implement all four explicitly, delegating to
  `key` (no `@total_ordering` overhead).
- **Dataclasses vs manual `__init__`** — `@dataclass` for data holders;
  manual `__init__` for behavior-rich classes. No `attrs`.
- **Error Handling** — built-in exceptions only (`ValueError`, …);
  capture partial-failure errors as strings.
- **Async** — not used; the codebase is synchronous.

---

## Writing New Code — Reuse-First Check

Before writing **any** new code, run this 3-tier check in order. It is a
pre-coding gate, same category as *Clarify Before Acting*. Full procedure
for classes (tables, rule-of-three, decision cheat-sheet):
`.claude/instructions/code/design/for_new_class.md`.

1. **Reuse first** — if the capability already exists in the codebase
   (`f_core/mixins/`, `f_core/recorder/`, `f_ds/`, `f_psl/`, or any
   `u_*`/`c_*` utility), USE IT by import / inheritance / composition.
   Never reimplement identity, equality, ordering, serialization,
   validation, event capture, or heap/container ops.
2. **Exists but not good enough → propose to improve it** — don't
   silently work around, fork, or duplicate existing code. Surface the
   gap and propose improving the existing code in place; **wait for OK**
   before a non-trivial change.
3. **Missing and broadly useful → propose core/infra, don't silently
   build** — if it would serve many tasks/contexts (rule of three: ≥3
   sites hand-roll it, or foundational with ≥2 reusers), propose
   extracting shared infrastructure into `f_core`/`f_ds`/`f_psl` and
   **wait for explicit user OK**. If it's one-off, write it inline
   (YAGNI).

---

## Testing Conventions

Tests live in `_tester.py` alongside `main.py` (pytest). Full
conventions and examples: `.claude/instructions/code/design/for_testing.md`.
Essentials:

- Test functions `test_<method_name>()`; each has a `=`-separator
  docstring.
- Prefer `MyClass.Factory.a()` directly in the test over a
  `@pytest.fixture` that only wraps it — use fixtures only for real
  setup/teardown, parametrization, or scope.

---

## Import Conventions

Full guide (aggregator vs direct, `ULazy`, `__init__.py` patterns):
`.claude/instructions/code/layout/for_imports.md`. Essentials:

- **Import order (PEP 8):** stdlib → third-party → framework, groups
  blank-line separated; absolute imports throughout.
- **Aggregator and direct imports are both first-class** — aggregators
  are lazy (`ULazy`), so equally cascade-immune.
- **Never put business logic in `__init__.py`.**

---

## Domain Abbreviations

Domain abbreviations (SPP, OMSPP, MMSPP, BFS, HS, DS, CS, PSL, GUI) are
defined in `.claude/instructions/meta/for_glossary.md`.

---

## Environment

- Python 3.13+ (Conda)
- Testing: pytest
- Logging: `f_log` — module-level `_log = get_log(__name__)`; full
  convention: `.claude/instructions/code/style/for_logging.md`
- No linter config — follows PEP 8 by convention
- Package name: `MyPy`

---

## CLAUDE Documentation Rule

### Auto-update: CLAUDE.md
Every code change MUST update the `CLAUDE.md` file in each folder that contains at least one changed file. Follow `.claude/instructions/docs/for_claude_md.md`. If `CLAUDE.md` does not exist in the folder, create it.

### On demand: CLAUDE.html and CLAUDE_REVIEW.html
`CLAUDE.html` and `CLAUDE_REVIEW.html` are generated **only when the user explicitly requests** them. These files are for human reading — Claude reads only `CLAUDE.md`. Follow `docs/for_claude_html.md` / `docs/for_claude_review.md` (and `docs/for_about_html.md` for `ABOUT.html`); those guides cover the visual style and the AI-generated-image workflow.

### Scope: Which folders get CLAUDE files
CLAUDE files are required **only** for folders containing class modules or utility modules:
- `main.py`, `__init__.py`, `_factory.py`, `_tester.py` — class modules
- `u_*.py` — utility modules
- `c_*.py` — component/service wrappers

CLAUDE files are **NOT** required for folders that only contain scripts:
- `_study.py`, `s_*.py` — study / exploratory scripts
- `experiments/`, `benchmark/`, `scripts/` — experiment folders
- `study/` — research folders

### Review suggestions
Suggestions from `CLAUDE_REVIEW.html` must be presented as a plan first. Only apply after explicit user approval.

---

## Google Drive

Full operations guide: `.claude/instructions/meta/for_drive.md`. Open with
`Drive.Factory.valdas()` (VALDAS OAuth). Non-negotiable rules:

- **Read Drive `Instructions/` first** — before ANY Drive op, read the
  relevant `Instructions/For_*.md` from Drive. Never cache across
  sessions; if a Drive instruction conflicts with this file, **Drive
  wins**.
- **Drive-only** — never save Drive files into the project directory; use
  `/tmp/` for all intermediates; do not auto-open files (the user views
  them on Drive).

---

## LaTeX Files

Full conventions: `.claude/instructions/meta/for_tex.md` (local) and Drive
`Instructions/For_Tex.md` (authoritative — read first; Drive wins).

Hard requirement: every `.tex` created or edited under this project
**must** define the `\me{...}` (red, author) / `\you{...}` (blue, AI)
annotation macros in its preamble, and you must act on inline `\me{...}`
notes on every read (execute imperatives; answer questions with a
one-sentence `\you{...}`). Both rules are specified in `for_tex.md`.

---

## Session Management

Session lifecycle = two skills under `.claude/skills/`: **`start-session`**
(start/continue) and **`finish-session`** (save/close/summarize). The
skills are the authoritative workflows — triggers and steps live in their
`SKILL.md`. Summaries live on Drive at `YYYY/MM/DD/<name>_session.md`
(flat names); the Google Drive rules above apply.

---

## Writing Skills

Before creating or editing **any** skill (`.claude/skills/<name>/SKILL.md`),
read `.claude/instructions/meta/for_skill.md` first. It is the authoritative
guide for skill content.

Core rule: a `SKILL.md` must be the **most minimal text that still passes
the correct message** — only lines that change what Claude does at run
time. `SKILL.md` is Claude-facing (imperative instructions); the "why",
philosophy, and visuals go in the human-facing `ABOUT.html`, never in
`SKILL.md`. Minimal, never gutted — necessary procedure (commands, paths,
templates) stays.
