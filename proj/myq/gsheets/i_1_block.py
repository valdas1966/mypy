from abc import abstractmethod
from proj.myq.questions.i_1_text import QuestionText
from typing import TypeVar
from proj.myq.gsheets.i_0_base import SheetBase

Question = TypeVar('Question', bound=QuestionText)


class SheetBlock(SheetBase[Question]):
    """
    ============================================================================
     Abstract-Class for Questions-Sheet in Myq.
    ============================================================================
    """

    @abstractmethod
    def to_questions(self) -> list[Question]:
        """
        ========================================================================
         Return List of Questions extracted from the Questions-Sheet.
        ========================================================================
        """
        pass
