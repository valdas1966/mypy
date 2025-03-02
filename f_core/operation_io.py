from f_core.inner.operation.a_3_log import OperationLog


class OperationIO(OperationLog):
    """
    ============================================================================
     Description: Operation InputRequest & OutputRequest properties.
    ============================================================================
     Attributes:
    ----------------------------------------------------------------------------
        1. input : any.
    ============================================================================
    """

    def _init_add_atts(self) -> None:
        """
        ========================================================================
         Description: Additional Attrs.
        ========================================================================
        """
        super()._init_add_atts()
        if not hasattr(self, '_input'):
            self._input = None
        # obj (Operation-OutputRequest Property)
        self._output = None

    @property
    def input(self) -> any:
        return self._input

    @property
    def output(self) -> any:
        return self._output
