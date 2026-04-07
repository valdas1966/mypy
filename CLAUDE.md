# MyPy Framework — Coding Conventions

## Clarify Before Acting
Before starting any task, if the prompt is ambiguous, underspecified, or open to multiple interpretations, ask clarifying questions first. Do not assume intent — confirm it. This applies to every prompt, no matter how simple it appears.

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
| `CLAUDE.md` | Yes | Module-specific docs for Claude Code |
| `CLAUDE.html` | On demand | Dark-themed HTML docs with TOC/search |
| `CLAUDE_REVIEW.html` | On demand | Code + design review (10 sections) |

Files prefixed with `_` are internal/private and not imported externally.

---

## Naming Conventions

### Folders
| Prefix | Meaning | Example |
|--------|---------|---------|
| `f_` | Framework module | `f_search`, `f_core`, `f_google` |
| `i_X_` | Inheritance level X | `i_0_base`, `i_1_astar`, `i_2_dijkstra` |
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
- **Constants**: `_UPPER_CASE` — `_SCOPES = [...]`

### Type Variables
- PascalCase, descriptive, with bound:
```python
State = TypeVar('State', bound=StateBase)
Problem = TypeVar('Problem', bound=ProblemSearch)
Item = TypeVar('Item')
```

---

## Docstring Conventions

### Class Docstrings
Wrapped in `=` separator lines (until max-width of 80 chars per line):
```python
class AStar(Generic[State], AlgoSPP[State, DataHeuristics]):
    """
    ============================================================================
     AStar (A*) Algorithm.
    ============================================================================
    """
```

### Method Docstrings
Same separator style, brief single-line description:
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
- Use lowercase generics: `dict[str, any]`, `tuple[int, int]`, `list[str]`.

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

### Total Ordering
For comparable classes, only implement `__lt__` with `@total_ordering`:
```python
@total_ordering
class Comparable(Equatable):
    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Comparable):
            return NotImplemented
        return self.key < other.key
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

---

## __init__.py Convention

Public exports and Factory wiring only:
```python
from f_class.main import MyClass
from f_class._factory import Factory

MyClass.Factory = Factory
```

Never put logic in `__init__.py`.

---

## Domain Abbreviations

| Abbreviation | Meaning |
|-------------|---------|
| SPP | Shortest Path Problem (one-to-one) |
| OMSPP | One-to-Many Shortest Path Problem |
| DS | Data Structures |
| CS | Computer Science |

---

## Environment

- Python 3.13+ (Conda)
- Testing: pytest
- Logging: loguru
- No linter config — follows PEP 8 by convention
- Package name: `MyPy`

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

### Drive Instructions

At the start of each session that involves Google Drive work, read
all `.md` files from the `Instructions/` folder on Drive:
```python
drive = Drive.Factory.valdas()
for f in drive.files(path='Instructions'):
    if f.endswith('.md'):
        print(drive.read(path=f'Instructions/{f}').text)
```

These instruction files define formats and workflows for:
- **Session summaries** — `For_Session_Summary.md`
- **Paper summaries** — `For_Summary.md`
- **LaTeX documents** — `For_Tex.md`

Always follow the latest version on Drive (not cached copies).

---

## Session Management

### Starting a New Session

When the user announces a new session (e.g., "new session: kids_math"
or "opening session: drive_refactor"), do the following **immediately**:

1. **Acknowledge** the session name.
2. **Read Drive instructions** — read all `.md` files from the
   `Instructions/` folder on Drive to load the latest workflows.
3. **If continuing a previous session** — read the previous session
   summary from Drive to restore context.
4. **Create the session folder and skeleton file on Drive**:
   - Write a skeleton `.md` to `/tmp/<name>_session.md` with the
     title, date, project path, and purpose filled in.
   - Upload to `YYYY/MM/DD/<name>_session.md` on Drive.
   This marks that a session started on this date and gives a file
   to build on throughout the session.
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
2. Convert to LaTeX at `/tmp/<name>_session.tex` using the template
   from the same instructions.
3. Compile to PDF: `cd /tmp && tectonic <name>_session.tex`.
4. Upload all three files (`.md`, `.tex`, `.pdf`) to Drive at:
   ```
   YYYY/MM/DD/<name>_session.md
   YYYY/MM/DD/<name>_session.tex
   YYYY/MM/DD/<name>_session.pdf
   ```
5. No local saves — `/tmp/` only. Do not auto-open the PDF.
