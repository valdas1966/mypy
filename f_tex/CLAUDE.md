# f_tex

## Purpose
LaTeX compilation and template helpers for the MyPy framework.
Wraps a local LaTeX engine binary (default: `tectonic`) and provides a
`session_summary` template that matches the Drive `For_Session_Summary.md`
conventions (orange accent, fancyhdr header, `\unchecked` command).

## Public API

### `class Tex` (compile only)

#### `Tex.__init__(engine: str = 'tectonic') -> None`
Bind the compiler to a LaTeX engine binary on `PATH`.

#### `Tex.engine -> str` *(property)*
Name of the engine binary.

#### `Tex.compile(src: str) -> bytes`
Compile a `.tex` source string; return PDF bytes.
Uses a `tempfile.TemporaryDirectory` — no artifacts are left on disk.
Raises `RuntimeError` with engine stderr on failure.

#### `Tex.compile_file(path_src: str, path_dest: str | None = None) -> bytes`
Compile a `.tex` file; return PDF bytes.
Multi-file projects (`\input{..}`, figures) resolve relative to
`path_src`'s directory. Writes the PDF to `path_dest` if given.
Raises `FileNotFoundError` if `path_src` does not exist.
Raises `RuntimeError` on compile failure.

#### `Tex.__repr__() -> str`
`Tex(engine='tectonic')`-style repr.

### `class Templates` (static .tex source builders)

Separate from `Tex` to keep the compiler single-responsibility. Lives
in `_templates.py`. All methods are `@staticmethod` — no state.

#### `Templates.session_summary(project_name, date, project_path, body) -> str`
Build a session-summary `.tex` source. `body` is raw LaTeX inserted
after the standard title block. Template follows the Drive
`Instructions/For_Session_Summary.md` conventions (orange accent,
fancyhdr header, `\unchecked` command).

## Inheritance (Hierarchy)
```
Tex   (no base class)
```
Standalone class. No mixins, no generics — the module is small and
single-purpose by design.

## Dependencies

| Import | Category | Used for |
|--------|----------|----------|
| `subprocess` | stdlib | invoking the engine binary |
| `tempfile` | stdlib | isolated compile directories |
| `pathlib.Path` | stdlib | file I/O |
| `pytest` | third-party | `_tester.py` only |

External: a LaTeX engine binary must exist on `PATH` **or** at a
well-known conda install location. `Tex.Factory.a()` resolves
tectonic's absolute path via `shutil.which('tectonic')`; if not on
`PATH`, it falls back to
`~/miniforge3/bin/tectonic`, `~/miniconda3/bin/tectonic`,
`~/anaconda3/bin/tectonic`, `/opt/homebrew/bin/tectonic`,
`/usr/local/bin/tectonic` before surfacing the "engine not found"
error. This makes the compiler robust to launchers (IDE run configs,
WSL shells, Windows terminals) that don't activate the conda env.

## Usage Example
```python
from f_tex import Tex

tex = Tex.Factory.a()

# 1) Compile a source string -> PDF bytes
pdf = tex.compile(src=r'''
\documentclass{article}
\begin{document} Hello. \end{document}
''')

# 2) Compile a .tex file and write the PDF
tex.compile_file(path_src='/tmp/paper.tex',
                 path_dest='/tmp/paper.pdf')

# 3) Compose with Drive: edit on disk, compile, upload
from f_google.services.drive import Drive
drive = Drive.Factory.valdas()
src = drive.read(path='2026/04/16/drive_session.tex').text
pdf = tex.compile(src=src)
open('/tmp/drive_session.pdf', 'wb').write(pdf)
drive.upload(path_src='/tmp/drive_session.pdf',
             path_dest='2026/04/16/drive_session.pdf')

# 4) Session-summary template
from f_tex import Templates
src = Templates.session_summary(
    project_name='Drive',
    date='2026-04-16',
    project_path='/mnt/f/mypy',
    body=r'\section{Purpose} f_tex scaffolding session.',
)
pdf = tex.compile(src=src)
```

## File Layout
```
f_tex/
├── main.py         # Tex — compile only
├── _templates.py   # Templates — static .tex source builders
├── _factory.py     # Factory.a()
├── _tester.py      # pytest — 7 tests
├── __init__.py     # exports Tex, Templates; wires Factory
├── CLAUDE.md       # this file
├── CLAUDE.html     # dark-theme API docs
└── ABOUT.html      # visual explainer ("what is a LaTeX compiler?")
```
