
class Validatable:
    """
    ============================================================================
     Mixin-Class for Validatable Objects.
    ============================================================================
    """

    def __init__(self, is_valid: bool = True) -> None:
        self._is_valid = is_valid

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

    def __bool__(self) -> bool:
        """
        ========================================================================
         Return True if the Object is Valid.
        ========================================================================
        """
        return self._is_valid
