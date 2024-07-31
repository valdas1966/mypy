from typing import Generic, TypeVar
from proj.myq.exam.i_0_base import ExamBase
from proj.myq.gui.i_0_qa import AppQA

Exam = TypeVar('Exam', bound=ExamBase)


class ManagerExamGui(Generic[Exam]):
    """
    ============================================================================
     Manages the Exam on GUI.
    ============================================================================
    """

    def __init__(self, exam: Exam) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._exam = exam
        self._app = AppQA(question_first=self._exam.next(),
                          on_enter=self._on_enter)
        self._app.run()

    def _on_enter(self, answer: str) -> None:
        """
        ========================================================================
         CallBack on User's Answer.
        ========================================================================
        """
        question = self._exam.current()
        if answer == question.answer:
            if self._exam.has_next():
                question = self._exam.next()
            else:
                self._app.msg_box('The END')
                exit(0)
        else:
            self._app.msg_box(question.answer)
        self._app.update(question)
