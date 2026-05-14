import re


class URe:
    """
    ============================================================================
     Class for Regex-related utilities.
    ============================================================================
    """

    @staticmethod
    def extract_words(text: str) -> list[str]:
        """
        ========================================================================
         Return a List of Words from the given Text, in the order of their
          occurrence.
         * A Word is a maximal sequence of word-characters
            ([A-Za-z0-9_]); any other character (space, comma, period,
            parenthesis, colon, newline, tab, etc.) acts as a delimiter.
         * Duplicates are preserved.
        ========================================================================
        """
        return re.findall(pattern=r'\w+', string=text)
