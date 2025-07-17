from f_core.mixins.printable import Printable
from f_core.mixins.clonable import Clonable
from abc import abstractmethod


class ProblemAlgo(Printable, Clonable):
    """
    ============================================================================
     ABC for Algorithm's Problem.
    ============================================================================
    """
    
    @abstractmethod
    def clone(self) -> 'ProblemAlgo':
        """
        ========================================================================
         Clone the Problem.
        ========================================================================
        """
        pass
