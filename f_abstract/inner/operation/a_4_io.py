from f_abstract.inner.operation.a_3_log import OperationLog


class OperationIO(OperationLog):
    """
    ============================================================================
     Description: Operation Input & Output properties.
    ============================================================================
    """

    # obj (Operation-Input Property)
    _input = None

    # obj (Operation-Output Property)
    _output = None

    @property
    def input(self) -> any:
        return self._input

    @property
    def output(self) -> any:
        return self._output
