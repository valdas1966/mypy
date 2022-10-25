from abc import ABC, abstractmethod
from f_abstract.inittable import Inittable


class Runnable(ABC, Inittable):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._run()

    @abstractmethod
    def _run(self) -> None:
        """
        ========================================================================
         Description: Run a Process.
        ========================================================================
        """
        pass
