from f_core.mixins.has.name import HasName


class StatsAlgo(HasName):
    """
    ============================================================================
     ABC for Algorithm's Stats.
    ============================================================================
    """

    def __init__(self, name: str = 'StatsAlgo') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        HasName.__init__(self, name=name)
        self.elapsed = 0
