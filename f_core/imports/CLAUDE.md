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

## Files
| File | Purpose |
|------|---------|
| `u_lazy.py` | `ULazy` static utility class. |
| `__init__.py` | Re-exports `ULazy` (eager leaf wiring). |
| `_tester.py` | pytest; 4-line structural cases. |
