import pytest

from f_quiz.question_options import QuestionOptions
from f_quiz.question import Question


@pytest.fixture
def q() -> QuestionOptions:
    """
    ========================================================================
     Create a QuestionOptions about Logic.
    ========================================================================
    """
    return QuestionOptions.Factory.logic()


def test_inheritance(q: QuestionOptions) -> None:
    """
    ========================================================================
     Test that QuestionOptions is a Question.
    ========================================================================
    """
    assert isinstance(q, Question)


def test_text(q: QuestionOptions) -> None:
    """
    ========================================================================
     Test the text property.
    ========================================================================
    """
    assert q.text == '***** is formal study of valid inference'


def test_answer(q: QuestionOptions) -> None:
    """
    ========================================================================
     Test the answer property.
    ========================================================================
    """
    assert q.answer == 'Logic'


def test_wrong(q: QuestionOptions) -> None:
    """
    ========================================================================
     Test the wrong property.
    ========================================================================
    """
    assert q.wrong == 'Intuition'


def test_options(q: QuestionOptions) -> None:
    """
    ========================================================================
     Test that options contains both answer and wrong.
    ========================================================================
    """
    opts = q.options
    assert len(opts) == 2
    assert set(opts) == {'Logic', 'Intuition'}


def test_str(q: QuestionOptions) -> None:
    """
    ========================================================================
     Test the __str__() method.
    ========================================================================
    """
    assert str(q) == ('***** is formal study of valid inference'
                       ' -> Logic | Intuition')
