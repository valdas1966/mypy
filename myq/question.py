from myq.inner.question.i_2_inputable import QuestionInputable


class Question(QuestionInputable):
    """
    ============================================================================
     Concrete Question-Class.
    ============================================================================
    """

    def __init__(self, text: str, answer: str) -> None:
        QuestionInputable.__init__(self, text, answer)
