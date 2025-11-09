from f_core.mixins.has.name import HasName
from f_core.mixins.validatable import Validatable
from f_core.processes.mixins.has_verbose import HasVerbose
from f_utils import u_datetime
from time import time


class ProcessABC(HasName, HasVerbose, Validatable):
    """
    ============================================================================
     ABC of Process-Classes.
    ============================================================================
    """

    def __init__(self,
                 verbose: bool = False,
                 name: str = 'Process') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        HasName.__init__(self, name=name)
        HasVerbose.__init__(self, verbose=verbose)
        Validatable.__init__(self)
        # Init Time Attributes
        self._elapsed: float = None
        self._time_start: float = None
        self._time_finish: float = None

    @property
    def time_start(self) -> float:
        """
        ========================================================================
         Return the start time of the process running.
        ========================================================================
        """
        return self._time_start

    @property
    def time_finish(self) -> float:
        """
        ========================================================================
         Return the finish time of the process running.
        ========================================================================
        """
        return self._time_finish

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
        self._time_start: float = time()
        if self.verbose:
            print(f'[{u_datetime.now()}] Start: {self.name}')

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
        if self.verbose:
            print(f'[{u_datetime.now()}] Finish: {self.name}')

