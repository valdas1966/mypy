# `f_nlp/_internal/_ngram` — N-Gram Concern

## 1) Purpose
Private single-concern class `_Ngram`. Exposed publicly as the
`UNlp.ngram` namespace. Never import outside `f_nlp`.

## 2) Public API (within f_nlp)
- `_Ngram.exact(text: str, n: int) -> list[list[str]]`
  Single-size primitive. Tokenizes via `_Token.ize`, then
  windows via `UList.sliding_windows`. `W - n + 1` n-grams
  (`n >= 1`); `[]` when `n > W`; `ValueError` when `n < 1`.
- `_Ngram.upto(text: str, n: int) -> list[list[str]]`
  Size-union of `exact`, grouped by size ascending; composes
  `exact` (length-`k` invariant per group). Sizes `k > W`
  contribute nothing.
- `_Ngram.doc_freq(texts: list[str], n: int) ->
  Counter[tuple[str, ...]]`
  **Document frequency**: how many texts contain each n-gram
  (per-text presence, deduped — not total occurrences). Keys
  are the lossless hashable `tuple` form of `exact`'s windows.
  Empty corpus → empty `Counter`; `ValueError` when `n < 1`
  (fail-fast even for empty corpus).

## 3) Hierarchy
Stand-alone private static class (all `@staticmethod`,
`_`-prefixed, no base, no `_factory.py`). `upto`/`doc_freq`
compose `exact`; `doc_freq` keeps `exact` the only windowing
path.

## 4) Dependencies
- `f_nlp._internal._token._Token` — tokenization (reused
  directly, not via the `UNlp` facade — avoids import cycle).
- `f_psl.builtins.list.main.UList` — sliding windows.
- `collections.Counter` (stdlib) — `doc_freq` return.

## Files
| File | Purpose |
|------|---------|
| `main.py` | `_Ngram`. |
| `__init__.py` | Leaf wiring: re-exports `_Ngram`. |
| `_tester.py` | pytest; tests `exact`/`upto`/`doc_freq`. |
