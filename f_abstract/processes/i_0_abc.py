from abc import abstractmethod
from f_abstract.mixins.nameable import Nameable
from f_abstract.mixins.validatable import Validatable


class ProcessABC(Nameable, Validatable):
    """
    ============================================================================
     ABC of Process-Classes.
    ============================================================================
    """

    def __init__(self,
                 name: str = 'Process') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        Nameable.__init__(self, name=name)
        Validatable.__init__(self)

    @abstractmethod
    def run(self) -> None:
        """
        ========================================================================
         Run the Process.
        ========================================================================
        """
        pass
