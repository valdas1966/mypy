# `f_nlp` — NLP Utilities

## 1) Purpose
`UNlp` is the single public **facade** for natural-language
helpers: multilingual tokenization, n-gram extraction, and
diacritic stripping. Per-concern logic is decomposed into
private classes under `f_nlp/_internal/`; `UNlp` binds them as
**namespaces**. `f_nlp` owns only the **language policy** (which
code points are word characters / marks); **all regex mechanism
lives in `f_psl/re`** (`URe`). No file under `f_nlp` imports
`re`.

## 2) Public API

`UNlp` (`u_nlp.py`) is the only entry point. Shape:

| Call | Concern class | Returns |
|------|---------------|---------|
| `UNlp.tokenize(text)` | `_Token` | `list[str]` |
| `UNlp.strip.marks(s)` | `_Strip` | `str` |
| `UNlp.strip.diacritics(text)` | `_Strip` | `str` |
| `UNlp.ngram.exact(text, n)` | `_Ngram` | `list[list[str]]` |
| `UNlp.ngram.upto(text, n)` | `_Ngram` | `list[list[str]]` |
| `UNlp.ngram.doc_freq(texts, n)` | `_Ngram` | `Counter[tuple[str, ...]]` |

`tokenize` is **flat** (a single operation — no one-method
namespace); `strip` and `ngram` are namespaces because each has
≥2 related operations.

