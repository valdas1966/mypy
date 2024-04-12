from myq.question.i_1_text import QuestionText


def test_text():
    q = QuestionText(text='2+2', answer='4')
    assert str(q) == '2+2 -> 4'
