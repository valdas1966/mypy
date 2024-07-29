from f_abstract.mixins.indexable import Indexable
from proj.myq.question.i_0_base import QuestionBase
from typing import Generic, TypeVar

Question = TypeVar('Question', bound=QuestionBase)


class ExamBase(Generic[Question], Indexable[Question]):
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
        Indexable.__init__(self)
        self._qs = qs

    def to_list(self) -> list[Question]:
        """
        ========================================================================
         Return List of Questions.
        ========================================================================
        """
        return self._qs
