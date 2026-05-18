from f_nlp import UNlp
from f_nlp._internal._token import _Token
from f_nlp._internal._strip import _Strip
from f_nlp._internal._ngram import _Ngram


def test_facade_wiring() -> None:
    """
    ========================================================================
     Facade wiring only — behavior is covered by each concern's
      own _tester.py under f_nlp/_internal/<concern>/. This file
      asserts that UNlp exposes the concerns correctly:
      * strip / ngram namespaces bound to the right classes,
      * flat tokenize delegates to _Token.ize.
    ========================================================================
    """
    # strip namespace is the _Strip concern class
    actual = UNlp.strip
    expected = _Strip
    assert actual is expected

    # ngram namespace is the _Ngram concern class
    actual = UNlp.ngram
    expected = _Ngram
    assert actual is expected

    # Flat UNlp.tokenize delegates to _Token.ize
    text = 'Hello مرحبا שָׁלוֹם, the cat!'
    actual = UNlp.tokenize(text=text)
    expected = _Token.ize(text=text)
    assert actual == expected

    # Namespaced calls reach the concern methods unchanged
    actual = UNlp.ngram.exact(text='the cat sat', n=2)
    expected = _Ngram.exact(text='the cat sat', n=2)
    assert actual == expected

    # strip.marks reachable through the facade namespace
    actual = UNlp.strip.marks('كَتَبَ')
    expected = _Strip.marks('كَتَبَ')
    assert actual == expected
