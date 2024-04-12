from abc import ABC, abstractmethod
from f_google.sheets.client import GSheets
from projects.myq.question.i_1_text import QuestionText


class SheetBase(ABC):
    """
    ============================================================================
     Abstract-Class for Sheet in Myq-English.
    ============================================================================
    """

    _ID_SPREAD = '1mOhkn4DPpUlgtuQxzTPNWlymBSmq9fS7T0t3IaDFf98'

    def __init__(self) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._spread = GSheets.spread(user='VALDAS',
                                      id_spread=SheetBase._ID_SPREAD)

    @abstractmethod
    def to_questions(self) -> tuple[QuestionText, ...]:
        """
        ========================================================================
         Return Tuple of Questions extracted from the SheetWords.
        ========================================================================
        """
        pass
