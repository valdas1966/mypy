import string
from f_utils.dtypes.u_seq import USeq


class Mask:
    """
    ============================================================================
     Utils-Class for applying masking techniques to Strings.
    ============================================================================
    """

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
            exceptions = string.punctuation
        return ''.join(ch if ch in exceptions else ch_mask for ch in s)

    @staticmethod
    def pct(s: str,
            pct_mask: int,
            ch_mask: str = '*',
            exceptions: set[str] = None) -> str:
        """
        ========================================================================
         1. Return a string with a given percentage of chars masked.
         2. Except those in the exceptions list.
        ------------------------------------------------------------------------
         Ex: '(abc)' -> '(a*c)'
        ========================================================================
        """
        if not exceptions:
            exceptions = set()
        if len(s) == 1:
            return '*'
        predicate = lambda x: x not in exceptions
        filtered = USeq.indexes.filter(seq=s, predicate=predicate)
        sampled = USeq.items.sample(seq=filtered, pct=pct_mask)
        return ''.join(ch_mask if i in sampled else ch
                       for i, ch in enumerate(s))
