from abc import ABC, abstractmethod
from f_google.sheets.utils import UGSheets, Spread
from proj.myq.questions.i_1_text import QuestionText
from typing import Generic, TypeVar

Question = TypeVar('Question', bound=QuestionText)


class SheetBase(ABC, Generic[Question]):
    """
    ============================================================================
     Abstract-Class for Questions-Sheet in Myq.
    ============================================================================
    """

    def __init__(self, id_spread: str) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._spread = UGSheets.spread(user='VALDAS', id_spread=id_spread)

    @property
    def spread(self) -> Spread:
        return self._spread

    @abstractmethod
    def to_questions(self) -> list[Question]:
        """
        ========================================================================
         Return List of Questions extracted from the Questions-Sheet.
        ========================================================================
        """
        pass
