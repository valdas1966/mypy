from f_core.mixins.verbosable.main import Verbosable


class Factory:
    """
    ========================================================================
    Factory for Verbosable objects.
    ========================================================================
    """

    @staticmethod
    def a() -> Verbosable:
        """
        ========================================================================
        Return a Verbosable object with the name 'A'.
        ========================================================================
        """
        return Verbosable(name='A')
