from f_ai.nlp.tokenizers.i_0_single import TokenizerSingle, Group


def test():
    text = 'a b c'
    tokens = TokenizerSingle(text=text).to_tokens()
    assert tokens == Group(data=['a', 'b', 'c'])