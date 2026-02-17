from f_core.old_mixins.printable import Printable


class RateSuccess(Printable):
    """
    ============================================================================
     Mixin-Class that Manages the Success-Rate Statistics.
    ============================================================================
    """

    def __init__(self) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._total = 0
        self._success = 0

    @property
    def total(self) -> int:
        """
        ========================================================================
         Total number of Approaches.
        ========================================================================
        """
        return self._total

    @property
    def success(self) -> int:
        """
        ========================================================================
         Number of Successful Approaches.
        ========================================================================
        """
        return self._success

    def rate(self) -> float:
        """
        ========================================================================
         Return the Success-Rate (success / total).
        ========================================================================
        """
        if not self._total:
            return 0
        return self._success / self._total

    def update(self, is_success: bool) -> None:
        """
        ========================================================================
         Updates the Stats based on the received Success.
        ========================================================================
        """
        self._total += 1
        self._success += int(is_success)

    def __str__(self) -> str:
        """
        ========================================================================
         Ex: '[4/10]'
        ========================================================================
        """
        return f'[{self.success}/{self.total}]'
