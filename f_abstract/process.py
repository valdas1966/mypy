from abc import ABC, abstractmethod
from f_abstract.initable import Initable


class Process(ABC, Initable):

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

    def _log(self, **kwargs_log) -> None:
        """
        ========================================================================
         Description: Log an Operation.
        ========================================================================
        """
        pass
