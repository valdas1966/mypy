from f_nlp._internal._token import _Token


def test_ize() -> None:
    """
    ========================================================================
     Test _Token.ize() across:
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
    actual = _Token.ize(text=text)
    expected = ['The', 'quick', 'brown', 'fox']
    assert actual == expected

    # Plain Arabic
    text = 'القط جلس على السجادة'
    actual = _Token.ize(text=text)
    expected = ['القط', 'جلس', 'على', 'السجادة']
    assert actual == expected

    # Vocalized Arabic — diacritics stay with the base letter
    text = 'الْقِطُّ جَلَسَ'
    actual = _Token.ize(text=text)
    expected = ['الْقِطُّ', 'جَلَسَ']
    assert actual == expected

    # Arabic punctuation delimits
    text = 'مرحبا، كيف حالك؟'
    actual = _Token.ize(text=text)
    expected = ['مرحبا', 'كيف', 'حالك']
    assert actual == expected

    # Mixed English + Arabic + ASCII/Arabic-Indic digits
    text = 'hello مرحبا 2026 ٢٠٢٦'
    actual = _Token.ize(text=text)
    expected = ['hello', 'مرحبا', '2026', '٢٠٢٦']
    assert actual == expected

    # Plain Hebrew
    text = 'שלום עולם'
    actual = _Token.ize(text=text)
    expected = ['שלום', 'עולם']
    assert actual == expected

    # Pointed Hebrew — niqqud stays with the base letter
    text = 'שָׁלוֹם עוֹלָם'
    actual = _Token.ize(text=text)
    expected = ['שָׁלוֹם', 'עוֹלָם']
    assert actual == expected

    # Hebrew cantillation — te'amim stay with the base letter
    text = 'בְּרֵאשִׁ֖ית בָּרָ֣א אֱלֹהִ֑ים'
    actual = _Token.ize(text=text)
    expected = ['בְּרֵאשִׁ֖ית', 'בָּרָ֣א', 'אֱלֹהִ֑ים']
    assert actual == expected

    # Hebrew maqaf is a delimiter — splits the phrase
    text = 'עַל־פְּנֵי'
    actual = _Token.ize(text=text)
    expected = ['עַל', 'פְּנֵי']
    assert actual == expected

    # Mixed English + Arabic + Hebrew in one string.
    # NOTE: tokens are returned in LOGICAL (code-point) order,
    # not the bidi-reordered visual order; vocalized Arabic and
    # pointed Hebrew keep their marks; ',' and '!' delimit.
    text = 'Hello مرحبا שלום, كَتَبَ שָׁלוֹם world!'
    actual = _Token.ize(text=text)
    expected = ['Hello', 'مرحبا', 'שלום', 'كَتَبَ', 'שָׁלוֹם', 'world']
    assert actual == expected

    # Out-of-scope scripts yield no tokens (by design)
    text = '我喜欢猫 привет γεια'
    actual = _Token.ize(text=text)
    expected = []
    assert actual == expected

    # Empty text
    text = ''
    actual = _Token.ize(text=text)
    expected = []
    assert actual == expected
