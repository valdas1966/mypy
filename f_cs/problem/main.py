from f_core.mixins import Equatable
from f_core.mixins.has.name import HasName
from f_core.protocols.equality.main import SupportsEquality


class ProblemAlgo(HasName, Equatable):
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

    @property
    def key(self) -> SupportsEquality:
        """
        ========================================================================
         Return the Problem's Name.
        ========================================================================
        """
        raise NotImplementedError
