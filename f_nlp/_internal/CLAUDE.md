# `f_nlp/_internal` — Private NLP Concern Modules

## 1) Purpose
Private implementation for `f_nlp`. Each NLP **concern is its
own folder-per-class module**; the public `UNlp` facade
(`f_nlp/u_nlp.py`) binds them as namespaces. **Never import
from here outside `f_nlp`** — the supported surface is `UNlp`.

## 2) Layout

```
_internal/
  __init__.py     private package marker (no logic)
  _policy.py      _TOKEN_RANGES, _MARK_RANGES — flat shared-data module
  _token/         _Token  -> UNlp.tokenize           (main.py + _tester + CLAUDE)
  _strip/         _Strip  -> UNlp.strip.*            (main.py + _tester + CLAUDE)
  _ngram/         _Ngram  -> UNlp.ngram.*            (main.py + _tester + CLAUDE)
```

Each concern folder is a standard class module: `main.py`
(the `_X` class), `__init__.py` (leaf wiring re-export),
`_tester.py` (tests the class **directly**), `CLAUDE.md`.

- `_policy.py` — language **policy only**: integer `(lo, hi)`
  code-point ranges for word chars (`_TOKEN_RANGES`) and
  optional marks (`_MARK_RANGES`, a strict subset of the mark
  portion of `_TOKEN_RANGES`). No class, no folder (it is
  data, not a concern class); no `re`. Its subset invariant is
  tested in `_strip/_tester.py` (the concern it protects).
- `_token/` — `_Token.ize` → `URe.extract_runs(text,
  _TOKEN_RANGES)`. EN/AR/HE scope; diacritic-aware; no
  normalization.
- `_strip/` — `_Strip.marks` → `URe.strip_ranges(s,
  _MARK_RANGES)`; `_Strip.diacritics` is a thin alias of
  `marks` (no new logic).
- `_ngram/` — `_Ngram.exact` (single-size primitive, windows
  `_Token.ize` via `UList.sliding_windows`); `_Ngram.upto`
  (size-union of `exact`); `_Ngram.doc_freq` (per-text
  presence `Counter`, `tuple` keys). All raise `ValueError`
  when `n < 1`.

## 3) Design Rules
- **Folder-per-class.** An internal class earns its own
  folder module (the framework's standard shape) — not inner
  classes, not separate public classes. Data-only modules
  (`_policy.py`) stay flat.
- **Policy here, mechanism in `URe`.** No `_internal` file
  imports `re`; all regex is delegated to `f_psl/re`.
- **No cross-public imports.** `_ngram` reuses `_Token`
  directly (`from f_nlp._internal._token import _Token`), not
  `UNlp`, to avoid a facade import cycle.
- **Tests are per-class.** Each `_internal/<concern>/_tester.py`
  tests its private class directly; `f_nlp/_tester.py` only
  asserts facade wiring. No double-testing.

## 4) Dependencies
- `f_psl.re.u_re.URe` — regex mechanism.
- `f_psl.builtins.list.main.UList` — sliding windows.
- `collections.Counter` (stdlib) — `_Ngram.doc_freq`.

## Files
| File | Purpose |
|------|---------|
| `__init__.py` | Empty (private package marker; no logic). |
| `_policy.py` | Shared language policy ranges (flat). |
| `_token/` | `_Token` tokenization concern (class module). |
| `_strip/` | `_Strip` diacritic-stripping concern (class module). |
| `_ngram/` | `_Ngram` n-gram concern (class module). |
