from projects.myq.exam.i_0_base import ExamBase
from projects.myq.question.i_1_text import QuestionText
from typing import TypeVar

Question = TypeVar('Question', bound=QuestionText)


class ExamText(ExamBase[Question]):
    """
    ============================================================================
     Exam for Text-Based Questions.
    ============================================================================
    """

    def __init__(self, qs: tuple[Question, ...]) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        ExamBase.__init__(self, qs=qs)
