from f_utils import u_random
from f_utils.dtypes.inner.str.indexes import Indexes


class Mask:
    """
    ============================================================================
     Utils-Class for masking a String.
    ============================================================================
    """

    _EXCEPTIONS = (' ', '"', "'")

    @staticmethod
    def full(s: str,
             char_mask: str = '*',
             exceptions: list[str] = None) -> str:
        """
        ========================================================================
         Mask a String (except blank chars).
        ========================================================================
        """
        if exceptions is None:
            exceptions = Mask._EXCEPTIONS
        return ''.join(ch if ch in exceptions else char_mask for ch in s)


    @staticmethod
    def pct(s: str,
            pct_to_mask: int,
            exceptions: list[str] = None) -> str:
        if len(s) == 1:
            return '*'
        n = round(pct_to_mask / 100 * len(s), 0)
        if n == 0:
            n = 1

        indexes = u_random.sample(range(len(s), n)




    @staticmethod
    def one_word(s: str,
                 char_mask: str = '*',
                 exceptions: list[str] = (' ', '"', "'")) -> str:
        return pass

