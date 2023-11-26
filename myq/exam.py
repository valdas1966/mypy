from myq.inner.exam.i_0_base import ExamBase
from myq.question import Question


class Exam(ExamBase):
    """
    ============================================================================
     Concrete Exam-Class.
    ============================================================================
    """

    def __init__(self, qs: list[Question]) -> None:
        ExamBase.__init__(self, qs)
