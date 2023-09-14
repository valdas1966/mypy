from myq.subs.question.sub_1_text import QuestionText


class ExamOnlyQuestion:
    """
    ============================================================================
     Desc: Base-Class of Exam with Text-Question.
    ============================================================================
    """

    def __init__(self):
        self._q = None
        self._run_methods()

    def _run_methods(self) -> None:
        """
        ========================================================================
         Desc: Run all methods of the Class.
        ========================================================================
        """
        self._set_question()

    def _set_question(self) -> None:
        """
        ========================================================================
         Desc: Set the Class-Question.
        ========================================================================
        """
        self._q = QuestionText(text='2+2', answer='4')
