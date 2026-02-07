from f_core.mixins.equable.main import Equable


class Factory:
    """
    ============================================================================
     Factory for the Equable class.
    ============================================================================
    """

    class Char(Equable):
        def __init__(self, char: str):
            self.char = char
        def key_comparison(self) -> str:
            return self.char

    @staticmethod
    def a() -> Equable:
        """
        ========================================================================
         Create a Char object with the value 'A'.
        ========================================================================
        """
        return Factory.Char(char='A')

    @staticmethod
    def b() -> Equable:
        """
        ========================================================================
         Create a Char object with the value 'B'.
        ========================================================================
        """
        return Factory.Char(char='B')
        