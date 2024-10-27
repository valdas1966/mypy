from abc import abstractmethod
from f_abstract.mixins.nameable import Nameable
from typing import Generic, TypeVar

Result = TypeVar('Result')


class ProcessABC(Generic[Result], Nameable):
    """
    ============================================================================
     ABC of Process-Classes.
    ============================================================================
    """

    def __init__(self, name: str = 'Process') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        Nameable.__init__(self, name=name)

    @abstractmethod
    def run(self, **kwargs) -> Result:
        """
        ========================================================================
         ABC-Method that executes the Process and returns its Result.
        ========================================================================
        """
        pass
