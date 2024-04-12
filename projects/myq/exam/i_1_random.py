from projects.myq.exam.i_0_base import ExamBase, QuestionBase
from typing import Generic, TypeVar
import random

Question = TypeVar('Question', bound=QuestionBase)


class ExamRandom(ExamBase[Question]):

    def __init__(self, qs: tuple[Question], cnt: int) -> None:
        qs = tuple(random.sample(population=qs, k=cnt))
        ExamBase.__init__(self, qs=qs)