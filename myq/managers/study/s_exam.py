from myq.managers.exam import ManagerExam
from myq.question import Question
from myq.exam import Exam


q_1 = Question(text='2+2', answer='4')
q_2 = Question(text='2+3', answer='5')
qs = [q_1, q_2]
exam = Exam(qs)
manager = ManagerExam(exam)
manager.run()
