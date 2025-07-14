from .main import HasName, HasNames


class Factory:
    """
    ============================================================================
     Factory class for creating HasNames objects.
    ============================================================================
    """

    @staticmethod
    def abc() -> HasNames:
        """
        ========================================================================
         Create a HasNames object with the names 'A', 'B', and 'C'.
        ========================================================================
        """
        a = HasName('A')
        b = HasName('B')
        c = HasName('C')
        return HasNames([a, b, c])
    