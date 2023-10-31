from myq.inner.question.i_0_text import QuestionText
from myq.inner.question.i_0_stats import QuestionStats


class Question(QuestionText, QuestionStats):

    # QuestionText
    text:   str   # Question's Text
    answer: str   # Question's Answer

    def __init__(self, text: str, answer: str) -> None:
        QuestionText.__init__(self, text, answer)
        QuestionStats.__init__(self)
