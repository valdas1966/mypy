from f_core.mixins.equatable.main import Equatable


class Factory:
    """
    ============================================================================
     Factory for the Equable class.
    ============================================================================
    """

    class Char(Equatable):
        def __init__(self, char: str):
            self.char = char
        def key(self) -> str:
            return self.char

    @staticmethod
    def a() -> Equatable:
        """
        ========================================================================
         Create a Char object with the value 'A'.
        ========================================================================
        """
        return Factory.Char(char='A')

    @staticmethod
    def b() -> Equatable:
        """
        ========================================================================
         Create a Char object with the value 'B'.
        ========================================================================
        """
        return Factory.Char(char='B')
        