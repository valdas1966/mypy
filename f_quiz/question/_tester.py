from f_quiz.question import Question


def test_text_and_answer() -> None:
    """
    ========================================================================
     Test the text property.
    ========================================================================
    """
    q = Question.Factory.capital_of_france()
    assert q.text == 'Capital of France'
    assert q.answer == 'Paris'

