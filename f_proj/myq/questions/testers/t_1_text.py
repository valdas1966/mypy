from f_proj.myq.questions.i_1_text import QuestionText


def test_text():
    q = QuestionText(text='2+2', answer='4')
    assert str(q) == '2+2 -> 4 [0/0]'
