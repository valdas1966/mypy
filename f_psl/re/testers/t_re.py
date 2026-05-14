from f_psl.re.generators.g_re import GenRe
from f_psl.re.u_re import URe


def test_extract_words_simple() -> None:
    """
    ========================================================================
     Test the extract_words() method on a space-delimited Text.
    ========================================================================
    """
    text = GenRe.simple()
    assert URe.extract_words(text=text) == ['hello', 'world', 'python']


def test_extract_words_mixed_delimiters() -> None:
    """
    ========================================================================
     Test the extract_words() method on a Text with mixed delimiters.
    ========================================================================
    """
    text = GenRe.mixed_delimiters()
    expected = ['one', 'two', 'three', 'four',
                'five', 'six', 'seven', 'eight']
    assert URe.extract_words(text=text) == expected


def test_extract_words_with_duplicates() -> None:
    """
    ========================================================================
     Test the extract_words() method: duplicate words are preserved
      in their original order of occurrence.
    ========================================================================
    """
    text = GenRe.with_duplicates()
    expected = ['cat', 'dog', 'cat', 'bird', 'dog', 'cat']
    assert URe.extract_words(text=text) == expected


def test_extract_words_empty() -> None:
    """
    ========================================================================
     Test the extract_words() method on an empty Text.
    ========================================================================
    """
    text = GenRe.empty()
    assert URe.extract_words(text=text) == []


def test_extract_words_only_delimiters() -> None:
    """
    ========================================================================
     Test the extract_words() method on a Text that contains only
      delimiters and no words.
    ========================================================================
    """
    text = GenRe.only_delimiters()
    assert URe.extract_words(text=text) == []
