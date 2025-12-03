from f_core.mixins.has.record_io.main import HasRecordIO


class Factory:
    
    @staticmethod
    def proc() -> HasRecordIO:
        """
        ============================================================================
         Factory method for a HasRecordIO object.
        ============================================================================
        """
        class Proc(HasRecordIO):
            """
            ============================================================================
             Process class.
            ============================================================================
            """
            def __init__(self) -> None:
                HasRecordIO.__init__(self, name='Process', verbose=True)
                self._input = input
