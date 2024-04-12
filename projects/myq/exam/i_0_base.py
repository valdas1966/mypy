from abc import ABC
from projects.myq.question.i_0_base import QuestionBase
from typing import Generic, TypeVar

Question = TypeVar('Question', bound=QuestionBase)


class ExamBase(ABC, Generic[Question]):
    """
    ============================================================================
     Base Exam-Class.
    ============================================================================
    """

    def __init__(self, qs: tuple[Question, ...]) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._qs = qs

    @property
    # List of Exam's Questions
    def questions(self) -> tuple[Question, ...]:
        return self._qs
