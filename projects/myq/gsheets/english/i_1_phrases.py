from projects.myq.gsheets.english.i_0_base import SheetBase, QuestionText


class SheetPhrases(SheetBase):
    """
    ============================================================================
     Sheet for English-Words in the Myq project.
    ============================================================================
    """

    _NAME_SHEET = 'Phrases'

    _COL_QUESTION = 2
    _COL_ANSWER = 3

    _ROW_FIRST = 2

    def __init__(self) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        SheetBase.__init__(self)
        self._sheet = self._spread[SheetPhrases._NAME_SHEET]

    def to_questions(self) -> tuple[QuestionText, ...]:
        """
        ========================================================================
         Return Tuple of Questions extracted from the SheetWords.
        ========================================================================
        """
        tuples = self._sheet.to_tuples(col_first=SheetPhrases._COL_QUESTION,
                                       col_last=SheetPhrases._COL_ANSWER,
                                       row_first=SheetPhrases._ROW_FIRST)
        return tuple(QuestionText(text=text, answer=answer)
                     for text, answer in tuples)
