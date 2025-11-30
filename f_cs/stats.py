from f_core.mixins.has.record import HasRecord


class StatsAlgo(HasRecord):
    """
    ============================================================================
     ABC for Algorithm's Stats.
    ============================================================================
    """

    RECORD_SPEC = {'elapsed': lambda o: o.elapsed}

    def __init__(self, name: str = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        HasRecord.__init__(self, name=name)
        self._elapsed = 0

    @property
    def elapsed(self) -> int:
        """
        ========================================================================
         Return the elapsed time in seconds.
        ========================================================================
        """
        return self._elapsed

    @elapsed.setter
    def elapsed(self, elapsed: int) -> None:
        """
        ========================================================================
         Set the elapsed time in seconds.
        ========================================================================
        """
        self._elapsed = elapsed
       