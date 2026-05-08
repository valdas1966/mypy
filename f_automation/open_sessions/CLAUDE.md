# OpenSessions

## Purpose
Open multiple Claude Code sessions in native OS terminal tabs. For each
session name, a tab is opened that runs `wsl` (when on Windows), then
`claude`, with `start session '<name>';` pre-submitted as the initial
prompt. Currently supports Windows (incl. WSL) via `wt.exe`; Mac stub
raises `NotImplementedError`.

## Public API

### Constructor
```python
def __init__(self,
             path_project: str = '/mnt/f/mypy') -> None
```

### Properties
```python
@property
def path_project(self) -> str
```

### Methods
```python
def open(self, names: list[str]) -> None
```
Validates each name (`[A-Za-z0-9_-]+`, must start with alnum/underscore),
detects the host OS, and dispatches to the platform backend.

### Factory (`OpenSessions.Factory.*`)
```python
OpenSessions.Factory.a() -> OpenSessions          # default /mnt/f/mypy
OpenSessions.Factory.at(path_project) -> OpenSessions
```

## Files

| File | Purpose |
|------|---------|
| `main.py` | `OpenSessions` class - validation, OS detection, routing |
| `_backend_windows.py` | `open_windows()` - builds `wt.exe` invocation |
| `_gui.py` | Tkinter `App` - multi-line name entry + Launch button |
| `_factory.py` | Factory presets |
| `_tester.py` | pytest unit tests (validation, OS detect, repr) |
| `launch.bat` | Windows shortcut target - opens GUI via WSL |
| `launch_cli.bat` | Windows shortcut target - opens tabs from `%*` args |

## Mechanism (Windows backend)

For each session name, append to `wt.exe` args:
```
new-tab --title <name> wsl.exe -- bash -lic
    "cd '<path_project>' && claude \"start session '<name>';\""
```
Multiple tabs are chained with the `;` separator (a single argv element
that `wt.exe` parses as a sub-command boundary). `claude "<prompt>"`
starts Claude Code in interactive mode with the prompt pre-submitted.

## Quoting Chain

The bash command travels four levels: Python `subprocess` (argv list) ->
WSL/Win interop (Linux argv -> Windows command line) -> `wt.exe`
(parses + re-joins for `CreateProcess`) -> `wsl.exe` (Windows args ->
Linux argv) -> `bash -lic` (parses string as a shell command). This is
fragile; the strict `_NAME_PATTERN` validator prevents shell injection
across the chain.

## Usage

CLI:
```bash
python -m f_automation.open_sessions.main automation kids_math papers
```

GUI:
```bash
python -m f_automation.open_sessions._gui
```

Programmatic:
```python
from f_automation.open_sessions import OpenSessions

OpenSessions.Factory.a().open(names=['automation', 'kids_math'])
```

Windows one-click: pin a shortcut to `launch.bat` (GUI) or
`launch_cli.bat name1 name2` (preset) on the taskbar.

## Inheritance (Hierarchy)

`OpenSessions` is a flat class - no mixins or base classes. It owns:
- name validation (`_validate_name`)
- OS detection (`_detect_os`, including WSL via `/proc/version`)
- backend dispatch (lazy import of `_backend_windows`)

## Dependencies

| Import | Purpose |
|--------|---------|
| `platform` | OS detection |
| `re` | Name validation pattern |
| `subprocess` | Spawn `wt.exe` |
| `tkinter`, `tkinter.ttk`, `tkinter.messagebox` | GUI |

## Constraints

- Session names: `[A-Za-z0-9_][A-Za-z0-9_-]*`. Anything else is rejected
  with `ValueError`.
- `claude` must be on `PATH` under `bash -lic` (login + interactive).
- `wt.exe` must be on `PATH` from WSL (Windows interop default).
- Tkinter from WSL needs WSLg (Windows 11) to display; falls back to
  running the GUI from Windows-side Python if needed.

## Future
- Mac backend via `osascript` driving iTerm2.
- Preset config (`sessions.json`) for named bundles.
- Last-used names persistence in the GUI.
