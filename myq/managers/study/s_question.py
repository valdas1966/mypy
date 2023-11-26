from myq.managers.question import ManagerQuestion
from myq.inner.question.i_2_inputable import QuestionInputable as Question


q = Question(text='2+2', answer='4')
m = ManagerQuestion(q)
m.run()
