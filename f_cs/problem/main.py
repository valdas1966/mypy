from f_core.mixins.has.name import HasName


class ProblemAlgo(HasName):
    """
    ============================================================================
     ABC for Algorithm's Problem.
    ============================================================================
    """

    def __init__(self, name: str = 'ProblemAlgo') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        super().__init__(name)
