from f_quiz.question_yes_no.main import QuestionYesNo


class Factory:
    """
    ========================================================================
     Factory for QuestionYesNo.
    ========================================================================
    """

    @staticmethod
    def yes() -> QuestionYesNo:
        """
        ====================================================================
         Create a QuestionYesNo with Answer 'Yes'.
        ====================================================================
        """
        return QuestionYesNo(
            text='Logic is formal study of valid inference',
            answer='Yes'
        )

    @staticmethod
    def no() -> QuestionYesNo:
        """
        ====================================================================
         Create a QuestionYesNo with Answer 'No'.
        ====================================================================
        """
        return QuestionYesNo(
            text='Logic is informal study of valid inference',
            answer='No'
        )
