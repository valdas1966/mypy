from f_utils import u_input
from myq.question import Question


class ManagerQuestion:
    """
    ============================================================================
     Manages the Question process.
    ============================================================================
     Methods:
    ----------------------------------------------------------------------------
        1. run() -> None
            [*] Prompt the Question to the User.
            [*] Capture the User's Answer.
            [*] Check the Answer-Correctness.
            [*] Update the Question-Stats based on Correctness.
            [*] Print the Correct-Answer (on fail guess).
    ============================================================================
    """

    _q:          Question   # Question to ask
    _prompt:     str        # Prompt (Question-Text) to the User
    _input:      str        # User's Answer
    _is_correct: bool       # User's Answer Correctness

    def __init__(self, q: Question) -> None:
        """
        ========================================================================
         Constructor.
        ========================================================================
        """
        self._q = q

    def run(self) -> None:
        """
        ========================================================================
            1. Prompt the Question to the User.
            2. Capture the User's Answer.
            3. Check the Answer-Correctness.
            4. Update the Question-Stats based on Correctness.
            5. Print the Correct-Answer (on fail guess).
        ========================================================================
        """
        self._prompt = self._get_prompt()
        self._input = self._get_input()
        self._is_correct = self._get_is_correct()
        if not self._is_correct:
            self._print_correct_answer()
        self._update()

    def _get_prompt(self) -> str:
        """
        ========================================================================
         Return Prompt that will be displayed to the user (Question-Text).
        ========================================================================
        """
        return f'{self._q.text}:'

    def _get_input(self) -> str:
        """
        ========================================================================
         Return the User's Answer.
        ========================================================================
        """
        return u_input.get(prompt=self._prompt)

    def _get_is_correct(self) -> bool:
        """
        ========================================================================
         Return True if the User's Answer is Correct.
        ========================================================================
        """
        return self._input == self._q.answer

    def _update(self) -> None:
        """
        ========================================================================
         Update Question-Stats with the Answer Correctness.
        ========================================================================
        """
        self._q.update(self._is_correct)

    def _print_correct_answer(self) -> None:
        """
        ========================================================================
         Print the Correct-Answer.
        ========================================================================
        """
        print(f'The correct answer is: {self._q.answer}')
