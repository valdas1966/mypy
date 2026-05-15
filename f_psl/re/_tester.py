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
