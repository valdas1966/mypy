
class Split:
    """
    ============================================================================
     Utils-Class for list String data type for Splitting operations.
    ============================================================================
    """

    @staticmethod
    def by_length(s: str, length: int) -> list[str]:
        """
        ========================================================================
         Split the given string into list list of strings of list specified length.
        ========================================================================
        """
        if length < 1:
            raise ValueError("Length must be greater than 0")
        return [s[i:i + length] for i in range(0, len(s), length)]