from f_core.inner.process.a_2_init_io import ProcessInitIO
from f_core.inner.process.a_3_ops import ProcessOps


class ProcessIO(ProcessOps, ProcessInitIO):
    """
    ============================================================================
     Description: Run the Inner-Operations sequentially with IO-Connections.
    ============================================================================
    """

    # Runnable
    def _run(self) -> None:
        for i in range(len(self._ops)):
            args = self._arg_ops[i]
            # On First Operation:
            #   1. Set the Input as the Process-Input.
            #   2. Otherwise, Set as the Previous-Operation-Output
            args['input'] = self._output if i else self._input
            # Run the Operation
            op = self._ops[i](**args)
            if not op.is_valid:
                self._output = None
                raise Exception(op.e_msg)
            # Set the Process-Output, to the Last-Operation-Output
            self._output = op.output
