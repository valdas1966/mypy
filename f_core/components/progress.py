from f_core.old_mixins.printable import Printable


class Progress(Printable):
    """
    ============================================================================
     Component Class representing list Progress.
    ============================================================================
    """

    def __init__(self,
                 cur: int,
                 total: int) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._cur = cur
        self._total = total

    def __str__(self) -> str:
        """
        ========================================================================
         Return STR-REPR of the Progress.
         Ex: '[5 / 10]'
        ========================================================================
        """
        return f'[{self._cur} / {self._total}]'
