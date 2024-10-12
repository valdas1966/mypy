from f_proj.myq.gsheets.english.i_0_english import SheetEnglish, QuestionMask


class SheetPhrases(SheetEnglish):
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
        SheetEnglish.__init__(self)
        self._sheet = self._spread[SheetPhrases._NAME_SHEET]

    def to_questions(self) -> list[QuestionMask]:
        """
        ========================================================================
         Return List of Questions extracted from the SheetWords.
        ========================================================================
        """
        tuples = self._sheet.to_tuples(col_first=SheetPhrases._COL_QUESTION,
                                       col_last=SheetPhrases._COL_ANSWER,
                                       row_first=SheetPhrases._ROW_FIRST)
        return [QuestionMask(text=text, answer=answer)
                for text, answer in tuples]
