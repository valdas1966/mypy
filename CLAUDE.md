# MyPy Framework — Coding Conventions

## Clarify Before Acting
Before starting a task that involves code changes or design decisions, if
the prompt is ambiguous, underspecified, or open to multiple
interpretations, ask clarifying questions first. Do not assume intent —
confirm it. For straightforward operational tasks (run tests, commit,
format, etc.) proceed directly without asking.

## Response Style

Text replies to the user must be **concise, structured, and
enumerated**. Favor lists over prose.

1. **Concise sentences.** Every sentence carries unique
   information. Cut filler, hedging, preamble, and restatement
   of the user's request. Prefer short sentences; split long
   ones.

2. **Structured layout.** Group related points. For any reply
   with more than one piece of information, use either:
   - a numbered list, or
   - the `DONE / QUESTIONS / NOTES` delimiters defined in the
     Drive `Instructions/For_Tex.md` "Reporting Back to the
     User" section — these apply to **all** task reports, not
     just tex work.

3. **Enumerate points.** When a reply covers multiple items,
   present them as a numbered list. One idea per item.

4. **Inner enumeration when nested.** If a numbered item has
   sub-points, nest a second level using bullets (`-`) or
   letters (`a./b./c.`). Two levels is usually enough; avoid
   deeper nesting.

5. **No narration of diffs or tool calls.** The tools, files,
   and session `.md` carry the evidence. Do not rehearse the
   user's request.

6. **Long explanations go into the session `.md`, not chat.**
   When a detailed rationale is warranted, write it to the
   session summary on Drive and link to it from a one-line
   chat note.

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

### Direct Imports (Preferred)
Always import from the **specific module**, not from aggregator packages:
```python
# GOOD — direct import, no cascade risk
from f_google.services.drive import Drive
from f_core.mixins.comparable import Comparable
from f_search.algos.i_1_spp.i_1_astar import AStar

# AVOID — triggers lazy loading through aggregator __init__.py
from f_google import Drive
from f_core.mixins import Comparable
from f_search.algos.i_1_spp import AStar
```
Both forms work, but direct imports are faster and immune to
dependency failures in sibling packages (e.g., importing `Drive`
won't fail if `vertexai` for `Gemini` is broken).

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

**Aggregator packages** — lazy re-exports (PEP 562 `__getattr__`):
```python
__all__ = ['ClassA', 'ClassB']


def __getattr__(name: str):
    _lazy = {
        'ClassA': 'f_pkg.sub_a',
        'ClassB': 'f_pkg.sub_b',
    }
    if name in _lazy:
        from importlib import import_module
        mod = import_module(_lazy[name])
        val = getattr(mod, name)
        globals()[name] = val
        return val
    raise AttributeError(
        f"module {__name__!r} has no attribute {name!r}"
    )
```
Lazy aggregators prevent cascade failures: importing one class
won't trigger loading all sibling packages.

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

### LaTeX / Report / Graph Work

When the user asks to create or edit **LaTeX documents**, **reports**,
**TikZ figures**, or **graph diagrams** — even outside a named session
— read `Instructions/For_Tex.md` from Drive first:
```python
drive = Drive.Factory.valdas()
print(drive.read(path='Instructions/For_Tex.md').text)
```
This file contains mandatory conventions for colors, section styling,
enumerated sentences, TikZ graph diagrams (node colors by search
status, edge label positioning, layout rules), and compilation.

---

## Session Management

### Starting a New Session

When the user announces a new session (e.g., "new session: kids_math",
"opening session: drive_refactor", or "start session 'instructions'"),
do the following **immediately**:

1. **Acknowledge** the session name.

2. **Read Drive instructions** — read all `.md` files from the
   `Instructions/` folder on Drive to load the latest workflows.
   These instruction files define formats and workflows for:
   - **Session summaries** — `For_Session_Summary.md`
   - **Paper summaries** — `For_Summary.md`
   - **LaTeX documents** — `For_Tex.md`
   Always follow the latest version on Drive (not cached copies).

3. **Look up prior sessions with the same name** on Drive. The
   user's default intent when starting a named session is to
   **continue the most recent session with that name**. Search
   across year folders for files matching
   `YYYY/MM/DD/<name>_session.md` (case-insensitive) and branch
   on the result:

   - **Exact name match exists** → continue automatically:
     read the most recent `<name>_session.md` from Drive to
     restore context, and announce which date you are continuing
     from (e.g., "continuing `instructions` session from
     2026-04-10"). Today's work goes under today's date folder
     with the same name.
   - **No exact match, but a similar name exists** (substring
     match or obvious typo, case-insensitive — e.g.,
     `instruction` vs. `instructions`, `kids_math` vs.
     `kids_maths`) → **ask the user** whether to continue that
     session. Do not assume — wait for confirmation. If they
     decline, proceed as a fresh session.
   - **No match at all** → proceed as a fresh session.

4. **Create the session file on Drive for today's date**:
   - Write a skeleton `.md` to `/tmp/<name>_session.md` with the
     title, date, project path, and purpose filled in. If
     continuing, seed Purpose / What We Built / Next Steps from
     the prior summary.
   - Upload to `YYYY/MM/DD/<name>_session.md` on Drive (today's
     date, even when continuing — the prior date's file stays
     intact as a historical record).
   - **`.md` only** — do not generate `.tex` or `.pdf` at session
     start.

5. **Track** important information throughout the session:
   - Key decisions and their reasoning.
   - What was built (deliverables, files, features).
   - Architecture and design choices.
   - Unresolved issues and next steps.

### Ending a Session

When the user asks to save/close/summarize the session, or when a
meaningful chunk of work is complete:

1. Write the full session summary to `/tmp/<name>_session.md`
   following the format in `Instructions/For_Session_Summary.md`
   on Drive.
2. Upload the `.md` to Drive at `YYYY/MM/DD/<name>_session.md`.
3. **Only if the user explicitly asks for a TeX/PDF export**,
   follow the "On-Demand: TeX and PDF Exports" section in
   `Instructions/For_Session_Summary.md`: convert to `.tex`,
   compile with `tectonic`, and upload both. Do not generate
   these proactively.
4. No local saves — `/tmp/` only. Do not auto-open the PDF.
