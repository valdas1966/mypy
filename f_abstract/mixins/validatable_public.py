from f_abstract.mixins.validatable import Validatable


class ValidatablePublic(Validatable):
    """
    ============================================================================
     Mixin-Class for Validatable Objects with public access to modify.
    ============================================================================
    """

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
