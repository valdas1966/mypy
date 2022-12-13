from f_abstract.inner.process.a_1_2_init_io import ProcessInitIO
from f_abstract.inner.process.a_3_ops import ProcessOps


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
            args['_input'] = self.output if i else self._input
            args['_globs'] = dict(self._globs)
            # Run the Operation
            op = self._ops[i](**args)
            if not op.is_valid:
                raise Exception(op.e_msg)
            # Set the Process-Output, to the Last-Operation-Output
            self._output = op.output
