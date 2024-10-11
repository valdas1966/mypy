from f_ai.nlp.tokenizers.i_1_join import TokenizerJoin
import pytest


@pytest.fixture
def ex_1() -> str:
    return 'hello world'


@pytest.fixture
def ex_2() -> str:
    return 'hello to world'


@pytest.fixture
def ex_3() -> str:
    return 'hello to the world'


@pytest.fixture
def ex_4() -> str:
    return 'hello to'


def test(ex_1, ex_2, ex_3, ex_4):
    tokens = TokenizerJoin(text=ex_1).to_tokens()
    assert tokens.data == ['hello', 'world']
    tokens = TokenizerJoin(text=ex_2).to_tokens()
    assert tokens.data == ['hello', 'to world']
    tokens = TokenizerJoin(text=ex_3).to_tokens()
    assert tokens.data == ['hello', 'to the world']
    tokens = TokenizerJoin(text=ex_4).to_tokens()
    assert tokens.data == ['hello', 'to']

