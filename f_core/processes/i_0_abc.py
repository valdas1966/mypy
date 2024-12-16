from abc import abstractmethod
from time import time
from f_core.mixins.has_name import HasName
from f_core.mixins.validatable import Validatable


class ProcessABC(HasName, Validatable):
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
        HasName.__init__(self, name=name)
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

    def _run_pre(self) -> None:
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

    def _run_post(self) -> None:
        """
        ========================================================================
         Run necessary operations after the Process finishes.
        ========================================================================
        """
        self._time_finish = time()
        self._elapsed = self._time_finish - self._time_start
