from f_core.process_tolerant import ProcessTolerant


class ProcessMultiSequential(ProcessTolerant):
    """
    ============================================================================
     Description: Run the Inner-Operations sequentially n-times, when n is the
                    length of the input-sequence.
    ============================================================================
    """

    def _set_ops(self) -> None:
        self._ops = [self._process_single] * len(self._input)

    def _set_arg_ops(self) -> None:
        self._arg_ops = [{'input_process': inp} for inp in self._input]
