
class Predicates:
    """
    ============================================================================
     Utils-Class for string predicates.
    ============================================================================
    """

    @staticmethod
    def is_wrapped(s: str, wrap: str) -> bool:
        """
        ========================================================================
         Return True if the given String is wrapped by the given Wrap.
        =======================================================================
        """
        return s[0] == wrap and s[-1] == wrap

    @staticmethod
    def is_not_wrapped(s: str, wrap: str) -> bool:
        """
        ========================================================================
         Return True if the given String is not wrapped by the given Wrap.
        ========================================================================
        """
        return not Predicates.is_wrapped(s=s, wrap=wrap)