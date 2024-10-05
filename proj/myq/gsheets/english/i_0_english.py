from abc import ABC, abstractmethod
from proj.myq.gsheets.i_0_base import SheetBase
from proj.myq.questions.i_2_mask import QuestionMask
from typing import Generic, TypeVar

Question = TypeVar('Question', bound=QuestionMask)


class SheetEnglish(SheetBase[Question]):
    """
    ============================================================================
     Abstract-Class for English-Sheet in Myq-English.
    ============================================================================
    """

    _ID_SPREAD = '1mOhkn4DPpUlgtuQxzTPNWlymBSmq9fS7T0t3IaDFf98'

    def __init__(self) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        SheetBase.__init__(self, id_spread=SheetEnglish._ID_SPREAD)

    @abstractmethod
    def to_questions(self) -> list[Question]:
        """
        ========================================================================
         Convert GSheet into Questions.
        ========================================================================
        """
        pass
