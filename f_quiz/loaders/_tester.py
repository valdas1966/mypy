from f_quiz.loaders.u_gsheet import load
from f_quiz.question import Question


def test_load() -> None:
    """
    ========================================================================
     Test the load() function.
    ========================================================================
    """
    questions = load()
    assert len(questions) > 0
    assert isinstance(questions[0], Question)
