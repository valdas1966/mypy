# `f_psl/re/generators` — Regex Test-Input Generators

## 1) Purpose
Provides canonical text samples used by the `f_psl.re` testers.
Centralising inputs keeps `t_re.py` declarative and lets multiple
tests share the same fixtures by name.

## 2) Public API

### `GenRe` (`g_re.py`)
- `GenRe.simple()             -> str` — space-delimited sentence.
- `GenRe.mixed_delimiters()   -> str` — commas, periods, colons,
  semicolons, parentheses, newlines, tabs, question marks.
- `GenRe.with_duplicates()    -> str` — words repeated for
  occurrence-order tests.
- `GenRe.empty()              -> str` — empty string.
- `GenRe.only_delimiters()    -> str` — only delimiters, no words.

## 3) Inheritance (Hierarchy)
`GenRe` is a stand-alone static class (no instances, no base).
Mirrors the `Gen<Name>` convention used in `f_psl/json/generators`.

## 4) Dependencies
- None.

## 5) Usage Example
```python
from f_psl.re.generators.g_re import GenRe
from f_psl.re.u_re import URe

URe.extract_words(text=GenRe.mixed_delimiters())
# ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight']
```
