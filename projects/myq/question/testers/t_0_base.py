from projects.myq.question.i_0_base import QuestionBase


def test_pct_answered():
    q = QuestionBase()
    assert q.pct_answered() == 0
    q.update(True)
    assert q.pct_answered() == 1
    q.update(False)
    assert q.pct_answered() == 0.5
