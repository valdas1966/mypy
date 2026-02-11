from f_core.mixins.comparable.main import Comparable


class Factory:
    """
    ============================================================================
     Factory for the Comparable class.
    ============================================================================
    """

    class Char(Comparable):
        def __init__(self, char: str) -> None:
            self.char = char
        @property
        def key(self) -> str:
            return self.char

    @staticmethod
    def a() -> Comparable:
        """
        ========================================================================
         Create a Comparable object with the value 'A'.
        ========================================================================
        """
        return Factory.Char(char='A')

    @staticmethod
    def b() -> Comparable:
        """
        ========================================================================
         Create a Comparable object with the value 'B'.
        ========================================================================
        """
        return Factory.Char(char='B')
