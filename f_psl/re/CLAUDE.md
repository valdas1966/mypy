# `f_psl/re` — Regex Utilities

## 1) Purpose
Thin wrapper around the Python standard-library `re` module.
Exposes a single static utility class, `URe`, that groups
regex-based helpers used across the framework.

## 2) Public API

### `URe` (`u_re.py`)
- `URe.extract_words(text: str) -> list[str]`
  Returns a list of words from `text`, in the order they
  appear. A "word" is a maximal sequence of word-characters
  `[A-Za-z0-9_]`; every other character (spaces, commas,
  periods, parentheses, colons, semicolons, newlines, tabs,
  etc.) acts as a delimiter. Duplicates are preserved in
  their original order of occurrence. Returns `[]` for empty
  input or input that contains no word-characters.

- `URe.extract_runs(text: str, ranges: Iterable[tuple[int, int]])
  -> list[str]`
  Returns all maximal runs of in-range characters, in order. A
  character qualifies iff its code point lies in any inclusive
  `(lo, hi)` range; any other character delimits. Duplicates
  preserved. Empty `ranges` → `[]`; raises `ValueError` if any
  `lo > hi`. The compiled pattern is **cached per distinct
  ranges** (no recompile on repeated calls). Class-special
  endpoints (`] \ ^ - [`) are escaped, so arbitrary ranges are
  handled correctly. This is the generic regex seam used by
  `f_nlp.UNlp.tokenize` (which supplies the language code-point
  policy and owns no regex itself).

- `URe.strip_ranges(text: str, ranges: Iterable[tuple[int, int]])
  -> str`
  The **dual** of `extract_runs`: returns `text` with every
  in-range character removed. Empty `ranges` → `text`
  unchanged; raises `ValueError` if any `lo > hi`. Uses the
  same cached, class-safe compiled pattern. Used by
  `f_nlp.UNlp.strip_marks` for diacritic-insensitive folding.

No `Factory` — `URe` is purely static (no instances). Test
inputs are inlined in `_tester.py`.

## 3) Inheritance (Hierarchy)
`URe` is a stand-alone **static utility class** — no instances,
no base class. Follows the `U`-prefix convention for purely
static utility classes.

## 4) Dependencies
- `re`, `collections.abc.Iterable` (in `u_re.py`);
  `re`, `functools.lru_cache` (in `_ranges.py`).
  Python standard library only.

## 5) Usage Example
```python
from f_psl.re import URe

URe.extract_words(text='hello, world! hello.')
# ['hello', 'world', 'hello']

URe.extract_words(text='one, two. three: (four)\nfive; six')
# ['one', 'two', 'three', 'four', 'five', 'six']

URe.extract_runs(text='ab12 cd!ef',
                 ranges=[(0x61, 0x7A), (0x30, 0x39)])
# ['ab12', 'cd', 'ef']
```

## Files
| File | Purpose |
|------|---------|
| `u_re.py` | `URe` class only. |
| `_ranges.py` | Internal: cached `compiled_class()` + class-safe `_cls()`. |
| `__init__.py` | Re-exports `URe`. |
| `_tester.py` | pytest; `extract_words` + `extract_runs` + `strip_ranges`, 4-line structural. |
