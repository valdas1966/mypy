import string


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

    @staticmethod
    def punctuations(s: str) -> str:
        """
        ========================================================================
         Return the String without punctuations.
        ========================================================================
        """
        return Filter.specific_chars(s=s, chars=set(string.punctuation))