- `UNlp.tokenize(text: str) -> list[str]`
  Word tokenizer scoped to **English + Arabic + Hebrew only**.
  Owns only `_TOKEN_RANGES` (integer `(lo, hi)` code-point
  ranges; no `\w`, no RTL literals; hand-typable, 1:1 verifiable
  against the Unicode charts) — delegates the regex to
  `URe.extract_runs`. Keeps combining marks attached to their
  base letter: Arabic harakat/tanwin/superscript-alef/tatweel/
  Quranic signs, Hebrew niqqud + cantillation (te'amim). So
  vocalized Arabic (`الْقِطُّ`) and pointed/cantillated Hebrew
  (`שָׁלוֹם`, `בְּרֵאשִׁ֖ית`) are one token. Whitespace and
  punctuation (incl. Arabic `،`/`؟` and Hebrew maqaf `־`/paseq/
  sof-pasuq) delimit. ASCII + Arabic-Indic digits and `_` are
  token chars. Duplicates preserved. **Tokenization only** — no
  normalization (stripping is the `UNlp.strip` concern). **By
  design:** any other script (Cyrillic, Greek, CJK, ...) yields
  no tokens.

- `UNlp.ngram.exact(text: str, n: int) -> list[list[str]]`
  All n-grams of `text`, in order. Tokenizes, then windows via
  `UList.sliding_windows`. For `W` words, `n >= 1`: `W - n + 1`
  n-grams; `[]` when `n > W`. `ValueError` when `n < 1`. Return
  is token-window form; join with `' '` at the call site for a
  string form. Example: `ngram.exact(text='the cat sat', n=2)
  -> [['the','cat'], ['cat','sat']]`.

- `UNlp.ngram.upto(text: str, n: int) -> list[list[str]]`
  Size-union of `ngram.exact`: every n-gram of size `1..n`
  inclusive, **grouped by size ascending** (all 1-grams, then
  all 2-grams, ...; each group keeps word order). `ngram.exact`
  stays the single-size primitive — this only composes it (no
  flag, no `(lo,hi)` parameter), so the length-`k` invariant
  holds per group. Sizes `k > W` contribute nothing (graceful).
  `ValueError` when `n < 1`. Example:
  `ngram.upto(text='the cat sat', n=2) ->
  [['the'], ['cat'], ['sat'], ['the','cat'], ['cat','sat']]`.

- `UNlp.ngram.doc_freq(texts: list[str], n: int) ->
  Counter[tuple[str, ...]]`
  **Document frequency** of n-grams over a corpus: for each
  n-gram, how many of the input `texts` contain it — *not*
  total occurrences. A repeat inside the same text is counted
  **once** for that text (per-text presence, deduplicated).
  Keys are the hashable `tuple` form of `ngram.exact`'s
  `list[str]` windows (lossless, collision-free — no
  string-join). Texts with `< n` words contribute nothing;
  empty corpus → empty `Counter`. Composes `ngram.exact`; no
  new tokenization logic. `ValueError` when `n < 1` (fail-fast,
  even for an empty corpus). Example:
  `ngram.doc_freq(texts=['the cat sat','the cat ran'], n=2) ->
  Counter({('the','cat'):2, ('cat','sat'):1, ('cat','ran'):1})`.

- `UNlp.strip.marks(s: str) -> str`
  Diacritic-insensitive **fold for comparison**: removes the
  optional Arabic/Hebrew marks (`_MARK_RANGES` — harakat,
  tanwin, tatweel, Quranic signs, Hebrew niqqud/te'amim/dagesh,
  shin/sin dots) while keeping base letters. Delegates the
  regex to `URe.strip_ranges`. Idempotent. Use for equality:
  `UNlp.strip.marks(a) == UNlp.strip.marks(b)`. `tokenize` /
  `ngram.*` stay **lossless** — fold at the call site when
  equality is wanted; `_MARK_RANGES` is a strict subset of the
  mark portion of `_TOKEN_RANGES` (never strips a token-only
  char; Arabic alef-wasla U+0671 is a letter and is preserved).
  **Linguistic note:** folding merges some phonemic
  distinctions on purpose (Hebrew shin שׁ vs sin שׂ, dagesh;
  Arabic shadda gemination) — that *is* "compare only the solid
  letters". Not a normalizer (no alef/taa-marbuta unification).

- `UNlp.strip.diacritics(text: str) -> str`
  Discoverable **alias of `strip.marks`** — same `_MARK_RANGES`
  policy, same `URe.strip_ranges` mechanism, no new logic
  (delegation is asserted in `_tester.py`). Removes all Hebrew
  (niqqud + te'amim/cantillation + dagesh + shin/sin dots) and
  all Arabic (harakat, tanwin, tatweel, Quranic signs)
  diacritics; base letters incl. alef-wasla preserved.
  Idempotent. Use when a caller wants clean consonantal text
  rather than specifically an equality fold. **Layering:** the
  Hebrew/Arabic *policy* stays in `f_nlp`; `URe` remains
  language-agnostic (no language-specific strip in `f_psl/re`).

## 3) Architecture / Hierarchy
`UNlp` is a stand-alone **static utility facade** (`U`-prefix,
no instances, no base, no `_factory.py`). It holds **no logic**
— only a flat `tokenize` delegator plus the `strip` / `ngram`
namespace bindings. All implementation lives in private
per-concern static classes:

```
f_nlp/
  u_nlp.py            UNlp facade (tokenize flat; strip=_Strip; ngram=_Ngram)
  __init__.py         re-exports UNlp (eager leaf wiring)
  _tester.py          pytest; facade-WIRING assertions only
  _internal/
    _policy.py        _TOKEN_RANGES, _MARK_RANGES (flat shared-data module)
    _token/           class module: main.py _tester.py __init__ CLAUDE.md
    _strip/           class module: main.py _tester.py __init__ CLAUDE.md
    _ngram/           class module: main.py _tester.py __init__ CLAUDE.md
```

Decomposition rule: each internal **class** is its own
folder-per-class module (`main.py` + `__init__.py` +
`_tester.py` + `CLAUDE.md`) — the framework's standard class
module shape, not inner classes, not separate public classes.
`_policy.py` stays a **flat shared-data module** (no class →
no folder); its subset invariant is tested in
`_strip/_tester.py`. The single `UNlp` entry point is
preserved; callers reach concerns by namespace.

**Testing split:** behavior is tested per concern in
`_internal/<concern>/_tester.py` (against the private class
directly); `f_nlp/_tester.py` is reduced to facade-wiring
assertions (namespace identity + delegation), so logic is not
double-tested. `_tester.py` files are run by explicit path
(pytest does not auto-discover the `_tester.py` name).

## 4) Dependencies
- `f_psl.re.u_re.URe` — **all** regex mechanism
  (`extract_runs`, `strip_ranges`); no `f_nlp` file imports
  `re`.
- `f_psl.builtins.list.main.UList` — sliding-window logic.
- `collections.Counter` (stdlib) — `ngram.doc_freq` return.
- No third-party NLP dependency (no `nltk`, no `pandas`).

> **Layering rule.** All regex context lives in `URe`; `f_nlp`
> holds only the language *policy* (`_policy.py`) and delegates.

## 5) Usage Example
```python
from f_nlp import UNlp

UNlp.tokenize(text='مرحبا، كيف حالك؟')      # ['مرحبا','كيف','حالك']
UNlp.tokenize(text='שָׁלוֹם עוֹלָם')          # ['שָׁלוֹם','עוֹלָם']

UNlp.ngram.exact(text='the quick brown fox', n=2)
# [['the','quick'], ['quick','brown'], ['brown','fox']]
UNlp.ngram.upto(text='the cat sat', n=2)
# [['the'],['cat'],['sat'],['the','cat'],['cat','sat']]
UNlp.ngram.doc_freq(texts=['the cat sat','the cat ran'], n=2)
# Counter({('the','cat'):2, ('cat','sat'):1, ('cat','ran'):1})

# Diacritic-insensitive equality (tokens stay lossless)
UNlp.strip.marks('שָׁלוֹם') == UNlp.strip.marks('שלום')   # True
UNlp.strip.diacritics('كَتَبَ')                            # 'كتب'
```
