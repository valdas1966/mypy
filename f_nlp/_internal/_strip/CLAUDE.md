# `f_nlp/_internal/_strip` — Diacritic-Stripping Concern

## 1) Purpose
Private single-concern class `_Strip`. Exposed publicly as the
`UNlp.strip` namespace. Never import outside `f_nlp`.

## 2) Public API (within f_nlp)
- `_Strip.marks(s: str) -> str`
  Diacritic-insensitive **fold for comparison**: removes
  `_MARK_RANGES` (harakat, tanwin, tatweel, Quranic signs,
  Hebrew niqqud/te'amim/dagesh, shin/sin dots), keeps base
  letters. Delegates to `URe.strip_ranges`. Idempotent.
  Folding merges some phonemic distinctions on purpose
  (Hebrew shin vs sin, dagesh; Arabic shadda) — "compare only
  the solid letters". Not a normalizer.
- `_Strip.diacritics(text: str) -> str`
  Discoverable **alias** of `marks` — same policy, same
  mechanism, no new logic (delegation asserted in
  `_tester.py`). For callers wanting clean consonantal text
  rather than specifically an equality fold.

## 3) Hierarchy
Stand-alone private static class (all `@staticmethod`,
`_`-prefixed, no base, no `_factory.py`).

## 4) Dependencies
- `f_psl.re.u_re.URe` — regex mechanism (no `re` here).
- `f_nlp._internal._policy._MARK_RANGES` — language policy.

## 5) Tested Invariant
`_tester.py` also asserts `_MARK_RANGES ⊆ _TOKEN_RANGES`
(stripping never removes a token-only char; alef-wasla
U+0671 stays a letter) — the policy invariant lives with the
concern it protects.

## Files
| File | Purpose |
|------|---------|
| `main.py` | `_Strip`. |
| `__init__.py` | Leaf wiring: re-exports `_Strip`. |
| `_tester.py` | pytest; `_Strip` + policy subset invariant. |
