
class Validatable:
    """
    ============================================================================
     Desc: Represents an Object that can be validated (Default=True).
    ============================================================================
     Properties:
    ----------------------------------------------------------------------------
        1. is_valid (bool) : Object's Validity.
    ============================================================================
    """

    def __init__(self, is_valid: bool = True) -> None:
        self._is_valid = is_valid

    @property
    def is_valid(self) -> bool:
        return self._is_valid

    @is_valid.setter
    def is_valid(self, val) -> None:
        self._is_valid = val
