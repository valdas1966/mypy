
class Factory:
    """
    ============================================================================
     Factory for the URe class.
     * URe is a static utility class with no instances, so the Factory
        provides canonical Text inputs used in testing.
    ============================================================================
    """

    @staticmethod
    def simple() -> str:
        """
        ========================================================================
         Return a simple Text with words separated by single spaces.
        ========================================================================
        """
        return 'hello world python'

    @staticmethod
    def mixed_delimiters() -> str:
        """
        ========================================================================
         Return a Text with mixed delimiters: commas, periods, colons,
          semicolons, parentheses, newlines, tabs, question marks.
        ========================================================================
        """
        return 'one, two. three: (four)\nfive; six!\tseven?eight'

    @staticmethod
    def with_duplicates() -> str:
        """
        ========================================================================
         Return a Text where some words appear multiple times.
        ========================================================================
        """
        return 'cat dog cat bird dog cat'

    @staticmethod
    def empty() -> str:
        """
        ========================================================================
         Return an empty Text.
        ========================================================================
        """
        return ''

    @staticmethod
    def only_delimiters() -> str:
        """
        ========================================================================
         Return a Text that contains only delimiters and no words.
        ========================================================================
        """
        return '  , . : ;\n\t () '
