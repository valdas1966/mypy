from f_ai.nlp.tokenizers.i_0_single import TokenizerSingle


class TokenizerJoin(TokenizerSingle):

    _WORDS_JOIN = {'a', 'the', 'and', 'or', 'to', 'of', 'into', 'in', 'within'}

    def _create_token(self) -> str:
        li = list()
        while self.words.has_next():
            word = self.words.next()
            if word in self._WORDS_JOIN:
                li.append(word)
            else:
                break

        li.append(self.words.current())
