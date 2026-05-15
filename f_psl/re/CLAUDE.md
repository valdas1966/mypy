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

No `Factory` — `URe` is purely static (no instances). Test
inputs are inlined in `_tester.py`.

## 3) Inheritance (Hierarchy)
`URe` is a stand-alone **static utility class** — no instances,
no base class. Follows the `U`-prefix convention for purely
static utility classes.

## 4) Dependencies
- `re` (Python standard library).

## 5) Usage Example
```python
from f_psl.re import URe

URe.extract_words(text='hello, world! hello.')
# ['hello', 'world', 'hello']

URe.extract_words(text='one, two. three: (four)\nfive; six')
# ['one', 'two', 'three', 'four', 'five', 'six']
```

## Files
| File | Purpose |
|------|---------|
| `u_re.py` | `URe` class. |
| `__init__.py` | Re-exports `URe`. |
| `_tester.py` | Single pytest test bundling all asserts. |
