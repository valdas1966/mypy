from abc import ABC
from proj.myq.question.i_0_base import QuestionBase
from typing import Generic, TypeVar

Q = TypeVar('Q', bound=QuestionBase)


class ExamBase(ABC, Generic[Q]):
    """
    ============================================================================
     Base Exam-Class.
    ============================================================================
    """

    def __init__(self, qs: list[Q]) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._qs = qs

    @property
    # List of Exam's Questions
    def questions(self) -> list[Q]:
        return self._qs
