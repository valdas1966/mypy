
class Inittable:
    """
    ============================================================================
     Desc: Mixin for Classes requiring a two-step init (Attributes and Methods).
    ============================================================================
    """

    def __init__(self) -> None:
        self._init_attributes()
        self._init_methods()

    def _init_attributes(self) -> None:
        """
        ========================================================================
         Desc: Initializes all Class-Attributes.
        ========================================================================
        """
        pass

    def _init_methods(self) -> None:
        """
        ========================================================================
         Desc: Executes all initialization methods.
        ========================================================================
        """
        pass
