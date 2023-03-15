from f_abstract.inner.process.a_3_ops import ProcessOps


class ProcessBlock(ProcessOps):
    """
    ============================================================================
     Description: Run the Inner-Operations sequentially as Transaction
                    (Process fails when one Operation is failed).
    ============================================================================
    """

    # Runnable
    def _run(self) -> None:
        for i, op in enumerate(self._ops):
            args = self._arg_ops[i]
            operation = op(**args)
            if not operation.is_valid:
                raise Exception(operation.e_msg)
