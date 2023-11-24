from myq.inner.question.i_1_text import QuestionText


class ExamOnlyQuestion:
    """
    ============================================================================
     Base-Class of Exam with Text-Question.
    ============================================================================
    """

    _q: QuestionText           # Current Question

    def __init__(self):
        self._q = None
        self._run_methods()

    def _run_methods(self) -> None:
        """
        ========================================================================
         Executes the Methods.
        ========================================================================
        """
        self._set_question()

    def _set_question(self) -> None:
        """
        ========================================================================
         Sets the Class-Question.
        ========================================================================
        """
        self._q = QuestionText(text='2+2', answer='4')
