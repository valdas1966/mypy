import pytest

from f_quiz.question_yes_no import QuestionYesNo
from f_quiz.question_options.main import QuestionOptions


@pytest.fixture
def q_yes() -> QuestionYesNo:
    """
    ========================================================================
     Create a QuestionYesNo with Answer 'Yes'.
    ========================================================================
    """
    return QuestionYesNo.Factory.yes()


@pytest.fixture
def q_no() -> QuestionYesNo:
    """
    ========================================================================
     Create a QuestionYesNo with Answer 'No'.
    ========================================================================
    """
    return QuestionYesNo.Factory.no()


def test_inheritance(q_yes: QuestionYesNo) -> None:
    """
    ========================================================================
     Test that QuestionYesNo is a QuestionOptions.
    ========================================================================
    """
    assert isinstance(q_yes, QuestionOptions)


def test_answer_yes(q_yes: QuestionYesNo) -> None:
    """
    ========================================================================
     Test that Answer is 'Yes'.
    ========================================================================
    """
    assert q_yes.answer == 'Yes'


def test_answer_no(q_no: QuestionYesNo) -> None:
    """
    ========================================================================
     Test that Answer is 'No'.
    ========================================================================
    """
    assert q_no.answer == 'No'


def test_wrong_yes(q_yes: QuestionYesNo) -> None:
    """
    ========================================================================
     Test that Wrong is 'No' when Answer is 'Yes'.
    ========================================================================
    """
    assert q_yes.wrong == 'No'


def test_wrong_no(q_no: QuestionYesNo) -> None:
    """
    ========================================================================
     Test that Wrong is 'Yes' when Answer is 'No'.
    ========================================================================
    """
    assert q_no.wrong == 'Yes'


def test_options_fixed_order(q_yes: QuestionYesNo,
                             q_no: QuestionYesNo) -> None:
    """
    ========================================================================
     Test that Options are always ['Yes', 'No'] in fixed order.
    ========================================================================
    """
    assert q_yes.options == ['Yes', 'No']
    assert q_no.options == ['Yes', 'No']


def test_text(q_yes: QuestionYesNo) -> None:
    """
    ========================================================================
     Test the Question Text.
    ========================================================================
    """
    assert q_yes.text == 'Logic is formal study of valid inference'
