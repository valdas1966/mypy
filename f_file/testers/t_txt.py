import pytest
from f_file.txt import Txt

s = 'Hello\nWorld!'
path = 'd:\\test.txt'


@pytest.fixture
def ex() -> Txt:
    return Txt.from_str(s=s, path=path)


def test_from_str(ex):
    assert str(ex) == s


def test_from_lines():
    txt = Txt.from_lines(lines=['Hello', 'World!'], path=path)
    assert str(txt) == s


def test_repr(ex):
    assert repr(ex) == '<Txt: d:\\test.txt>'


def test_iter(ex):
    assert list(ex) == ['Hello', 'World!']


def test_add_line(ex):
    ex.add_line(line='A', index=0)
    assert list(ex) == ['A', 'Hello', 'World!']
    ex.add_line(line='B')
    assert list(ex) == ['A', 'Hello', 'World!', 'B']
