from f_core.mixins.printable import Printable
from f_core.abstracts.clonable import Clonable
from abc import ABC, abstractmethod


class ProblemAlgo(ABC, Printable, Clonable):
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
