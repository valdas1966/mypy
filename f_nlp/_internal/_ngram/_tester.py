from collections import Counter

import pytest

from f_nlp._internal._ngram import _Ngram


def test_exact() -> None:
    """
    ========================================================================
     Test _Ngram.exact() across:
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
    actual = _Ngram.exact(text=text, n=n)
    expected = [['the', 'cat'], ['cat', 'sat']]
    assert actual == expected

    # Unigrams
    text = 'the cat sat'
    n = 1
    actual = _Ngram.exact(text=text, n=n)
    expected = [['the'], ['cat'], ['sat']]
    assert actual == expected

    # n == word count
    text = 'the cat sat'
    n = 3
    actual = _Ngram.exact(text=text, n=n)
    expected = [['the', 'cat', 'sat']]
    assert actual == expected

    # n > word count
    text = 'the cat sat'
    n = 4
    actual = _Ngram.exact(text=text, n=n)
    expected = []
    assert actual == expected

    # Empty text
    text = ''
    n = 2
    actual = _Ngram.exact(text=text, n=n)
    expected = []
    assert actual == expected

    # Arabic bigrams
    text = 'القط جلس على السجادة'
    n = 2
    actual = _Ngram.exact(text=text, n=n)
    expected = [['القط', 'جلس'], ['جلس', 'على'], ['على', 'السجادة']]
    assert actual == expected

    # n < 1 raises ValueError
    text = 'the cat sat'
    n = 0
    with pytest.raises(ValueError):
        _Ngram.exact(text=text, n=n)


def test_upto() -> None:
    """
    ========================================================================
     Test _Ngram.upto() across:
      * the canonical n == 2 case (unigrams then bigrams),
      * n == 1 (identical to exact with n == 1),
      * n == word count (all sizes, last is the whole text),
      * n > word count (oversized sizes contribute nothing),
      * empty text,
      * Arabic up-to-2 (multilingual tokenization),
      * n < 1 raising ValueError.
    ========================================================================
    """
    # Canonical: sizes 1..2, grouped by size ascending
    text = 'the cat sat'
    n = 2
    actual = _Ngram.upto(text=text, n=n)
    expected = [['the'], ['cat'], ['sat'],
                ['the', 'cat'], ['cat', 'sat']]
    assert actual == expected

    # n == 1 equals exact(n=1)
    text = 'the cat sat'
    n = 1
    actual = _Ngram.upto(text=text, n=n)
    expected = [['the'], ['cat'], ['sat']]
    assert actual == expected

    # n == word count — top size is the whole text
    text = 'the cat sat'
    n = 3
    actual = _Ngram.upto(text=text, n=n)
    expected = [['the'], ['cat'], ['sat'],
                ['the', 'cat'], ['cat', 'sat'],
                ['the', 'cat', 'sat']]
    assert actual == expected

    # n > word count — oversized sizes contribute nothing
    text = 'the cat'
    n = 4
    actual = _Ngram.upto(text=text, n=n)
    expected = [['the'], ['cat'], ['the', 'cat']]
    assert actual == expected

    # Empty text
    text = ''
    n = 3
    actual = _Ngram.upto(text=text, n=n)
    expected = []
    assert actual == expected

    # Arabic up-to-2
    text = 'القط جلس على'
    n = 2
    actual = _Ngram.upto(text=text, n=n)
    expected = [['القط'], ['جلس'], ['على'],
                ['القط', 'جلس'], ['جلس', 'على']]
    assert actual == expected

    # n < 1 raises ValueError
    text = 'the cat sat'
    n = 0
    with pytest.raises(ValueError):
        _Ngram.upto(text=text, n=n)


def test_doc_freq() -> None:
    """
    ========================================================================
     Test _Ngram.doc_freq() across:
      * the canonical 2-text shared-bigram case,
      * a repeat inside one text counted once (presence, not
         total occurrences),
      * a text shorter than n contributing nothing,
      * empty corpus -> empty Counter,
      * Arabic unigrams across texts (multilingual),
      * n < 1 raising ValueError even for an empty corpus.
    ========================================================================
    """
    # Canonical: shared bigram across two texts
    texts = ['the cat sat', 'the cat ran']
    n = 2
    actual = _Ngram.doc_freq(texts=texts, n=n)
    expected = Counter({('the', 'cat'): 2,
                        ('cat', 'sat'): 1, ('cat', 'ran'): 1})
    assert actual == expected

    # Repeat inside ONE text counted once (df, not total)
    texts = ['ba ba ba']
    n = 2
    actual = _Ngram.doc_freq(texts=texts, n=n)
    expected = Counter({('ba', 'ba'): 1})
    assert actual == expected

    # A text shorter than n contributes nothing
    texts = ['hi', 'a b c']
    n = 2
    actual = _Ngram.doc_freq(texts=texts, n=n)
    expected = Counter({('a', 'b'): 1, ('b', 'c'): 1})
    assert actual == expected

    # Empty corpus -> empty Counter
    texts = []
    n = 2
    actual = _Ngram.doc_freq(texts=texts, n=n)
    expected = Counter()
    assert actual == expected

    # Arabic unigrams across texts
    texts = ['القط جلس', 'القط نام']
    n = 1
    actual = _Ngram.doc_freq(texts=texts, n=n)
    expected = Counter({('القط',): 2, ('جلس',): 1, ('نام',): 1})
    assert actual == expected

    # n < 1 raises ValueError even for an empty corpus
    texts = []
    n = 0
    with pytest.raises(ValueError):
        _Ngram.doc_freq(texts=texts, n=n)
