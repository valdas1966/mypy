from typing import Generic, TypeVar
from proj.myq.exam.i_0_base import ExamBase
from proj.myq.gui.i_0_qa import AppQA

Exam = TypeVar('Exam', bound=ExamBase)


class ManagerExamGui(Generic[Exam]):

    def __init__(self, exam: Exam) -> None:
        self._exam = exam
        question_first = self._exam[0].text
        self._app = AppQA(question_first=question_first,
                          on_enter=self._on_enter)
        self._update = self._app.update
        self._index = 1
        self._app.run()

    def _on_enter(self, answer: str) -> None:
        question = self._exam[self._index].text
        self._update(question)
        self._index += 1


