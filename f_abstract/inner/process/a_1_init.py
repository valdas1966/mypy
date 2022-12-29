from f_abstract.operation import Operation


class ProcessInit(Operation):
    """
    ============================================================================
     Description: Operation is the Process' Prototype.
    ============================================================================
    """

    # OperationLog
    def _pre_run(self) -> None:
        self._to_pre_log = True
        super()._pre_run()
