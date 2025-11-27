from f_core.mixins.has.record.main import HasRecord


class Factory:
    """
    ============================================================================
     Factory of concrete classes that inherit from HasRecord.
    ============================================================================
    """
    
    @staticmethod
    def a() -> HasRecord:
        """
        ========================================================================
         Factory of first concrete class A(HasRecord).
        ========================================================================
        """
        class A(HasRecord):
            FIELDS_SPECIFIC = ('a')
            def __init__(self) -> None:
                self.a = 1
        return A()
    
    @staticmethod
    def b() -> HasRecord:
        """
        ========================================================================
         Factory of second concrete class B(A).
        ========================================================================
        """
        class A(HasRecord):
            FIELDS_SPECIFIC = ('a')
            def __init__(self) -> None:
                self.a = 1
        class B(A):
            FIELDS_SPECIFIC = ('b')
            def __init__(self) -> None:
                super().__init__()
                self.b = 2
        return B()

    @staticmethod
    def none() -> HasRecord:
        """
        ========================================================================
         Factory of a class that does not inherit from HasRecord.
        ========================================================================
        """
        return HasRecord()
