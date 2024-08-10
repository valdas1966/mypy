from proj.myq.exam.i_0_base import ExamBase, QuestionBase
from typing import TypeVar

Q = TypeVar('Q', bound=QuestionBase)


class ExamCombine(ExamBase[Q]):
    """
    ============================================================================
     Exam-Class that combine multiple Exams.
    ============================================================================
    """

    def __init__(self,
                 exams: list[ExamBase[Q]]) -> None:
        """
        ========================================================================
         Init private Attributes (combine questions from all exams).
        ========================================================================
        """
        qs = list()
        for exam in exams:
            qs.extend(exam.to_list())
        ExamBase.__init__(self, qs=qs)
