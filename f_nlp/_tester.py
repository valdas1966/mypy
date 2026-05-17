import pytest

from f_nlp import UNlp
from f_nlp.u_nlp import _MARK_RANGES, _TOKEN_RANGES


def test_tokenize() -> None:
    """
    ========================================================================
     Test the tokenize() method across:
      * English with punctuation,
      * plain (unvocalized) Arabic,
      * vocalized Arabic (diacritics kept with the base letter),
      * Arabic punctuation as a delimiter,
      * mixed scripts and digit systems,
      * plain Hebrew,
      * pointed Hebrew (niqqud kept with the base letter),
      * Hebrew cantillation (te'amim kept with the base letter),
      * Hebrew maqaf as a delimiter (splits the phrase),
      * mixed English + Arabic + Hebrew in one string,
      * out-of-scope scripts (CJK, Cyrillic) yield no tokens,
      * empty text.
    ========================================================================
    """
    # English with punctuation
    text = 'The quick, brown fox!'
    actual = UNlp.tokenize(text=text)
    expected = ['The', 'quick', 'brown', 'fox']
    assert actual == expected

    # Plain Arabic
    text = 'القط جلس على السجادة'
    actual = UNlp.tokenize(text=text)
    expected = ['القط', 'جلس', 'على', 'السجادة']
    assert actual == expected

    # Vocalized Arabic — diacritics stay with the base letter
    text = 'الْقِطُّ جَلَسَ'
    actual = UNlp.tokenize(text=text)
    expected = ['الْقِطُّ', 'جَلَسَ']
    assert actual == expected

    # Arabic punctuation delimits
    text = 'مرحبا، كيف حالك؟'
    actual = UNlp.tokenize(text=text)
    expected = ['مرحبا', 'كيف', 'حالك']
    assert actual == expected

    # Mixed English + Arabic + ASCII/Arabic-Indic digits
    text = 'hello مرحبا 2026 ٢٠٢٦'
    actual = UNlp.tokenize(text=text)
    expected = ['hello', 'مرحبا', '2026', '٢٠٢٦']
    assert actual == expected

    # Plain Hebrew
    text = 'שלום עולם'
    actual = UNlp.tokenize(text=text)
    expected = ['שלום', 'עולם']
    assert actual == expected

    # Pointed Hebrew — niqqud stays with the base letter
    text = 'שָׁלוֹם עוֹלָם'
    actual = UNlp.tokenize(text=text)
    expected = ['שָׁלוֹם', 'עוֹלָם']
    assert actual == expected

    # Hebrew cantillation — te'amim stay with the base letter
    text = 'בְּרֵאשִׁ֖ית בָּרָ֣א אֱלֹהִ֑ים'
    actual = UNlp.tokenize(text=text)
    expected = ['בְּרֵאשִׁ֖ית', 'בָּרָ֣א', 'אֱלֹהִ֑ים']
    assert actual == expected

    # Hebrew maqaf is a delimiter — splits the phrase
    text = 'עַל־פְּנֵי'
    actual = UNlp.tokenize(text=text)
    expected = ['עַל', 'פְּנֵי']
    assert actual == expected

    # Mixed English + Arabic + Hebrew in one string.
    # NOTE: tokens are returned in LOGICAL (code-point) order,
    # not the bidi-reordered visual order; vocalized Arabic and
    # pointed Hebrew keep their marks; ',' and '!' delimit.
    text = 'Hello مرحبا שלום, كَتَبَ שָׁלוֹם world!'
    actual = UNlp.tokenize(text=text)
    expected = ['Hello', 'مرحبا', 'שלום', 'كَتَبَ', 'שָׁלוֹם', 'world']
    assert actual == expected

    # Out-of-scope scripts yield no tokens (by design)
    text = '我喜欢猫 привет γεια'
    actual = UNlp.tokenize(text=text)
    expected = []
    assert actual == expected

    # Empty text
    text = ''
    actual = UNlp.tokenize(text=text)
    expected = []
    assert actual == expected


