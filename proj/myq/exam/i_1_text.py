from proj.myq.exam.i_0_base import ExamBase
from proj.myq.question.i_1_text import QuestionText
from typing import TypeVar

Q = TypeVar('Q', bound=QuestionText)


class ExamText(ExamBase[Q]):
    """
    ============================================================================
     Exam for Text-Based Questions.
    ============================================================================
    """

    def __init__(self, qs: list[Q]) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        ExamBase.__init__(self, qs=qs)
