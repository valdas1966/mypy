from proj.myq.gsheets.english.i_0_english import SheetEnglish, Q


class SheetWords(SheetEnglish):
    """
    ============================================================================
     Sheet for English-Words in the Myq project.
    ============================================================================
    """

    _NAME_SHEET = 'Words'

    _COL_QUESTION = 2
    _COL_ANSWER = 3

    _ROW_FIRST = 2

    def __init__(self) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        SheetEnglish.__init__(self)
        self._sheet = self._spread[SheetWords._NAME_SHEET]

    def to_questions(self) -> list[Q]:
        """
        ========================================================================
         Return List of Questions extracted from the SheetWords.
        ========================================================================
        """
        tuples = self._sheet.to_tuples(col_first=SheetWords._COL_QUESTION,
                                       col_last=SheetWords._COL_ANSWER,
                                       row_first=SheetWords._ROW_FIRST)
        return [Q(text=text, answer=answer) for text, answer in tuples]
