from myq.inner.question.i_0_text import QuestionText
from f_abstract.mixins.inputable import Inputable
from datetime import datetime


class QuestionInputable(QuestionText, Inputable):
    """
    ============================================================================
     Extends QuestionText to display a Question to the User and captures
      its answer.
    ============================================================================
     Inherited Methods:
    ----------------------------------------------------------------------------
        1. gen_prompt() -> str
           [*] Generates a Prompt that will be displayed to the User.
        2. get_input() -> None
           [*] Captures the User's Input (input-str and date-times).
    ============================================================================
    """

    # QuestionText
    text:      str       # Question's Text
    answer:    str       # Question's Answer
    # Inputable
    input:     str       # User's Input
    dt_prompt: datetime  # Prompt DateTime
    dt_input:  datetime  # Input DateTime

    def __init__(self, text: str, answer: str) -> None:
        QuestionText.__init__(self, text, answer)
        Inputable.__init__(self)
