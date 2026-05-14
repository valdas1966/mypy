# `f_psl/re/testers` — Regex Tests

## 1) Purpose
pytest suite for `f_psl.re`. Each test exercises a single public
method of `URe` using inputs from `GenRe`.

## 2) Public API (test functions in `t_re.py`)
- `test_extract_words_simple()`              — single-space input.
- `test_extract_words_mixed_delimiters()`    — commas, colons,
  parens, newlines, tabs, etc.
- `test_extract_words_with_duplicates()`     — duplicates kept in
  occurrence order.
- `test_extract_words_empty()`               — empty input → `[]`.
- `test_extract_words_only_delimiters()`     — no word chars → `[]`.

## 3) Inheritance (Hierarchy)
None — module of free pytest functions.

## 4) Dependencies
- `pytest` (third-party, run-time).
- `f_psl.re.u_re.URe`           — system under test.
- `f_psl.re.generators.g_re.GenRe` — canonical test inputs.

## 5) Usage Example
```bash
python -m pytest f_psl/re/testers/t_re.py -v
```
