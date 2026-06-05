# MyPy Framework — Coding Conventions

## Clarify Before Acting
Before starting a task that involves code changes or design decisions, if
the prompt is ambiguous, underspecified, or open to multiple
interpretations, ask clarifying questions first. Do not assume intent —
confirm it. For straightforward operational tasks (run tests, commit,
format, etc.) proceed directly without asking.

## Effort Escalation

Before starting a task, judge whether regular reasoning effort
is likely to suffice. If the task is genuinely complex —
multi-step design, subtle correctness, cross-module impact,
non-obvious tradeoffs, hard performance constraints — **flag
this and ask** whether to use a higher reasoning effort (e.g.,
`ultrathink`) before proceeding. Do not silently downscope or
take a shortcut on a task that warrants the extra budget. For
routine, well-scoped tasks, proceed without asking.

## Response Style

Format every reply so the reader grasps it **at a glance and
in full**. Structure for fast scanning; never pad.

1. **Bottom line first.** Open with the verdict / result /
   answer — a bold line or short header — before any detail.
   The takeaway comes before the reasoning.

2. **Structure over prose.** Prefer headers, **bold
   lead-ins**, and ranked lists. Use a **table** for anything
   comparative (option vs. trade-off, proposal vs. take vs.
   why, before vs. after). Avoid paragraph walls.

3. **Status markers.** Signal verdicts and rankings with
   compact icons — ✅ do · 🟡 caveat · ❌ avoid · ⏸️ defer ·
   🚫 don't — so items can be ranked without close reading.

4. **Complete but tight.** As long as needed to be fully
   understood, as short as possible. No fixed word or sentence
   cap — but cut all preamble, recap, restatement of the
   request, and hedging. Every line earns its place.

5. **No narration of tool calls or diffs.** Tools, files, and
   the session `.md` carry the evidence — do not replay them
   in chat.

6. **Long rationale → session `.md`, link from chat.** When
   deep reasoning is warranted, write it to the Drive session
   summary and link it in one line; keep the chat reply to the
   conclusions.

7. **Task reports — lead with outcome.** State what changed /
   what holds / what's blocked, using the structure above. Add
   a **Note** only for genuinely critical, non-obvious info
   (default: none — most reports need none). Raise a
   **Question** only as a pre-task blocker (genuine ambiguity
   that stops progress) — never as an after-the-fact
   follow-up.

## Project Structure

### Top-Level Modules
Framework modules use the `f_` prefix: `f_core`, `f_ds`, `f_search`, `f_google`, `f_utils`, `f_gui`, `f_cs`, etc.

### Module Internal Hierarchy
Modules use `i_X_name/` folders to express inheritance depth:
```
f_search/algos/
├── i_0_base/i_0_search/        # Level 0 — abstract root (AlgoSearch)
├── i_1_spp/                    # Level 1 — SPP family
│   ├── i_0_base/               # Level 1→0 — abstract SPP base
│   ├── i_1_astar/              # Level 1→1 — AStar
│   └── i_2_dijkstra/           # Level 1→2 — Dijkstra (extends AStar)
└── i_2_omspp/                  # Level 2 — One-to-Many family
```
The number after `i_` indicates the inheritance level within that scope. `i_0_` is always the abstract base.

### Standard Files Per Module
Every class module contains a subset of these files:
| File | Required | Purpose |
|------|----------|---------|
| `main.py` | Yes | Primary class implementation |
| `__init__.py` | Yes | Public exports; wires `Factory` onto the class |
| `_factory.py` | If testable | Factory class for creating common instances |
| `_tester.py` | If testable | pytest unit tests |
| `_study.py` | No | Exploratory / research scripts |
| `_run_tests.py` | No | Batch runner for all `_tester.py` in subtree |
| `_from.py` | No | Static constructors from external formats |
| `_to.py` | No | Instance conversion methods to external formats |
| `CLAUDE.md` | Yes | Module-specific docs for Claude Code |
| `CLAUDE.html` | On demand | Dark-themed HTML docs with TOC/search |
| `CLAUDE_REVIEW.html` | On demand | Code + design review (10 sections) |
| `ABOUT.html` | On demand | Visual overview for human reading |

Files prefixed with `_` are internal/private and not imported externally.

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

### Factory Pattern
Each class declares `Factory: type = None`. The actual Factory is defined in `_factory.py` and wired in `__init__.py`:
```python
# main.py
class MyClass:
    Factory: type = None

# _factory.py
class Factory:
    @staticmethod
    def a() -> 'MyClass':
        ...

# __init__.py
from .main import MyClass
from ._factory import Factory
MyClass.Factory = Factory
```

