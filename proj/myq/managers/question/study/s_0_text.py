from proj.myq.question.i_1_text import QuestionText
from proj.myq.managers.question.i_0_text import ManagerQuestionText


q = QuestionText(text='2+2', answer='4')
ManagerQuestionText(q=q).run()
