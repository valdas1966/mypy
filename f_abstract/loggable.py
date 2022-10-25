from abc import ABC, abstractmethod
from f_abstract.inittable import Inittable


class Loggable(ABC, Inittable):

    def _log(self, **params) -> None:
        """
        ========================================================================
         Description: Log an Operation.
        ========================================================================
        """
        pass
