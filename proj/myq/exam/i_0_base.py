from f_abstract.mixins.iterable import Iterable, Item
from proj.myq.question.i_0_base import QuestionBase
from typing import Generic, TypeVar

Question = TypeVar('Question', bound=QuestionBase)


class ExamBase(Generic[Question], Iterable[Question]):
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
        self._qs = qs

    def to_list(self) -> list[Question]:
        """
        ========================================================================
         Return List of Questions.
        ========================================================================
        """
        return self._qs
