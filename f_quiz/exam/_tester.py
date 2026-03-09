from f_quiz.exam import Exam


def test_questions() -> None:
    """
    ========================================================================
     Test that Exam stores the Questions.
    ========================================================================
    """
    exam = Exam.Factory.two_capitals()
    assert len(exam.questions) == 2
    assert exam.questions[0].text == 'Capital of France'
    assert exam.questions[1].text == 'Capital of Germany'


def test_run_correct(monkeypatch) -> None:
    """
    ========================================================================
     Test run() with all correct answers.
    ========================================================================
    """
    answers = iter(['Paris', 'Berlin'])
    monkeypatch.setattr('builtins.input', lambda _: next(answers))
    exam = Exam.Factory.two_capitals()
    exam.run()


def test_run_wrong(monkeypatch) -> None:
    """
    ========================================================================
     Test run() with wrong answers.
    ========================================================================
    """
    answers = iter(['London', 'Madrid'])
    monkeypatch.setattr('builtins.input', lambda _: next(answers))
    exam = Exam.Factory.two_capitals()
    exam.run()
