from f_ai.nlp.tokenizers.i_0_single import Tokenizer


def test():
    text = 'a b c'
    tokens = Tokenizer(text=text).to_tokens()
    assert tokens == ['a', 'b', 'c']