from myq.exams.e_0_only_question import ExamOnlyQuestion
from f_utils import u_input


class ExamWithResponse(ExamOnlyQuestion):
    """
    ============================================================================
     Desc: Extends ExamOnlyQuestion to include User's Response.
    ============================================================================
    """

    def __init__(self):
        self._response = None
        self._dt_a = None
        self._dt_b = None
        self._is_correct = None
        ExamOnlyQuestion.__init__(self)

    def _run_methods(self) -> None:
        """
        ========================================================================
         Desc: Run all methods of the Class.
        ========================================================================
        """
        ExamOnlyQuestion._run_methods(self)
        self._set_response()
        self._set_is_correct()

    def _get_prompt(self) -> str:
        """
        ========================================================================
         Desc: Return the Prompt that will be displayed to the User.
        ========================================================================
        """
        return f'{self._q.text}:'

    def _set_response(self) -> None:
        """
        ========================================================================
         Desc: Get Response from the User and set it in class attributes.
        ========================================================================
        """
        prompt = self._get_prompt()
        t = u_input.get(prompt=prompt, with_dt=True)
        self._response, self._dt_a, self._dt_b = t

    def _set_is_correct(self) -> None:
        """
        ========================================================================
         Desc: Check if the User's Response is a correct Answer.
        ========================================================================
        """
        self._is_correct = self._q.answer == self._response
