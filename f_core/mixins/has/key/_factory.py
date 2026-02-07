from f_core.mixins.has.key import HasKey


class Factory:
    """
    ============================================================================
     Factory for the HasKey class.
    ============================================================================
    """

    @staticmethod
    def a() -> HasKey[str]:
        """
        ========================================================================
        Create a HasKey object with the key 'A'.
        ========================================================================
        """
        return HasKey[str](key='A')

    @staticmethod
    def b() -> HasKey[str]:
        """
        ========================================================================
        Create a HasKey object with the key 'B'.
        ========================================================================
        """
        return HasKey[str](key='B')
