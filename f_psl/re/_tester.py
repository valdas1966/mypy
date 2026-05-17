import pytest

from f_psl.re import URe


def test_extract_words() -> None:
    """
    ========================================================================
     Test the extract_words() method across:
      * simple space-delimited text,
      * text with mixed delimiters (commas, periods, colons, semicolons,
         parentheses, newlines, tabs, question marks),
      * text with duplicate words (order preserved),
      * empty text,
      * text with only delimiters and no words.
    ========================================================================
    """
    # Simple
    text = 'hello world python'
    actual = URe.extract_words(text=text)
    expected = ['hello', 'world', 'python']
    assert actual == expected

    # Mixed delimiters
    text = 'one, two. three: (four)\nfive; six!\tseven?eight'
    actual = URe.extract_words(text=text)
    expected = ['one', 'two', 'three', 'four',
                'five', 'six', 'seven', 'eight']
    assert actual == expected

    # Duplicates preserved in order
    text = 'cat dog cat bird dog cat'
    actual = URe.extract_words(text=text)
    expected = ['cat', 'dog', 'cat', 'bird', 'dog', 'cat']
    assert actual == expected

    # Empty
    text = ''
    actual = URe.extract_words(text=text)
    expected = []
    assert actual == expected

    # Only delimiters
    text = '  , . : ;\n\t () '
    actual = URe.extract_words(text=text)
    expected = []
    assert actual == expected


def test_extract_runs() -> None:
    """
    ========================================================================
     Test the extract_runs() method across:
      * a single ASCII-letter range,
      * multiple ranges (letters + digits) as one alphabet,
      * empty ranges (-> []),
      * lo > hi (-> ValueError),
      * class-special endpoints ([ \\ ] ^ -) escaped correctly,
      * an Arabic code-point range.
    ========================================================================
    """
    # Single ASCII-letter range
    text = 'ab12 cd!ef'
    actual = URe.extract_runs(text=text, ranges=[(0x61, 0x7A)])
    expected = ['ab', 'cd', 'ef']
    assert actual == expected

    # Multiple ranges as one alphabet (a-z + 0-9)
    text = 'ab12 cd!ef'
    actual = URe.extract_runs(text=text, ranges=[(0x61, 0x7A), (0x30, 0x39)])
    expected = ['ab12', 'cd', 'ef']
    assert actual == expected

    # Empty ranges
    text = 'anything'
    actual = URe.extract_runs(text=text, ranges=[])
    expected = []
    assert actual == expected

    # lo > hi raises ValueError
    with pytest.raises(ValueError):
        URe.extract_runs(text='x', ranges=[(0x42, 0x41)])

    # Class-special endpoints ([ \ ] ^ _ -> 0x5B..0x5F) escaped
    text = 'A[\\]^_`a'
    actual = URe.extract_runs(text=text, ranges=[(0x5B, 0x5F)])
    expected = ['[\\]^_']
    assert actual == expected

    # Arabic code-point range
    text = 'مرحبا world'
    actual = URe.extract_runs(text=text, ranges=[(0x0621, 0x064A)])
    expected = ['مرحبا']
    assert actual == expected


def test_strip_ranges() -> None:
    """
    ========================================================================
     Test the strip_ranges() method across:
      * removing a single ASCII range,
      * removing multiple ranges,
      * empty ranges (text unchanged),
      * lo > hi (-> ValueError),
      * removing Arabic harakat while keeping the letters.
    ========================================================================
    """
    # Remove a single ASCII range (digits)
    text = 'a1b2c3'
    actual = URe.strip_ranges(text=text, ranges=[(0x30, 0x39)])
    expected = 'abc'
    assert actual == expected

    # Remove multiple ranges (digits + lowercase)
    text = 'a1B2c3'
    actual = URe.strip_ranges(text=text, ranges=[(0x30, 0x39), (0x61, 0x7A)])
    expected = 'B'
    assert actual == expected

    # Empty ranges -> text unchanged
    text = 'unchanged'
    actual = URe.strip_ranges(text=text, ranges=[])
    expected = 'unchanged'
    assert actual == expected

    # lo > hi raises ValueError
    with pytest.raises(ValueError):
        URe.strip_ranges(text='x', ranges=[(0x42, 0x41)])

    # Remove Arabic harakat, keep the letters
    text = 'كَتَبَ'
    actual = URe.strip_ranges(text=text, ranges=[(0x064B, 0x065F)])
    expected = 'كتب'
    assert actual == expected
