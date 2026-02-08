from f_core.mixins.hashable import Hashable


class Factory:
    """
    ============================================================================
     Factory for the Hashable class.
    ============================================================================
    """

    class Char(Hashable):
        """
        ============================================================================
         Hashable class for characters.
        ============================================================================
        """
        def __init__(self, char: str):
            self.char = char
        def key_comparison(self) -> str:
            return self.char

    @staticmethod
    def a() -> Hashable:
        """
        ========================================================================
         Create a Hashable object with the key 'A'.
        ========================================================================
        """
        return Factory.Char(char='A')

    @staticmethod
    def b() -> Hashable:
        """
        ========================================================================
         Create a Hashable object with the key 'B'.
        ========================================================================
        """
        return Factory.Char(char='B')