### Mixin Composition
Prefer mixins over deep single inheritance. Mixins are adjectives:
```python
class CellBase(HasRowCol, HasName):
class CellMap(CellBase, ValidatableMutable):
class ProblemSPP(ProblemSearch, HasStart, HasGoal):
```

### Template Method (Lifecycle Hooks)
Base classes define hooks; subclasses override:
```python
def _pre_run(self) -> None: ...
def _post_run(self) -> None: ...
def _init_add_atts(self) -> None: ...
```

### Generics
Classes are parameterized with `Generic[...]`:
```python
class AlgoSearch(Generic[Problem, Solution], Algo[Problem, Solution]):
class AStar(Generic[State], AlgoSPP[State, DataHeuristics]):
```

### Comparison Operators
For comparable classes, implement all four operators explicitly for
performance (no `@total_ordering` overhead). Delegate to `key`:
```python
class Comparable(Equatable):
    def __lt__(self, other: object) -> bool:
        return self.key < other.key
    def __le__(self, other: object) -> bool:
        return self.key <= other.key
    def __gt__(self, other: object) -> bool:
        return self.key > other.key
    def __ge__(self, other: object) -> bool:
        return self.key >= other.key
```

### Dataclasses vs Manual `__init__`
Use `@dataclass` for **data-holder classes** with no business logic:
```python
@dataclass
class ResultTest:
    passed: int = 0
    failed: int = 0
    failures: list[str] = field(default_factory=list)
```
Use **manual `__init__`** for behavior-rich classes (mixins, algorithms,
domain objects). Do not use `attrs`.

### Error Handling
No custom exception classes — use built-in exceptions (`ValueError`,
`FileNotFoundError`, `TypeError`). For operations that can fail
partially, capture the error as a string:
```python
try:
    response = requests.get(url=url, timeout=timeout)
except Exception as e:
    exception = str(e)
```

### Async
Not used. The entire codebase is synchronous.

---

## Building New Classes — Infrastructure Check

Before writing a new class, run this **2-step check**. It is a
pre-coding gate, same category as *Clarify Before Acting*. The
codebase's primary design language is capability-as-mixin +
reusable-data-structure — silently re-implementing a capability
fragments the framework (future migrations become N-class
refactors).

### Step 1 — Reuse existing `f_core` / `f_ds` infrastructure

Before hand-rolling **any** cross-cutting capability (identity,
equality, ordering, serialization, validation, event capture,
container type), check whether it already exists.

**Where to look:**

`f_core/mixins/` — capability mixins (adjectives):

| Capability | Mixin |
|---|---|
| equality | `Equatable` |
| ordering (all 4 operators, `key`-based) | `Comparable` |
| name + `__str__` / `__repr__` | `Printable`, `HasName` |
| dict ↔ obj serialization | `Dictable` |
| validation (immutable / mutable) | `Validatable` / `ValidatableMutable` |
| 2-D grid row/col identity | `HasRowCol` |
| generic keyed identity | `HasKey` |

`f_core/recorder/` — `Recorder` (list-of-dict event capture
with `is_active` on/off).

`f_ds/` — reusable data structures: grids, cells, queues
(FIFO/LIFO), priority queues, maps.

**How to look quickly:**
```
Glob: f_core/mixins/**/__init__.py
Glob: f_ds/**/main.py
Grep: "class <Capability>" in f_core/ f_ds/
```

**Rule:** if the capability exists, USE IT by inheritance or
composition. Never reimplement `__eq__` / `__hash__` / ordering
/ recording / heap ops in a new class — delegate to the mixin
or data structure.

### Step 2 — Missing but broadly useful → **SUGGEST, don't silently build**

If no existing infrastructure matches and you're about to
hand-roll the capability, apply the **rule of three + future
use** test. **Suggest** creating shared infrastructure when
ANY of these holds:

1. **≥3 existing classes** already hand-roll the same pattern
   (concrete duplication present today), OR
2. The capability is **foundational** (identity / equality /
   ordering / serialization / validation / event capture /
   container type) and will be reused by **≥2 concrete
   classes** current-or-imminent, OR
3. A **clean extraction point** exists in an adjacent module
   (e.g., the new class wants heap ops that belong in `f_ds`
   rather than the domain module).

**Do NOT create shared infrastructure when:**
- Only one class needs it AND the use case is narrow (YAGNI).
- The "infrastructure" is domain logic in disguise (it belongs
  in the domain module, not `f_core` / `f_ds`).

**How to suggest (mandatory script):** pause before writing
the new class and tell the user, using concrete file paths and
at least two naming examples:

