from f_core.inner.process.a_3_ops import ProcessOps


class ProcessTolerant(ProcessOps):
    """
    ============================================================================
     Description: Run the Inner-Operations sequentially in tolerant manner
                    (one op failing does not cause the entire process to fail).
    ============================================================================
    """

    # Runnable
    def _run(self) -> None:
        for i, op in enumerate(self._ops):
            args = self._arg_ops[i]
            op(**args)
