from proj.myq.questions.i_1_text import QuestionText
from typing import Generic, TypeVar
from f_utils import u_input

Q = TypeVar('Q', bound=QuestionText)


class ManagerQuestionPrompt(Generic[Q]):
    """
    ============================================================================
     Manages the Inputable Question-Text process.
    ============================================================================
    """

    def __init__(self) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._q = None
        self._prompt = None
        self._input = None
        self._is_correct = None

    def run(self, q: Q) -> None:
        """
        ========================================================================
            1. Prompt the Question to the User.
            2. Capture the User's Answer.
            3. Check the Answer-Correctness.
            4. Print the Correct-Answer (on fail guess).
            5. Update the Question-Stats based on Correctness.
        ========================================================================
        """
        self._q = q
        self._reset()
        self._ask()
        self._update()
        while not self._is_correct:
            self._print_correct_answer()
            self._ask()

    def _reset(self) -> None:
        """
        ========================================================================
         Reset the Private-Attributes.
        ========================================================================
        """
        self._q = None
        self._prompt = None
        self._input = None
        self._is_correct = None

    def _ask(self) -> None:
        """
        ========================================================================
         Ask the Question, Capture the Answer and Check its correctness.
        ========================================================================
        """
        self._prompt = self._get_prompt()
        self._input = self._get_input()
        self._is_correct = self._get_is_correct()

    def _get_prompt(self) -> str:
        """
        ========================================================================
         Return Prompt that will be displayed to the user (Question-Text).
        ========================================================================
        """
        return f'\n{self._q.text}:'

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
        self._q.stats.update(self._is_correct)

    def _print_correct_answer(self) -> None:
        """
        ========================================================================
         Print the Correct-Answer.
        ========================================================================
        """
        print(f'The correct answer is: {self._q.answer}')
