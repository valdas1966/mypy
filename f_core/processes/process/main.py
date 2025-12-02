from f_core.mixins.validatable import Validatable
from f_core.mixins.has.record import HasRecord
from typing import Generic, TypeVar
from time import perf_counter

Input = TypeVar('Input')
Output = TypeVar('Output')

class Process(Generic[Input, Output],
              HasRecord,
              Validatable):
    """
    ============================================================================
     Simple unified Process class with optional input and output.
    ============================================================================
    """

    # Record Specification
    RECORD_SPEC = {'elapsed': lambda o: o._elapsed}

    # Factory
    Factory = None

    def __init__(self,
                 input: Input | None = None,
                 verbose: bool = False,
                 name: str = 'Process') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._input: Input | None = input
        self._output: Output | None = None
        HasRecord.__init__(self, name=name, verbose=verbose)
        Validatable.__init__(self)
        # Init Time Attributes
        self._elapsed: int = None
        self._time_start: float = None
        self._time_finish: float = None
        self._str_start: str = f'[Start]'
        self._str_finish: str = '[Finish]'

    def run(self) -> Output | None:
        """
        ========================================================================
         Run the Process.
        ========================================================================
        """
        self._run_pre()
        self._run()
        self._run_post()
        return self._output

    def _run_pre(self) -> None:
        """
        ========================================================================
         Run necessary operations before the start of the Process.
        ========================================================================
        """
        self._elapsed = None
        self._time_start: float = perf_counter()
        self.print(msg=self._str_start)

    def _run(self) -> None:
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
        self._time_finish = perf_counter()
        self._elapsed = int((self._time_finish - self._time_start) * 1000)  # Convert to milliseconds
        self._str_finish += f' [Elapsed={self._elapsed}]'
        self.print(msg=self._str_finish)
