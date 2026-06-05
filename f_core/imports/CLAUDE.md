# `f_core/imports` — Import / Packaging Utilities

## 1) Purpose
Static utilities for package import behavior. Hosts `ULazy`,
the single source of the PEP 562 lazy-aggregator mechanism that
was previously hand-rolled in 100+ aggregator `__init__.py`
files. Lives in `f_core` because lazy aggregation is the
framework's foundational anti-cascade import primitive; `f_core`
is the most foundational module and has no cascading deps.

## 2) Public API

### `ULazy` (`u_lazy.py`)
- `ULazy.install(g: dict, specs: dict[str, str]) -> None`
  Installs lazy `__getattr__` / `__all__` / `__dir__` into the
  calling package's `globals()`. Each spec is `'module'`
  (return the module) or `'module:attr'` (return the symbol).
  Resolved values are cached into `g` so each spec imports
  once.

## 3) Inheritance (Hierarchy)
`ULazy` is a stand-alone **static utility class** (`U`-prefix,
no instances, no base, no `_factory.py`).

## 4) Dependencies
- Standard library only (`importlib`). No framework deps —
  keeps `f_core` cascade-free.

## 5) Usage Example
```python
# any aggregator __init__.py — replaces the ~15-line block
from f_core.imports import ULazy

ULazy.install(globals(), {
    'UList': 'f_psl.builtins.list:UList',   # symbol form
    'u_dir': 'f_psl.os.u_dir',              # module form
})
```

### IDE-friendly variant (recommended)

`ULazy` injects names at **runtime** via `__getattr__`, so static
analyzers (PyCharm, pyright) can't see them — `from pkg import Name`
shows *"unresolved reference"* and gets no autocomplete. Mirror the
specs in a `TYPE_CHECKING` block: it is **False at runtime** (laziness
untouched — verified: importing the aggregator does not load a
submodule until its name is accessed) but **True for analyzers**, so
the names resolve with real go-to-definition.

```python
from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:                      # never runs — analyzers only
    from f_psl.builtins.list import UList

ULazy.install(globals(), {
    'UList': 'f_psl.builtins.list:UList',
})
```

The export list is necessarily stated twice (literal imports can't be
generated for a static tool) — a small, stable cost. Mirror the
`module:attr` spec exactly so both point at the same target.

## Files
| File | Purpose |
|------|---------|
| `u_lazy.py` | `ULazy` static utility class. |
| `__init__.py` | Re-exports `ULazy` (eager leaf wiring). |
| `_tester.py` | pytest; 4-line structural cases. |
