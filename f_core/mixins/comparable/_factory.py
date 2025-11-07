from f_core.mixins.comparable.main import Comparable
from f_core.protocols.equable import Equable


class Factory:
    """
    ============================================================================
     Factory for the Comparable class.
    ============================================================================
    """

    class Temp(Comparable):
        def __init__(self, key: str) -> None:
            self.key = key
        def key_comparison(self) -> str:
            return self.key

    @staticmethod
    def a() -> Temp:
        """
        ========================================================================
         Create a Comparable object with the value 'A'.
        ========================================================================
        """
        return Factory.Temp(key='A')

    @staticmethod
    def b() -> Temp:
        """
        ========================================================================
         Create a Comparable object with the value 'B'.
        ========================================================================
        """
        return Factory.Temp(key='B')
