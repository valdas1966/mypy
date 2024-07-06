from proj.myq.exam.i_0_base import ExamBase, QuestionBase
from typing import TypeVar
import random

Q = TypeVar('Q', bound=QuestionBase)


class ExamRandom(ExamBase[Q]):
    """
    ============================================================================
     Exam-Class with random questions.
    ============================================================================
    """

    def __init__(self,
                 qs: list[Q],
                 cnt: int) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        qs = list(random.sample(population=qs, k=cnt))
        ExamBase.__init__(self, qs=qs)
