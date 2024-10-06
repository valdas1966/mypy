from f_google.sheets.utils import UGSheets, Spread
from proj.myq.questions.i_2_mask import QuestionMask
from typing import Type


class SheetBase:
    """
    ============================================================================
     Abstract-Class for Questions-Sheet in Myq.
    ============================================================================
    """

    def __init__(self,
                 id_spread: str,
                 type_question: Type[QuestionMask] = QuestionMask) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._spread = UGSheets.spread(user='VALDAS', id_spread=id_spread)
        self._type_question = type_question

    @property
    def spread(self) -> Spread:
        """
        ========================================================================
         Return the Spread of current Google-Sheet.
        ========================================================================
        """
        return self._spread

    @property
    def type_question(self) -> Type[QuestionMask]:
        """
        ========================================================================
         Return Type of Questions to Build.
        ========================================================================
        """
        return self._type_question
