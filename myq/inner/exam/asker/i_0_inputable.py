from f_abstract.mixins.inputable import Inputable
from myq.question import Question
from datetime import datetime


class AskerInputable(Inputable):
    """
    ============================================================================
        
    """

    # Inputable
    input:     str        # User's Input
    dt_prompt: datetime   # Prompt DateTime
    dt_input:  datetime   # Input DateTime

    def __init__(self, q: Question) -> None:
        self._q = q

    def gen_prompt(self) -> str:
        """
        ========================================================================
         Generates a Question-Prompt that will be displayed to the User.
        ========================================================================
        """
        return f'{self._q.text}:'

    def ask(self) -> None:
        """
        ========================================================================
         1. Asks a Question the User and captures its Answer.
         2. Updates the Question-Stats based on the answer correctness.
        ========================================================================
        """
        self.get_input()
        if self.input == self.answer:
            self._q.update(True)
        else:
            self._q.update(False)
            print(f'The correct answer is: {self.answer}')
