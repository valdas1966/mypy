from f_core.mixins.has.name import HasName
from f_ds.groups.group import Listable
from f_proj.myq.questions.i_0_base import QuestionBase
from typing import TypeVar

Question = TypeVar('Question', bound=QuestionBase)


class BlockBase(Listable[Question], HasName):
    """
    ============================================================================
     Base-Class for Block of Questions.
    ============================================================================
    """

    def __init__(self, name: str) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        HasName.__init__(self, name=name)
