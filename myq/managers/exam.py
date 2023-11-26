from myq.exam import Exam
from myq.managers.question import ManagerQuestion


class ManagerExam:
    """
    ============================================================================
     Manage the Exam-Process.
    ============================================================================
    """

    def __init__(self, exam: Exam) -> None:
        self._exam = exam
        self._manager_question = ManagerQuestion()

    def run(self) -> None:
        """
        ========================================================================
         Ask a Question in the list ordering.
        ========================================================================
        """
        self._print_start()
        for q in self._exam.questions:
            self._manager_question.run(q)
        self._print_finish()

    @staticmethod
    def _print_start() -> None:
        print('START EXAM')

    @staticmethod
    def _print_finish() -> None:
        print('FINISH EXAM')
