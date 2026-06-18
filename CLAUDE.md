# MyPy Framework — Coding Conventions

This file is the **hub**: the always-loaded introduction and conventions
index. Detailed, task-specific procedures live in `f_claude/instructions/`
— read the relevant guide **before** starting that task.

## Task-Specific Guides

When you are about to do one of these tasks, read its guide in
`f_claude/instructions/` first (this index is the map; each section below
also links its guide inline):

| About to… | Read (`f_claude/instructions/`) |
|---|---|
| Add or update a `CLAUDE.md` | `for_claude_md.md` |
| Generate `CLAUDE.html` | `for_claude_html.md` |
| Generate `CLAUDE_REVIEW.html` | `for_claude_review.md` |
| Generate `ABOUT.html` | `for_about_html.md` |
| Write or edit a skill | `for_skill.md` |
| Write new code (reuse-first check) / build a class | `for_new_class.md` |
| Apply a design pattern | `for_patterns.md` |
| Write tests (`_tester.py`) | `for_testing.md` |
| Write imports / an `__init__.py` | `for_imports.md` |
| Lay out a module (folders, file roles) | `for_structure.md` |
| Add logging to a module | `for_logging.md` |
| Look up a domain abbreviation | `for_glossary.md` |
| Do any Google Drive operation | `for_drive.md` |
| Write or edit LaTeX (`.tex`) | `for_tex.md` |

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
`f_claude/instructions/for_structure.md`.

---

## Naming Conventions

### Folders
| Prefix | Meaning | Example |
|--------|---------|---------|
| `f_` | Framework module | `f_search`, `f_core`, `f_google` |
| `i_X_` | Inheritance level X | `i_0_base`, `i_1_astar`, `i_2_dijkstra` |
| `_internal/` | Private helper classes | `drive/_internal/` |
| (none) | Domain grouping | `algos/`, `problems/`, `solutions/`, `ds/` |

### Files
| Prefix | Meaning | Example |
|--------|---------|---------|
| `u_` | Utility module (functions, no classes) | `u_dict.py`, `u_file.py`, `u_datetime.py` |
| `c_` | Component / service wrapper | `c_loguru.py`, `c_timer.py` |
| `_` | Internal / private | `_factory.py`, `_tester.py` |
| (none) | Public module | `main.py` |

### Classes
- **PascalCase**: `AlgoSearch`, `CellBase`, `AStar`, `ProblemSPP`
- **Base classes**: named `*Base` or placed in `i_0_base/`
- **Mixins**: named as adjectives/capabilities — `Comparable`, `Printable`, `HasRowCol`, `ValidatableMutable`
- **Enums**: `TypeComparison`, `ServiceAccount`

### Functions and Methods
- **snake_case**: `_discover()`, `_handle_successor()`, `_need_relax()`
- **Private**: single `_` prefix — `_init_add_atts()`, `_pre_run()`
- **Factory statics**: short names for test objects — `a()`, `b()`, `gen()`

### Variables
- **Instance attributes**: `self._name` (single `_` for protected)
- **Local aliases**: short names in method bodies — `data = self._data`
- **Dict attributes**: descriptive prefixed names — `dict_g`, `dict_h`
- **Module-level constants**: `_UPPER_CASE` (private) — `_SCOPES = [...]`
- **Class-level constants**: `UPPER_CASE` (public) — `Factory: type = None`

### Type Variables
- PascalCase, descriptive, with bound:
```python
State = TypeVar('State', bound=StateBase)
Problem = TypeVar('Problem', bound=ProblemSearch)
Item = TypeVar('Item')
```

---

## Docstring Conventions

### Separator Width Rule
The `=` count adjusts to keep total line width at 80 characters:
| Context | Indentation | `=` count |
|---------|-------------|-----------|
| Module-level | 0 spaces | 80 |
| Class docstring | 4 spaces | 76 |
| Method docstring | 8 spaces | 72 |

### Class Docstrings
```python
class AStar(Generic[State], AlgoSPP[State, DataHeuristics]):
    """
    ============================================================================
     AStar (A*) Algorithm.
    ============================================================================
    """
```

### Method Docstrings
```python
def _discover(self, state: State) -> None:
    """
    ========================================================================
     Discover the given State.
    ========================================================================
    """
```

