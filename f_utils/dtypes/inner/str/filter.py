class Filter:
    """
    ============================================================================
     Utils for applying Filter-Methods on String.
    ============================================================================
    """

    @staticmethod
    def specific_chars(s: str, chars: set[str]) -> str:
        """
        ========================================================================
         Return the String without received specific chars.
        ========================================================================
        """
        return ''.join(ch for ch in s if ch not in chars)
