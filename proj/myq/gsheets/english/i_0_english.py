from abc import abstractmethod
from proj.myq.gsheets.i_0_base import SheetBase
from proj.myq.questions.i_2_mask import QuestionMask
from typing import Type


class SheetEnglish(SheetBase):
    """
    ============================================================================
     Abstract-Class for English-Sheet in Myq-English.
    ============================================================================
    """

    _ID_SPREAD = '1mOhkn4DPpUlgtuQxzTPNWlymBSmq9fS7T0t3IaDFf98'

    def __init__(self,
                 type_question: Type[QuestionMask] = QuestionMask) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        SheetBase.__init__(self,
                           id_spread=SheetEnglish._ID_SPREAD,
                           type_question=type_question)

    @abstractmethod
    def to_questions(self) -> list[Type[QuestionMask]]:
        """
        ========================================================================
         Convert GSheet into Questions.
        ========================================================================
        """
        pass
