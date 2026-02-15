from f_core.mixins.validatable.main import Validatable


class ValidatableMutable(Validatable):
    """
    ============================================================================
     Mixin-Class for Validatable Objects with public access to modify.
    ============================================================================
    """

    # Factory
    Factory: type | None = None

    def __init__(self, is_valid: bool) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        super().__init__(is_valid=is_valid)

    def set_valid(self) -> None:
        """
        ========================================================================
         Set the Object to be Valid.
        ========================================================================
        """
        self._is_valid = True

    def set_invalid(self) -> None:
        """
        ========================================================================
         Set the Object to be InValid.
        ========================================================================
        """
        self._is_valid = False
