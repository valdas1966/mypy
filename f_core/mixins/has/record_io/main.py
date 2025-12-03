from f_core.mixins.has import HasRecord, HasName


class HasRecordIO(HasName):
    """
    ============================================================================
     Mixin for objects with records for input and output.
    ============================================================================
    """
    
    def __init__(self,
                 name: str = 'HasRecordIO') -> None:
        """
        ============================================================================
         Init private Attributes.
        ============================================================================
        """
        HasName.__init__(self, name)
        self._record_input = HasRecord()
        self._record_output = HasRecord()

    @property
    def record_input(self) -> HasRecord:
        """
        ============================================================================
         Getter for the input record.
        ============================================================================
        """
        return self._record_input
    
    @property
    def record_output(self) -> HasRecord:
        """
        ============================================================================
         Getter for the output record.
        ============================================================================
        """
        return self._record_output
    
    