### Inline Comments
Short, above the line they describe:
```python
# Aliases
data = self._data
# Set State's Parent
data.set_best_to_be_parent_of(state=state)
```

---

## Code Style

### Type Annotations
- Annotate all function parameters and return types.
- Use `-> None` for methods that return nothing.
- Use modern union syntax: `type | None` (not `Optional`).
- Use lowercase generics: `dict[str, Any]`, `tuple[int, int]`, `list[str]`.

```python
def __init__(self,
             row: int,
             col: int,
             name: str = 'CellBase') -> None:

@property
def key(self) -> tuple[int, int]:
```

### Formatting
- **Indentation**: 4 spaces, no tabs.
- **Line length**: 80 characters.
- **Multi-line params**: align with opening parenthesis.
- **Blank lines**: 2 between top-level definitions, 1 between methods, none inside short methods.
- **Strings**: f-strings preferred — `f'{self.name}({self.row},{self.col})'`.
- **Named arguments** in calls: `data.set_best_to_be_parent_of(state=state)`.

### Class Definition Order
1. Class docstring
2. Class-level attributes (`Factory: type = None`, `cls_stats: type = ...`)
3. `__init__`
4. Properties (`@property`)
5. Public methods
6. Private methods (`_method`)
7. Dunder methods (`__str__`, `__repr__`, `__lt__`)

---

## Design Patterns

Full examples: `f_claude/instructions/for_patterns.md` — read it before
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
`f_claude/instructions/for_new_class.md`.

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
conventions and examples: `f_claude/instructions/for_testing.md`.
Essentials:

- Test functions `test_<method_name>()`; each has a `=`-separator
  docstring.
- Prefer `MyClass.Factory.a()` directly in the test over a
  `@pytest.fixture` that only wraps it — use fixtures only for real
  setup/teardown, parametrization, or scope.

---

## Import Conventions

Full guide (aggregator vs direct, `ULazy`, `__init__.py` patterns):
`f_claude/instructions/for_imports.md`. Essentials:

- **Import order (PEP 8):** stdlib → third-party → framework, groups
  blank-line separated; absolute imports throughout.
- **Aggregator and direct imports are both first-class** — aggregators
  are lazy (`ULazy`), so equally cascade-immune.
- **Never put business logic in `__init__.py`.**

---

## Domain Abbreviations

Domain abbreviations (SPP, OMSPP, MMSPP, BFS, HS, DS, CS, PSL, GUI) are
defined in `f_claude/instructions/for_glossary.md`.

---

## Environment

- Python 3.13+ (Conda)
- Testing: pytest
- Logging: `f_log` — module-level `_log = get_log(__name__)`; full
  convention: `f_claude/instructions/for_logging.md`
- No linter config — follows PEP 8 by convention
- Package name: `MyPy`

---

## CLAUDE Documentation Rule

### Auto-update: CLAUDE.md
Every code change MUST update the `CLAUDE.md` file in each folder that contains at least one changed file. Follow `f_claude/instructions/for_claude_md.md`. If `CLAUDE.md` does not exist in the folder, create it.

### On demand: CLAUDE.html and CLAUDE_REVIEW.html
`CLAUDE.html` and `CLAUDE_REVIEW.html` are generated **only when the user explicitly requests** them. These files are for human reading — Claude reads only `CLAUDE.md`. Follow `for_claude_html.md` / `for_claude_review.md` (and `for_about_html.md` for `ABOUT.html`); those guides cover the visual style and the AI-generated-image workflow.

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

Full operations guide: `f_claude/instructions/for_drive.md`. Open with
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

Full conventions: `f_claude/instructions/for_tex.md` (local) and Drive
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
read `f_claude/instructions/for_skill.md` first. It is the authoritative
guide for skill content.

Core rule: a `SKILL.md` must be the **most minimal text that still passes
the correct message** — only lines that change what Claude does at run
time. `SKILL.md` is Claude-facing (imperative instructions); the "why",
philosophy, and visuals go in the human-facing `ABOUT.html`, never in
`SKILL.md`. Minimal, never gutted — necessary procedure (commands, paths,
templates) stays.
