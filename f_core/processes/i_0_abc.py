from abc import abstractmethod
from time import time
from f_core.mixins.nameable import Nameable
from f_core.mixins.validatable import Validatable


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
        self._elapsed: float | None = None
        self._time_start = None
        self._time_finish = None

    @property
    def elapsed(self) -> float:
        """
        ========================================================================
         Return the elapsed time of the process running.
        ========================================================================
        """
        return self._elapsed

    def run_pre(self) -> None:
        """
        ========================================================================
         Run necessary operations before the start of the Process.
        ========================================================================
        """
        self._elapsed = None
        self._time_start = time()

    @abstractmethod
    def run(self) -> None:
        """
        ========================================================================
         Run the Process.
        ========================================================================
        """
        pass

    def run_post(self) -> None:
        """
        ========================================================================
         Run necessary operations after the Process finishes.
        ========================================================================
        """
        self._time_finish = time()
        self._elapsed = self._time_finish - self._time_start
