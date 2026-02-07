from f_core.mixins.validatable import Validatable
from typing import Generic, TypeVar, Any
from time import perf_counter

Input = TypeVar('Input')
Output = TypeVar('Output')

class Process(Generic[Input, Output],
              Validatable):
    """
    ============================================================================
     Simple unified Process class with optional input and output.
    ============================================================================
    """

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
        msg = self._str_start
        if self._input is not None:
            if isinstance(self._input, HasRecord):
                rec = self._input.str_record()
                if rec:
                    # No label if record exists
                    msg += f' {rec}'
                else:
                    msg += f' [Input={repr(self._input)}]'
            else:
                msg += f' [Input={repr(self._input)}]'
        self.print(msg=msg)

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
        msg = self._str_finish
        if self._output is not None:
            if isinstance(self._output, HasRecord):
                rec = self._output.str_record()
                if rec:
                    msg += f' {rec}'    # <-- NO LABEL
                else:
                    msg += f' [Output={repr(self._output)}]'
            else:
                msg += f' [Output={repr(self._output)}]'
        msg += f' [Elapsed={self._elapsed}]'
        self.print(msg=msg)

    @staticmethod
    def _format_io(value: Any) -> str:
        """
        ========================================================================
         Prefer record-string if value is HasRecord, otherwise use repr(value).
        ========================================================================
        """
        if isinstance(value, HasRecord):
            s = value.str_record()
            # If record is empty, fall back to repr
            return s if s else repr(value)
        return repr(value)
