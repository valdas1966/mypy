from f_abstract.inner.process.a_3_ops import ProcessOps


class ProcessSequence(ProcessOps):
    """
    ============================================================================
     Description: Run the Inner-Operations sequentially.
    ============================================================================
    """

    # Runnable
    def _run(self) -> None:
        for i, op in enumerate(self._ops):
            args = self._arg_ops[i]
            args['_globs'] = dict(self._globs)
            op(**args)
