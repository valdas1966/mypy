# `f_nlp` — NLP Utilities

## 1) Purpose
Static utility class `UNlp` for natural-language helpers:
multilingual tokenization and n-gram extraction. This module
owns only the **language policy** (which code points are word
characters); **all regex mechanism lives in `f_psl/re`**
(`URe.extract_runs`). `u_nlp.py` imports no `re`.

## 2) Public API

### `UNlp` (`u_nlp.py`)

- `UNlp.tokenize(text: str) -> list[str]`
  Word tokenizer scoped to **English + Arabic + Hebrew only**.
  Owns only `_TOKEN_RANGES` — a tuple of integer `(lo, hi)`
  code-point ranges (no `\w`, no RTL literals; hand-typable,
  1:1 verifiable against the Unicode charts) — and delegates
  the regex entirely to `URe.extract_runs(text, _TOKEN_RANGES)`.
  Keeps combining
  marks attached to their base letter: Arabic harakat/tanwin/
  superscript-alef/tatweel/Quranic signs, and Hebrew niqqud +
  cantillation (te'amim). So vocalized Arabic (`الْقِطُّ`) and
  pointed/cantillated Hebrew (`שָׁלוֹם`, `בְּרֵאשִׁ֖ית`) are one
  token, not many. Whitespace and punctuation (incl. Arabic
  `،`/`؟` and Hebrew maqaf `־`/paseq/sof-pasuq) delimit.
  ASCII + Arabic-Indic digits and `_` are token chars.
  Duplicates preserved. **Tokenization only** — no
  normalization (diacritic stripping / alef unification is a
  separate concern). **By design:** letters of any other
  script (Cyrillic, Greek, CJK, ...) are not matched —
  out-of-scope text yields no tokens.

- `UNlp.ngram(text: str, n: int) -> list[list[str]]`
  All n-grams of `text`, in order. Tokenizes via
  `UNlp.tokenize`, then windows via `UList.sliding_windows`.
  For `W` words and window `n` (`n >= 1`): `W - n + 1` n-grams;
  `[]` when `n > W`. Raises `ValueError` when `n < 1`. Return
  shape is token-window form (`list[list[str]]`); join with
  `' '` at the call site for a string form.
  Example: `ngram(text='the cat sat', n=2) ->
  [['the', 'cat'], ['cat', 'sat']]`.

- `UNlp.strip_marks(s: str) -> str`
  Diacritic-insensitive **fold for comparison**: removes the
  optional Arabic/Hebrew marks (`_MARK_RANGES` — harakat,
  tanwin, tatweel, Quranic signs, Hebrew niqqud/te'amim/dagesh,
  shin/sin dots) while keeping base letters. Delegates the
  regex to `URe.strip_ranges`. Idempotent. Use for equality:
  `UNlp.strip_marks(a) == UNlp.strip_marks(b)`. `tokenize` /
  `ngram` stay **lossless** — fold at the call site when
  equality is wanted; `_MARK_RANGES` is a strict subset of the
  mark portion of `_TOKEN_RANGES` (never strips a token-only
  char; Arabic alef-wasla U+0671 is a letter and is preserved).
  **Linguistic note:** folding merges some phonemic
  distinctions on purpose (Hebrew shin שׁ vs sin שׂ, dagesh;
  Arabic shadda gemination) — that *is* "compare only the solid
  letters". Not a normalizer (no alef/taa-marbuta unification).

## 3) Inheritance (Hierarchy)
`UNlp` is a stand-alone **static utility class** (`U`-prefix,
no instances, no base, no `_factory.py`).

## 4) Dependencies
- `f_psl.re.u_re.URe` — **all** regex mechanism
  (`URe.extract_runs`); `u_nlp.py` imports no `re`.
- `f_psl.builtins.list.main.UList` — sliding-window logic.
- No third-party NLP dependency (no `nltk`).

> **Layering rule (supersedes the earlier in-session stance).**
> All regex context lives in `URe`; `UNlp` holds only the
> tokenization *policy* (`_TOKEN_RANGES`) and delegates. The
> previously documented "not `URe`" decision was reversed by
> explicit architectural direction.

## 5) Usage Example
```python
from f_nlp import UNlp

UNlp.tokenize(text='مرحبا، كيف حالك؟')   # Arabic
# ['مرحبا', 'كيف', 'حالك']
UNlp.tokenize(text='שָׁלוֹם עוֹלָם')          # pointed Hebrew
# ['שָׁלוֹם', 'עוֹלָם']

UNlp.ngram(text='the quick brown fox', n=2)
# [['the', 'quick'], ['quick', 'brown'], ['brown', 'fox']]

UNlp.tokenize(text='Hello مرحبا שלום, كَتَبَ שָׁלוֹם world!')
# ['Hello','مرحبا','שלום','كَتَبَ','שָׁלוֹם','world']
# (LOGICAL/code-point order — not bidi visual order)

# Diacritic-insensitive equality (tokens stay lossless)
UNlp.strip_marks('שָׁלוֹם') == UNlp.strip_marks('שלום')   # True
UNlp.strip_marks('كَتَبَ')  == UNlp.strip_marks('كتب')     # True
```

## Files
| File | Purpose |
|------|---------|
| `u_nlp.py` | `UNlp` + `_TOKEN_RANGES` / `_MARK_RANGES` (policy). |
| `__init__.py` | Re-exports `UNlp` (eager leaf wiring). |
| `_tester.py` | pytest; 4-line structural cases. |
