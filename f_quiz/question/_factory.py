from f_quiz.question.main import Question


class Factory:
    """
    ========================================================================
     Factory for Question.
    ========================================================================
    """

    @staticmethod
    def capital_of_france() -> Question:
        """
        ====================================================================
         Create a Question 'Capital of France'.
        ====================================================================
        """
        return Question(text='Capital of France', answer='Paris')

    @staticmethod
    def capital_of_germany() -> Question:
        """
        ====================================================================
         Create a Question 'Capital of Germany'.
        ====================================================================
        """
        return Question(text='Capital of Germany', answer='Berlin')
