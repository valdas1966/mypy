
class RateSuccess:
    """
    ============================================================================
     Manages Success-Rate Statistics.
    ============================================================================
    """

    def __init__(self) -> None:
        self._total = 0
        self._success = 0

    @property
    def total(self) -> int:
        return self._total

    @property
    def success(self) -> int:
        return self._success

    def rate(self) -> float:
        """
        ========================================================================
         Return the Success-Rate.
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
