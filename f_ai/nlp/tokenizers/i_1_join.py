from f_ai.nlp.tokenizers.i_0_single import TokenizerSingle


class TokenizerJoin(TokenizerSingle):

    _WORDS_JOIN = {'a', 'the', 'and', 'or', 'to', 'of', 'into', 'in', 'within'}

    def _create_token(self) -> str:
        """
        ========================================================================
         Collects all JOIN-WORDS with next non-JOIN-WORDS if exists.
        ========================================================================
        """
        words_token = [self.words.current()]
        if self.words.current() in self._WORDS_JOIN:
            # Collect all join-words.
            words_token += self.words.collect(cond_break=self._cond_break)
            # If there's a next word after the join-words, add it.
            if self.words.current() not in self._WORDS_JOIN:
                words_token.append(self.words.current())
        return ' '.join(words_token)

    def _cond_break(self) -> bool:
        """
        ========================================================================
         Break the Collection if reach non-JOIN-WORD.
        ========================================================================
        """
        return self.words.current() not in self._WORDS_JOIN
