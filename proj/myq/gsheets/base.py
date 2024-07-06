from abc import ABC, abstractmethod
from proj.myq.question.i_1_text import QuestionText as Q


class SheetBase(ABC):
    """
    ============================================================================
     Abstract-Class for Questions-Sheet in Myq.
    ============================================================================
    """

    @abstractmethod
    def to_questions(self) -> list[Q]:
        """
        ========================================================================
         Return List of Questions extracted from the Questions-Sheet.
        ========================================================================
        """
        pass
