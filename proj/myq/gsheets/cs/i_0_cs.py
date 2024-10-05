from abc import ABC, abstractmethod
from f_google.sheets.client import GSheets
from proj.myq.questions.i_2_mask import QuestionMask
from typing import Generic, TypeVar

Q = TypeVar('Q', bound=QuestionMask)


class SheetCS(ABC, Generic[Q]):
    """
    ============================================================================
     Abstract-Class for Sheet in Myq-English.
    ============================================================================
    """

    _ID_SPREAD = '1haZi5T98P6kq3dnq4dO10JHDql'

    def __init__(self) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._spread = GSheets.spread(user='VALDAS',
                                      id_spread=self._ID_SPREAD)

    @abstractmethod
    def to_questions(self) -> list[Q]:
        """
        ========================================================================
         Convert GSheet into Questions.
        ========================================================================
        """
        pass