> "I'm about to implement `<capability>` in `<new_class>`.
> `<existing_class_A>` and `<existing_class_B>` already
> hand-roll this. Propose extracting it into
> `f_core/<folder>/<name>.py` (or `f_ds/<folder>/<name>.py`)
> as a shared mixin/utility first. Proceed?"

**Wait for explicit confirmation.** Never silently extract —
new shared infrastructure is an architectural commitment the
user owns.

### Decision cheat-sheet

```
new class needed
    │
    ├── capability already in f_core/f_ds? ──► YES → use it (inherit/compose)
    │                                          │
    │                                          NO
    │                                          ▼
    ├── ≥3 hand-rolled duplicates OR foundational + ≥2 reusers?
    │       │
    │       ├── YES → SUGGEST new shared infra (wait for user OK)
    │       │
    │       └── NO  → write it inline in the new class (YAGNI)
```

---

## Testing Conventions

Tests live in `_tester.py` alongside `main.py`. Use pytest with fixtures that call Factory methods:
```python
import pytest

@pytest.fixture
def a() -> Comparable:
    """
    ========================================================================
     Create a Comparable object with the value 'A'.
    ========================================================================
    """
    return Comparable.Factory.a()

def test_lt(a: Comparable, b: Comparable) -> None:
    """
    ========================================================================
     Test the __lt__() method.
    ========================================================================
    """
    assert a < b
    assert not (b < a)
```

- Test functions: `test_<method_name>()`.
- Fixtures: short names matching Factory methods (`a`, `b`, `gen`).
- Each test has a docstring with `=` separators.

### Prefer `Factory` over `@pytest.fixture`

Do **not** wrap a `Factory` call in a `@pytest.fixture` when the
Factory method alone is enough. Fixtures add indirection and hide
where the object comes from — if the test just needs a canonical
instance, call `MyClass.Factory.a()` directly inside the test:

```python
# GOOD — Factory is the single source of canonical test objects
def test_lt() -> None:
    """
    ========================================================================
     Test the __lt__() method.
    ========================================================================
    """
    a = Comparable.Factory.a()
    b = Comparable.Factory.b()
    assert a < b

# AVOID — fixture duplicates Factory, adds no value
@pytest.fixture
def a() -> Comparable:
    return Comparable.Factory.a()
```

Use `@pytest.fixture` **only** when it adds real value beyond what
`Factory` provides — e.g., shared setup/teardown, parametrization,
scope (`scope='module'`), or an object built from multiple Factory
calls with non-trivial wiring. When in doubt, prefer `Factory`:
it's more explicit and keeps the test's inputs visible in the test
body.

---

## Import Conventions

### Aggregator vs Direct Imports — both first-class
Either form is fine; pick by ergonomics. They are equivalent in safety
and speed because aggregators are **lazy** (`ULazy`): `from f_pkg import X`
loads only `X`'s module on access, not its siblings — so it is just as
cascade-immune as a direct import (importing `Drive` won't fail if
`vertexai` for `Gemini` is broken).

```python
# Aggregator — ergonomic, groups related names
from f_gui.elements import Window, Container, Label
from f_core.mixins import Comparable

# Direct — addresses one leaf module explicitly
from f_google.services.drive import Drive
from f_search.algos.i_1_spp.i_1_astar import AStar
```

**Requirement for aggregators:** the package's `__init__.py` MUST carry
the `TYPE_CHECKING` mirror block (see below) so the aggregator form
resolves in IDEs / mypy (no "unresolved reference", real autocomplete).
All `ULazy` aggregators in the repo now have it.

### Import Order (PEP 8)
1. Standard library (`os`, `typing`, `abc`, `collections`)
2. Third-party (`pytest`, `loguru`, `google.auth`)
3. Framework (`f_core`, `f_ds`, `f_search`, `f_google`)

Separate groups with a blank line. Use absolute imports throughout.

### __init__.py Convention

Two types of `__init__.py` in this codebase:

**Leaf modules** — Factory wiring (eager imports):
```python
from f_class.main import MyClass
from f_class._factory import Factory

MyClass.Factory = Factory
```

**Aggregator packages** — lazy re-exports via `ULazy` + a
`TYPE_CHECKING` mirror block. `ULazy.install` wires the runtime
`__getattr__`/`__all__`/`__dir__`; the `if TYPE_CHECKING:` block (False
at runtime, so laziness is untouched; True for analyzers) makes the
names statically resolvable. Mirror each `module:attr` spec exactly.
```python
from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:                        # analyzers only — never runs
    from f_pkg.sub_a import ClassA
    from f_pkg.sub_b import ClassB

ULazy.install(globals(), {
    'ClassA': 'f_pkg.sub_a:ClassA',
    'ClassB': 'f_pkg.sub_b:ClassB',
})
```
Lazy aggregators prevent cascade failures: importing one class
won't trigger loading all sibling packages. See
`f_core/imports/CLAUDE.md` for `ULazy` spec forms (symbol / module /
relative).

