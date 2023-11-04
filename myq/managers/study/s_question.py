from myq.managers.question import ManagerQuestion
from myq.question import Question


q = Question(text='2+2', answer='4')
m = ManagerQuestion(q)
m.run()
