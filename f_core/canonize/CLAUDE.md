# `f_core/canonize` — Canonical Identity Projection

## 1) Purpose
Hosts `canonize(v)`, the single source of "render any keyed
framework object as a clean comparable PRIMITIVE". It recursively
descends the f_core key family so that identity-rendering is
expressed **once**, not re-hand-rolled per subclass.

Replaces the per-subclass `event_key()` methods (deleted from
`StateBase` / `StateCell`) and subsumes the old
`f_hs/algo/u_event_normalize._unwrap`.

## 2) Public API

### `canonize` (`u_canonize.py`)
- `canonize(v: object) -> object`
  - `HasKey` / `HasRowCol` object → `canonize(v.key)` (descend),
  - `tuple` / `list` → element-wise `canonize`, container type
    preserved,
  - primitive / `None` → returned unchanged.
  - Idempotent: `canonize(canonize(v)) == canonize(v)`.

Resolves e.g. `StateCell → (row, col)`,
`StateBase[graph] → 'A'`, `(s1, s2) → ((0,0), (1,1))`; numbers /
`None` pass through.

## 3) Inheritance (Hierarchy)
`canonize` is a stand-alone **free function** (`u_`-prefix module,
no class, no instances, no `_factory.py`, no `main.py`).

## 4) Dependencies
- `f_core.mixins.has.key.HasKey` — descent dispatch target.
- `f_core.mixins.has.row_col.HasRowCol` — descent dispatch target
  (a *sibling* of `HasKey`, not a subclass; both expose `.key`).

No stdlib beyond `isinstance`. No deps outside f_core.

## 5) Placement rationale
`canonize` lives in **f_core** (not f_utils / f_psl / f_hs) because
placement follows the **dispatch targets**, not the `u_` surface
form: it descends `HasKey` / `HasRowCol` (f_core mixins) and must
canonize `CellMap` (a `HasRowCol` in **f_ds**, above f_core) and
States (**f_hs**, above f_ds). f_core is the only layer at-or-below
all of them, so every consumer reaches it *downward* — no backward
import. Mirrors `f_core/imports/u_lazy.py` (a `u_` utility in
f_core because it is f_core's own plumbing). A peer folder of
`mixins/` (not nested inside it) because `mixins/` holds only
mixins and `canonize` spans **both** `key/` and `row_col/`.

## Files
| File | Purpose |
|------|---------|
| `u_canonize.py` | `canonize` free function. |
| `__init__.py` | Lazy re-export of `canonize` via `ULazy`. |
| `_tester.py` | pytest; all three dispatch branches + idempotency. |
| `_study.py` | Runnable toy examples. |
| `ABOUT.html` | Human-facing visual explainer (the concept). |
