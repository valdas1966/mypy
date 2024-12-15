
class USheet:
    """
    ============================================================================
     Utils-Class for Google-Sheets.
    ============================================================================
    """

    @staticmethod
    def to_letters(index: int) -> str:
        """
        ========================================================================
         Convert Col-Index into Sheet-Letters.
         Ex: 1 to A, 2 to B, ... , 27 to AA and etc.
        ========================================================================
        """
        letters = str()
        while index > 0:
            index, remainder = divmod(index - 1, 26)
            letters = chr(65 + remainder) + letters
        return letters

    @staticmethod
    def to_a1_range(row_first: int,
                    row_last: int,
                    col_first: int,
                    col_last: int) -> str:
        """
        ========================================================================
         Convert to A1-Notation Range, ex: (A1:Z5).
        ========================================================================
        """
        letter_col_first = USheet.to_letters(index=col_first)
        letter_col_last = USheet.to_letters(index=col_last)
        return f'{letter_col_first}{row_first}:{letter_col_last}{row_last}'
