from myq.question.i_1_text import QuestionText
from myq.managers.question.i_0_text import ManagerQuestionText


q = QuestionText(text='2+2', answer='4')
man = ManagerQuestionText()
man.run(q=q)
