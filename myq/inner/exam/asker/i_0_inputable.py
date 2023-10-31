from f_abstract.mixins.inputable import Inputable
from myq.question import Question
from datetime import datetime


class AskerInputable(Inputable):

    # QuestionText
    text:      str        # Question's Text
    answer:    str        # Question's Answer
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
        self.get_input()
        if self._input == self.answer:
            self.update(True)
        else:
            self.update(False)
            print(f'The correct answer is: {self.answer}')