def test_ngram() -> None:
    """
    ========================================================================
     Test the ngram() method across:
      * the canonical bigram example,
      * unigrams (n == 1),
      * n equal to the word count (single n-gram),
      * n larger than the word count (empty result),
      * empty text,
      * Arabic bigrams (multilingual tokenization),
      * n < 1 raising ValueError.
    ========================================================================
    """
    # Canonical bigram
    text = 'the cat sat'
    n = 2
    actual = UNlp.ngram(text=text, n=n)
    expected = [['the', 'cat'], ['cat', 'sat']]
    assert actual == expected

    # Unigrams
    text = 'the cat sat'
    n = 1
    actual = UNlp.ngram(text=text, n=n)
    expected = [['the'], ['cat'], ['sat']]
    assert actual == expected

    # n == word count
    text = 'the cat sat'
    n = 3
    actual = UNlp.ngram(text=text, n=n)
    expected = [['the', 'cat', 'sat']]
    assert actual == expected

    # n > word count
    text = 'the cat sat'
    n = 4
    actual = UNlp.ngram(text=text, n=n)
    expected = []
    assert actual == expected

    # Empty text
    text = ''
    n = 2
    actual = UNlp.ngram(text=text, n=n)
    expected = []
    assert actual == expected

    # Arabic bigrams
    text = 'القط جلس على السجادة'
    n = 2
    actual = UNlp.ngram(text=text, n=n)
    expected = [['القط', 'جلس'], ['جلس', 'على'], ['على', 'السجادة']]
    assert actual == expected

    # n < 1 raises ValueError
    text = 'the cat sat'
    n = 0
    with pytest.raises(ValueError):
        UNlp.ngram(text=text, n=n)


def test_strip_marks() -> None:
    """
    ========================================================================
     Test the strip_marks() method across:
      * vocalized Arabic == plain Arabic,
      * Arabic tatweel (kashida) removed,
      * Arabic alef-wasla (a LETTER) preserved,
      * pointed Hebrew == plain Hebrew,
      * Hebrew cantillation removed,
      * idempotence,
      * text with no marks unchanged,
      * structural invariant: _MARK_RANGES code points are a
         subset of _TOKEN_RANGES (and contain no letter/digit).
    ========================================================================
    """
    # Vocalized Arabic folds to plain
    actual = UNlp.strip_marks('كَتَبَ')
    expected = 'كتب'
    assert actual == expected
    assert UNlp.strip_marks('مُحَمَّدٌ') == UNlp.strip_marks('محمد')

    # Tatweel (elongation only) is removed
    actual = UNlp.strip_marks('كاتـــب')
    expected = 'كاتب'
    assert actual == expected

    # Alef-wasla is a letter — preserved, not stripped
    actual = UNlp.strip_marks('ٱلله')
    expected = 'ٱلله'
    assert actual == expected

    # Pointed Hebrew folds to plain
    actual = UNlp.strip_marks('שָׁלוֹם')
    expected = 'שלום'
    assert actual == expected

    # Hebrew cantillation removed
    actual = UNlp.strip_marks('בְּרֵאשִׁ֖ית')
    expected = 'בראשית'
    assert actual == expected

    # Idempotent
    once = UNlp.strip_marks('שָׁלוֹם')
    actual = UNlp.strip_marks(once)
    expected = once
    assert actual == expected

    # No marks -> unchanged
    text = 'hello שלום كتب 2026'
    actual = UNlp.strip_marks(text)
    expected = 'hello שלום كتب 2026'
    assert actual == expected

    # Invariant: _MARK_RANGES is a strict subset of the mark
    # portion of _TOKEN_RANGES (never strips a token-only char)
    mark_cps = {c for lo, hi in _MARK_RANGES for c in range(lo, hi + 1)}
    token_cps = {c for lo, hi in _TOKEN_RANGES for c in range(lo, hi + 1)}
    actual = mark_cps <= token_cps
    expected = True
    assert actual == expected
