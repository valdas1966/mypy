# TestRunner

## Purpose
Discover and run all `_tester*.py` files under a folder tree
using pytest, and print a grouped, color-coded summary. Designed
to be invoked from a project-local `_run_tests.py` (typically a
one-line `TestRunner.run()` call) so tests can be run at any
folder level (whole repo, module, submodule).

## Public API

### Method
```python
@staticmethod
def run(path_folder: str = None,
        pattern: str = '_tester*.py',
        verbose: bool = False) -> ResultTest
```

| Arg | Default | Description |
|-----|---------|-------------|
| `path_folder` | `None` | Caller's directory if `None` |
| `pattern` | `'_tester*.py'` | glob pattern via `Path.rglob` |
| `verbose` | `False` | (reserved) |

Returns a `ResultTest` with `passed`, `failed`, `errors`, `files`,
`failures`.

## Discovery Pattern
The default pattern **`_tester*.py`** matches the canonical
`_tester.py` as well as any concern-split siblings such as
`_tester_grid.py` or `_tester_recording.py`. This lets a module
split its tests by concern without any ceremony beyond the
filename — the same `_run_tests.py` still picks them all up.

## Typical Usage
```python
# Anywhere under the repo: a one-line _run_tests.py
from f_test import TestRunner


TestRunner.run()  # auto-detects the caller's folder
```

Run from the repo root:
```
python -m f_hs._run_tests
python -m f_hs.frontier._run_tests
python -m f_hs.algo._run_tests
```

## Dependencies
- `pytest` — runs the discovered files via `pytest.main`
- `f_test.result.ResultTest` — return payload
