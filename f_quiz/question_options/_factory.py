from f_quiz.question_options.main import QuestionOptions


class Factory:
    """
    ========================================================================
     Factory for QuestionOptions.
    ========================================================================
    """

    @staticmethod
    def logic() -> QuestionOptions:
        """
        ====================================================================
         Create a Question about Logic definition.
        ====================================================================
        """
        return QuestionOptions(
            text='***** is formal study of valid inference',
            answer='Logic',
            wrong='Intuition'
        )

    @staticmethod
    def formal() -> QuestionOptions:
        """
        ====================================================================
         Create a Question about Formal.
        ====================================================================
        """
        return QuestionOptions(
            text='Logic is ***** study of valid inference',
            answer='formal',
            wrong='informal'
        )
