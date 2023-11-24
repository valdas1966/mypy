from myq.inner.exam.i_0_only_question import ExamOnlyQuestion
from myq.inner.question.i_1_text import QuestionText
from datetime import datetime
from f_utils import u_input


class ExamWithResponse(ExamOnlyQuestion):
    """
    ============================================================================
     Extends ExamOnlyQuestion to include User's Response.
    ============================================================================
    """

    _q:            QuestionText     # Current Question
    _response:     str              # User Response
    _dt_a:         datetime         # Prompt DateTime
    _dt_b:         datetime         # Response DateTime
    _is_correct:   bool             # Response Correctness

    def __init__(self):
        self._response = None
        self._dt_a = None
        self._dt_b = None
        self._is_correct = None
        ExamOnlyQuestion.__init__(self)
        self._set_response()
        self._set_is_correct()

    def _set_response(self) -> None:
        """
        ========================================================================
         Gets Response from the User.
        ========================================================================
        """
        prompt = self.__get_prompt()
        t = u_input.get(prompt=prompt, with_dt=True)
        self._response, self._dt_a, self._dt_b = t

    def _set_is_correct(self) -> None:
        """
        ========================================================================
         Checks if the User's Response is a correct Answer.
        ========================================================================
        """
        self._is_correct = self._q.answer == self._response

    def _prompt(self) -> str:
        """
        ========================================================================
         Returns the Prompt that will be displayed to the User.
        ========================================================================
        """
        return f'{self._q.text}:'
