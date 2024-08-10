from f_utils.dtypes.u_list import UList as u_list


class Mask:
    """
    ============================================================================
     Utils-Class for applying masking techniques to Strings.
    ============================================================================
    """

    _EXCEPTIONS = (' ', '"', "'")

    @staticmethod
    def full(s: str,
             ch_mask: str = '*',
             exceptions: list[str] = None) -> str:
        """
        ========================================================================
         1. Return a string where all chars are masked with the mask-char.
         2. Except those in the exceptions list.
        ------------------------------------------------------------------------
         Ex: 'abc' -> '***'
        ========================================================================
        """
        if exceptions is None:
            exceptions = Mask._EXCEPTIONS
        return ''.join(ch if ch in exceptions else ch_mask for ch in s)

    @staticmethod
    def pct(s: str,
            pct_to_mask: int,
            ch_mask: str = '*',
            exceptions: list[str] = None) -> str:
        """
        ========================================================================
         1. Return a string with a given percentage of chars masked.
         2. Except those in the exceptions list.
        ------------------------------------------------------------------------
         Ex: 'abc' -> 'a*c'
        ========================================================================
        """
        if exceptions is None:
            exceptions = Mask._EXCEPTIONS
        if len(s) == 1:
            return '*'
        indexes = u_list.indexes.sample(li=list(s),
                                        cond=lambda x: x not in exceptions,
                                        pct=pct_to_mask)
        return ''.join(ch_mask if i in indexes else ch
                       for i, ch in enumerate(s))

    @staticmethod
    def one_word(text: str,
                 pct: int = 100,
                 exceptions: list[str] = None) -> str:
        """
        ========================================================================
         Return a Text with one random Masked-Word.
        ------------------------------------------------------------------------
         Ex: 'Hello World!' -> '**** World!'
        ========================================================================
        """
        words = text.split(' ')
        index_word = u_list.indexes.sample(li=words, size=1)[0]
        word_masked = Mask.pct(s=words[index_word],
                               pct_to_mask=pct,
                               exceptions=exceptions)
        words[index_word] = word_masked
        return ' '.join(words)
