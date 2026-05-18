from f_nlp._internal._strip import _Strip
from f_nlp._internal._policy import _MARK_RANGES, _TOKEN_RANGES


def test_marks() -> None:
    """
    ========================================================================
     Test _Strip.marks() across:
      * vocalized Arabic == plain Arabic,
      * Arabic tatweel (kashida) removed,
      * Arabic alef-wasla (a LETTER) preserved,
      * pointed Hebrew == plain Hebrew,
      * Hebrew cantillation removed,
      * idempotence,
      * text with no marks unchanged.
    ========================================================================
    """
    # Vocalized Arabic folds to plain
    actual = _Strip.marks('كَتَبَ')
    expected = 'كتب'
    assert actual == expected
    assert _Strip.marks('مُحَمَّدٌ') == _Strip.marks('محمد')

    # Tatweel (elongation only) is removed
    actual = _Strip.marks('كاتـــب')
    expected = 'كاتب'
    assert actual == expected

    # Alef-wasla is a letter — preserved, not stripped
    actual = _Strip.marks('ٱلله')
    expected = 'ٱلله'
    assert actual == expected

    # Pointed Hebrew folds to plain
    actual = _Strip.marks('שָׁלוֹם')
    expected = 'שלום'
    assert actual == expected

    # Hebrew cantillation removed
    actual = _Strip.marks('בְּרֵאשִׁ֖ית')
    expected = 'בראשית'
    assert actual == expected

    # Idempotent
    once = _Strip.marks('שָׁלוֹם')
    actual = _Strip.marks(once)
    expected = once
    assert actual == expected

    # No marks -> unchanged
    text = 'hello שלום كتب 2026'
    actual = _Strip.marks(text)
    expected = 'hello שלום كتب 2026'
    assert actual == expected


def test_diacritics() -> None:
    """
    ========================================================================
     Test _Strip.diacritics() alias across:
      * vocalized Arabic == plain Arabic,
      * pointed/cantillated Hebrew == plain Hebrew,
      * Arabic alef-wasla (a LETTER) preserved,
      * idempotence,
      * identical to _Strip.marks (delegation invariant),
      * text with no marks unchanged.
    ========================================================================
    """
    # Vocalized Arabic folds to plain
    actual = _Strip.diacritics('كَتَبَ')
    expected = 'كتب'
    assert actual == expected

    # Cantillated Hebrew folds to plain
    actual = _Strip.diacritics('בְּרֵאשִׁ֖ית')
    expected = 'בראשית'
    assert actual == expected

    # Alef-wasla is a letter — preserved
    actual = _Strip.diacritics('ٱلله')
    expected = 'ٱلله'
    assert actual == expected

    # Idempotent
    once = _Strip.diacritics('שָׁלוֹם')
    actual = _Strip.diacritics(once)
    expected = once
    assert actual == expected

    # Delegation invariant: identical to _Strip.marks
    text = 'مُحَمَّدٌ שָׁלוֹם hello 2026'
    actual = _Strip.diacritics(text)
    expected = _Strip.marks(text)
    assert actual == expected

    # No marks -> unchanged
    text = 'hello שלום كتب 2026'
    actual = _Strip.diacritics(text)
    expected = 'hello שלום كتب 2026'
    assert actual == expected


def test_policy_subset_invariant() -> None:
    """
    ========================================================================
     Structural invariant guarding _Strip correctness:
      _MARK_RANGES code points are a strict subset of
      _TOKEN_RANGES (stripping never removes a token-only
      char; Arabic alef-wasla U+0671 stays a letter).
    ========================================================================
    """
    # _MARK_RANGES is a subset of the mark portion of _TOKEN_RANGES
    mark_cps = {c for lo, hi in _MARK_RANGES for c in range(lo, hi + 1)}
    token_cps = {c for lo, hi in _TOKEN_RANGES for c in range(lo, hi + 1)}
    actual = mark_cps <= token_cps
    expected = True
    assert actual == expected
