from f_quiz.question_options.main import QuestionOptions


class QuestionYesNo(QuestionOptions):
    """
    ========================================================================
     Quiz Question with fixed Yes/No Answer Options.
    ========================================================================
    """

    Factory: type = None

    def __init__(self, text: str, answer: str) -> None:
        """
        ====================================================================
         Init with Text and Answer (Yes or No).
        ====================================================================
        """
        wrong = 'No' if answer == 'Yes' else 'Yes'
        QuestionOptions.__init__(self,
                                 text=text,
                                 answer=answer,
                                 wrong=wrong)

    @property
    def options(self) -> list[str]:
        """
        ====================================================================
         Return ['Yes', 'No'] in fixed order.
        ====================================================================
        """
        return ['Yes', 'No']