Never put business logic in `__init__.py`.

---

## Domain Abbreviations

| Abbreviation | Meaning |
|-------------|---------|
| SPP | Shortest Path Problem (one-to-one) |
| OMSPP | One-to-Many Shortest Path Problem |
| MMSPP | Many-to-Many Shortest Path Problem |
| BFS | Breadth-First Search |
| HS | Heuristic Search |
| DS | Data Structures |
| CS | Computer Science |
| PSL | Python Standard Library (wrappers) |
| GUI | Graphical User Interface |

---

## Environment

- Python 3.13+ (Conda)
- Testing: pytest
- Logging: `f_log` (wrapper around Python `logging` + `ColorLog`)
- No linter config — follows PEP 8 by convention
- Package name: `MyPy`

### Logging Convention
```python
from f_log import get_log

_log = get_log(__name__)
_log.info(f'{cl.label("GET")} {cl.path(url)} {cl.time(elapsed)}')
```
Use module-level `_log = get_log(__name__)`. Use standard levels
(`debug`, `info`, `warning`, `error`). Use `ColorLog` helpers
for formatted output.

---

## CLAUDE Documentation Rule

### Auto-update: CLAUDE.md
Every code change MUST update the `CLAUDE.md` file in each folder that contains at least one changed file. Follow the template in `f_claude/instructions/for_claude_md.md`. If `CLAUDE.md` does not exist in the folder, create it.

### On demand: CLAUDE.html and CLAUDE_REVIEW.html
`CLAUDE.html` and `CLAUDE_REVIEW.html` are generated **only when the user explicitly requests** them. These files are for human reading — Claude reads only `CLAUDE.md`.

Follow the templates in `f_claude/instructions/`:
- `for_claude_html.md` — instructions for generating `CLAUDE.html`
- `for_claude_review.md` — instructions for generating `CLAUDE_REVIEW.html`

### Visual HTML Files
All generated HTML files (`CLAUDE.html`, `CLAUDE_REVIEW.html`) should be **as visual as possible** — not just text walls. Use diagrams, colored sections, icons, visual hierarchies, and illustrations to make the content engaging and easy to scan.

**AI-Generated Images Workflow:**
When generating HTML files, if an image or illustration would significantly enhance the documentation (e.g., architecture diagrams, class hierarchy visuals, concept illustrations), Claude should:
1. Pause the HTML generation.
2. Provide the user with a clear image-generation prompt (suitable for ChatGPT, Google Gemini, or NanoBanana).
3. Wait for the user to upload the generated image(s).
4. Embed the image(s) into the HTML file (using base64 inline or relative paths).

The user has subscriptions to **ChatGPT**, **Google Gemini**, and **NanoBanana** for image generation.

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

### Read Drive Instructions First

Before performing **any** Google Drive operation (session work,
summaries, reports, LaTeX, uploads, reads, deletes, folder listings,
etc.), **always read the relevant file(s) from the Drive
`Instructions/` folder first**. This folder holds the authoritative,
up-to-date workflows — the local `CLAUDE.md` is only a pointer.

```python
from f_google.services.drive import Drive
drive = Drive.Factory.valdas()

# 1) Discover what instructions exist:
for f in drive.files(path='Instructions'):
    print(f)

# 2) Read the relevant one(s) for the task at hand:
print(drive.read(path='Instructions/For_Session_Summary.md').text)
print(drive.read(path='Instructions/For_Report.md').text)
print(drive.read(path='Instructions/For_Summary.md').text)
print(drive.read(path='Instructions/For_Tex.md').text)
```

Rules:
- **Never cache** these instructions across sessions — always re-read
  from Drive, since they may have been updated.
- Map task → instruction file:
  - Session start / session summary → `For_Session_Summary.md`
  - Paper / project reports → `For_Report.md`
  - Paper summaries → `For_Summary.md`
  - LaTeX, TikZ, graphs, figures → `For_Tex.md`
- If no dedicated instruction file matches the task, list
  `Instructions/` anyway and confirm — new instruction files may
  have been added.
- Follow the Drive instruction verbatim; if it conflicts with this
  local `CLAUDE.md`, **the Drive instruction wins**.

### How to Open Google Drive

Connect to our Google Drive using the VALDAS OAuth credentials:
```python
from f_google.services.drive import Drive
drive = Drive.Factory.valdas()
```

### Common Operations

