from f_abstract.mixins.nameable import Nameable
from f_ds.groups.group import Listable
from f_proj.myq.questions.i_0_base import QuestionBase
from typing import TypeVar

Question = TypeVar('Question', bound=QuestionBase)


class BlockBase(Listable[Question], Nameable):
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
        Nameable.__init__(self, name=name)
