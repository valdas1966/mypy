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
            RECORD_SPEC = {'a': lambda o: o.a}
            def __init__(self, name: str = 'A'):
                super().__init__(name=name)
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
            RECORD_SPEC = {'a': lambda o: o.a}
            def __init__(self, name: str = 'A'):
                super().__init__(name=name)
                self.a = 1
        class B(A):
            RECORD_SPEC = {'b': lambda o: o.b}
            def __init__(self, name: str = 'B'):
                super().__init__(name=name)
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
