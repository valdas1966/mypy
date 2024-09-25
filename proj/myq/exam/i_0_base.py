from f_abstract.mixins.cursorable import Cursorable
from proj.myq.question.i_0_base import QuestionBase
from typing import Generic, TypeVar

Question = TypeVar('Question', bound=QuestionBase)


class ExamBase(Generic[Question], Cursorable[Question]):
    """
    ============================================================================
     Base Exam-Class.
    ============================================================================
    """

    def __init__(self, qs: list[Question]) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        Cursorable.__init__(self, data=qs)
