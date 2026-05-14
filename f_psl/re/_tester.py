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
    assert URe.extract_words(text=text) == ['hello', 'world', 'python']

    # Mixed delimiters
    text = 'one, two. three: (four)\nfive; six!\tseven?eight'
    assert URe.extract_words(text=text) == ['one', 'two', 'three', 'four',
                                            'five', 'six', 'seven', 'eight']

    # Duplicates preserved in order
    text = 'cat dog cat bird dog cat'
    assert URe.extract_words(text=text) == ['cat', 'dog', 'cat',
                                            'bird', 'dog', 'cat']

    # Empty
    text = ''
    assert URe.extract_words(text=text) == []

    # Only delimiters
    text = '  , . : ;\n\t () '
    assert URe.extract_words(text=text) == []
