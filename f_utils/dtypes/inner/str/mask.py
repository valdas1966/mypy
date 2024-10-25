from f_utils.dtypes.u_seq import USeq
from f_utils.dtypes.inner.str.filter import Filter


class Mask:
    """
    ============================================================================
     Utils-Class for applying masking techniques to Strings.
    ============================================================================
    """

    _EXCEPTIONS = {' ', '"', "'", '(', ')'}

    @staticmethod
    def full(s: str,
             ch_mask: str = '*',
             exceptions: set[str] = None) -> str:
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
            exceptions: set[str] = None) -> str:
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
        predicate = lambda x: x not in exceptions
        filtered = USeq.indexes.filter(seq=s, predicate=predicate)
        sampled = USeq.items.sample(seq=filtered, pct=pct_to_mask)
        return ''.join(ch_mask if i in sampled else ch
                       for i, ch in enumerate(s))

    @staticmethod
    def one_word(text: str,
                 pct: int = 100,
                 exceptions: set[str] = None) -> tuple[str, str]:
        """
        ========================================================================
         Return a Text with one random Masked-Word and un-masked word.
        ------------------------------------------------------------------------
         Ex: 'Hello World!' -> ('**** World!', 'Hello')
        ========================================================================
        """
        words = text.split(' ')
        # Select one random index
        index_word = USeq.indexes.sample(seq=words, size=1)[0]
        # Selected word in unmasked format
        word_unmasked = Filter.specific_chars(s=words[index_word],
                                              chars=Mask._EXCEPTIONS)
        # Selected word in masked format
        word_masked = Mask.pct(s=words[index_word],
                               pct_to_mask=pct,
                               exceptions=exceptions)
        # Replace unmasked word with its masked format
        words[index_word] = word_masked
        return ' '.join(words), word_unmasked
