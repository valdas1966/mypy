import pytest

from f_quiz.exam_gui.runner import ExamRunner


@pytest.fixture
def runner() -> ExamRunner:
    """
    ========================================================================
     Create an ExamRunner with two capital city Questions.
    ========================================================================
    """
    return ExamRunner.Factory.two_capitals()


def test_current(runner: ExamRunner) -> None:
    """
    ========================================================================
     Test the current property.
    ========================================================================
    """
    assert runner.current.text == 'Capital of France'


def test_number(runner: ExamRunner) -> None:
    """
    ========================================================================
     Test the number property.
    ========================================================================
    """
    assert runner.number == 1


def test_total(runner: ExamRunner) -> None:
    """
    ========================================================================
     Test the total property.
    ========================================================================
    """
    assert runner.total == 2


def test_score(runner: ExamRunner) -> None:
    """
    ========================================================================
     Test the score property.
    ========================================================================
    """
    assert runner.score == 0


def test_is_finished(runner: ExamRunner) -> None:
    """
    ========================================================================
     Test the is_finished property.
    ========================================================================
    """
    assert not runner.is_finished


def test_check_correct(runner: ExamRunner) -> None:
    """
    ========================================================================
     Test check() with a correct Answer.
    ========================================================================
    """
    assert runner.check(answer='Paris') is True
    assert runner.score == 1
    assert runner.number == 2


def test_check_wrong(runner: ExamRunner) -> None:
    """
    ========================================================================
     Test check() with a wrong Answer.
    ========================================================================
    """
    assert runner.check(answer='London') is False
    assert runner.score == 0
    assert runner.number == 2


def test_full_run(runner: ExamRunner) -> None:
    """
    ========================================================================
     Test a full Exam run.
    ========================================================================
    """
    runner.check(answer='Paris')
    runner.check(answer='Berlin')
    assert runner.is_finished
    assert runner.score == 2
    assert runner.current is None


def test_n_questions() -> None:
    """
    ========================================================================
     Test n_questions limits the number of Questions.
    ========================================================================
    """
    runner = ExamRunner.Factory.two_capitals_n(n_questions=1)
    assert runner.total == 1
    runner.check(answer='Paris')
    assert runner.is_finished


def test_is_random() -> None:
    """
    ========================================================================
     Test is_random shuffles Questions.
    ========================================================================
    """
    runner = ExamRunner.Factory.two_capitals_random()
    texts = {runner.current.text}
    runner.check(answer='skip')
    texts.add(runner.current.text)
    assert texts == {'Capital of France', 'Capital of Germany'}
