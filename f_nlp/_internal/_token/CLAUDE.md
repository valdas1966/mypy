# `f_nlp/_internal/_token` — Tokenization Concern

## 1) Purpose
Private single-concern class `_Token`. Exposed publicly as the
flat `UNlp.tokenize(text)`. Never import outside `f_nlp`.

## 2) Public API (within f_nlp)
- `_Token.ize(text: str) -> list[str]`
  Word tokenizer scoped to **English + Arabic + Hebrew only**.
  Owns no regex — delegates to `URe.extract_runs(text,
  _TOKEN_RANGES)`. Combining marks stay attached to the base
  letter (vocalized Arabic / pointed-cantillated Hebrew = one
  token). Whitespace + punctuation (Arabic `،`/`؟`, Hebrew
  maqaf/paseq/sof-pasuq) delimit. Duplicates preserved.
  **Tokenization only** — no normalization (that is `_Strip`).
  Out-of-scope scripts → no tokens, by design.

## 3) Hierarchy
Stand-alone private static class (all `@staticmethod`,
`_`-prefixed, no base, no `_factory.py`).

## 4) Dependencies
- `f_psl.re.u_re.URe` — regex mechanism (no `re` here).
- `f_nlp._internal._policy._TOKEN_RANGES` — language policy.

## Files
| File | Purpose |
|------|---------|
| `main.py` | `_Token`. |
| `__init__.py` | Leaf wiring: re-exports `_Token`. |
| `_tester.py` | pytest; tests `_Token.ize` directly. |
