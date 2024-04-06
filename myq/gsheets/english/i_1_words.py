from myq.gsheets.english.i_0_base import SheetBase
from myq.question.i_1_text import QuestionText


class SheetWords(SheetBase):
    """
    ============================================================================
     Sheet for English-Words in the Myq project.
    ============================================================================
    """

    __NAME_SHEET = 'Words'

    __COL_QUESTION = 2
    __COL_ANSWER = 3

    __ROW_FIRST = 2

    def __init__(self) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        SheetBase.__init__(self)
        self._sheet = self._spread[SheetWords.__NAME_SHEET]

    def to_questions(self) -> tuple[QuestionText, ...]:
        """
        ========================================================================
         Return Tuple of Questions extracted from the SheetWords.
        ========================================================================
        """
        tuples = self._sheet.to_tuples(col_first=SheetWords.__COL_QUESTION,
                                       col_last=SheetWords.__COL_ANSWER,
                                       row_first=SheetWords.__ROW_FIRST)
        return tuple(QuestionText(text=text, answer=answer)
                     for text, answer in tuples)
