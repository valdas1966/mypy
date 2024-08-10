from proj.myq.gsheets.english.i_0_english import SheetEnglish, QuestionText


class SheetDefinitions(SheetEnglish):
    """
    ============================================================================
     Sheet for English-Words in the Myq project.
    ============================================================================
    """

    _NAME_SHEET = 'Definitions'

    _COL_QUESTION = 3
    _COL_ANSWER = 2

    _ROW_FIRST = 2

    def __init__(self) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        SheetEnglish.__init__(self)
        self._sheet = self._spread[SheetDefinitions._NAME_SHEET]

    def to_questions(self) -> list[QuestionText]:
        """
        ========================================================================
         Return List of Questions extracted from the SheetWords.
        ========================================================================
        """
        tuples = self._sheet.to_tuples(col_first=SheetDefinitions._COL_ANSWER,
                                       col_last=SheetDefinitions._COL_QUESTION,
                                       row_first=SheetDefinitions._ROW_FIRST)
        return [QuestionText(text=text, answer=answer)
                for answer, text in tuples]