**List folders and files:**
```python
folders = drive.folders(path='Projects/2026')   # list subfolder names
files = drive.files(path='Projects/2026')       # list file names
folders = drive.folders()                       # root-level folders
```

**Read a file into memory (no local save):**
```python
response = drive.read(path='Papers/Topic/Paper.pdf')
print(response.text)       # text content (markdown for PDFs)
print(response.pages)      # list[bytes] — PNG pages (PDFs only)
```

**Check existence:**
```python
if drive.is_exists(path='2026/04/07/session.md'):
    ...
```

**Upload (auto-creates parent folders, overwrites if exists):**
```python
drive.upload(path_src='/tmp/file.md',
             path_dest='2026/04/07/file.md')
```

**Download to local disk:**
```python
drive.download(path_src='Papers/Topic/Paper.pdf',
               path_dest='/tmp/Paper.pdf')
```

**Create folder / delete:**
```python
drive.create_folder(path='2026/04/07')
drive.delete(path='2026/04/07/old_file.md')
```

### Drive-Only Workflow

- **Never save Drive files locally** in the project directory.
- Use `/tmp/` for all intermediate work (compile, edit, etc.).
- Upload results back to Drive.
- Do **not** auto-open files — the user views them on Drive.

---

## LaTeX Files

### Mandatory `\me` / `\you` annotation macros

Every `.tex` file created or edited under this project — whether
destined for Drive or Overleaf — **must** define both annotation
macros in the preamble, so the option to write inline author /
AI comments is available at all times:

- **`\me{...}`** — the author's voice, rendered in **red**.
- **`\you{...}`** — Claude's (the AI's) reply, rendered in
  **blue**.

Both macros share a single `\ifdraft` toggle, so flipping it to
`\draftfalse` strips every annotation for the publication build.
A `.tex` without the block is **non-conforming** — fix before
upload (to Drive or Overleaf).

**Required preamble block** (paste verbatim, after the color /
styling preamble, before `\begin{document}`):

```latex
% ── Author annotations (draft only) ─────────────────────
\newif\ifdraft\drafttrue  % flip to \draftfalse to strip all

\newcommand{\me}[1]{%
    \ifdraft\textcolor{red}{\textbf{[me:\,#1]}}\fi%
}
\newcommand{\you}[1]{%
    \ifdraft\textcolor{blue}{\textbf{[you:\,#1]}}\fi%
}
```

The block must be present even when the file currently contains
zero `\me{...}` or `\you{...}` calls — annotations may be added
inline at any time.

### Bidirectional protocol

On every read of a `.tex`, scan for inline `\me{...}`
annotations and act:

- **Tasks** (imperatives — "make X bold", "add reference") —
  execute the edit. If a `\me{...}` line sits in a LaTeX-invalid
  position (e.g., inside `\begin{itemize}` before any `\item`),
  remove the line as part of the fix.
- **Questions** (interrogatives — "why X?", "does Y hold?") —
  insert `\you{<one-sentence answer>}` immediately after the
  `\me{...}`, keeping the `\me{...}` so the thread reads
  naturally.
- **No `\you{...}` without a `\me{...}`** — AI annotations exist
  to answer the author. Do not add unsolicited `\you{...}`.

Replies inside `\you{...}` follow the same brevity rule: one
sentence or less. Long rationale belongs in the session `.md`,
never the `.tex`.

### Drive instructions are authoritative

Before creating or editing any **LaTeX document**, **report**,
**TikZ figure**, or **graph diagram** — even outside a named
session — read `Instructions/For_Tex.md` from Drive first:

```python
drive = Drive.Factory.valdas()
print(drive.read(path='Instructions/For_Tex.md').text)
```

That file holds the authoritative conventions for colors,
section styling, enumerated sentences, TikZ graph diagrams
(node colors by search status, edge label positioning, layout
rules), and compilation. If it conflicts with this section,
**Drive wins**.

---

## Session Management

The session lifecycle lives in two skills under `.claude/skills/`:

- **`start-session`** — start or continue a named session: read Drive
  instructions, find & continue a prior same-named session, create
  today's skeleton, report back. Triggers: "start session '<name>'",
  "new session", "open session".
- **`finish-session`** — save / close / summarize / end the session:
  write & upload the full summary. Triggers: "save the session", "close
  session", "summarize the session", "end session".

Both call the shared Drive helper at
`.claude/skills/_session_lib/session.py` and are the authoritative
workflows. Session summaries live on Drive at
`YYYY/MM/DD/<name>_session.md` (flat names); the Drive rules above (read
`Instructions/` first; Drive-only; `/tmp` for intermediates) still apply.
