from proj.myq.exam.i_0_base import ExamBase as Exam
from proj.myq.managers.question.i_0_text import ManagerQuestionText


class ManagerExamText:
    """
    ============================================================================
     Manage the Inputable Question-Text Exam-Process.
    ============================================================================
    """

    def __init__(self, exam: Exam) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._exam = exam
        self._man_question = ManagerQuestionText()

    def run(self) -> None:
        """
        ========================================================================
         1. Run the Exam-Process.
         2. Ask a Question in the list ordering.
        ========================================================================
        """
        self._print_start()
        for i, q in enumerate(self._exam.questions):
            self._man_question.run(q)
        self._print_finish()

    @staticmethod
    def _print_start() -> None:
        """
        ========================================================================
         Print Start of the Exam.
        ========================================================================
        """
        print('START EXAM')

    @staticmethod
    def _print_finish() -> None:
        """
        ========================================================================
         Print Finish of the Exam.
        ========================================================================
        """
        print('\nFINISH EXAM')