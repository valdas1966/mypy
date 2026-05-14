
class GenRe:
    """
    ============================================================================
     Class for Regex-related Test-Input Generators.
    ============================================================================
    """

    @staticmethod
    def simple() -> str:
        """
        ========================================================================
         Generate a simple Text with words separated by single spaces.
        ========================================================================
        """
        return 'hello world python'

    @staticmethod
    def mixed_delimiters() -> str:
        """
        ========================================================================
         Generate a Text with mixed delimiters: commas, periods, colons,
          semicolons, parentheses, newlines, tabs, question marks.
        ========================================================================
        """
        return 'one, two. three: (four)\nfive; six!\tseven?eight'

    @staticmethod
    def with_duplicates() -> str:
        """
        ========================================================================
         Generate a Text where some words appear multiple times.
        ========================================================================
        """
        return 'cat dog cat bird dog cat'

    @staticmethod
    def empty() -> str:
        """
        ========================================================================
         Generate an empty Text.
        ========================================================================
        """
        return ''

    @staticmethod
    def only_delimiters() -> str:
        """
        ========================================================================
         Generate a Text that contains only delimiters and no words.
        ========================================================================
        """
        return '  , . : ;\n\t () '
